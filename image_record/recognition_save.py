import cv2
import time
import hashlib
import base64
import json
import requests
import pandas as pd

APP_ID = "858738d4"
API_KEY = "a9f9a7562637cae9653348db83e43bea"
LABEL_FILE = "/home/sunrise/image/label.xlsx"  # 标签表路径

def load_label_map():
    """加载Excel标签映射表"""
    try:
        print("正在加载标签映射表...")
        df = pd.read_excel(LABEL_FILE, sheet_name=0)
        print(f"标签表加载成功，共 {len(df)} 行数据")
        # 清洗列名并转换label值为整数
        df.columns = [col.strip() for col in df.columns]
        df['label'] = df['label'].astype(int)
        return {
            row['label']: {
                'name': str(row['中文']).strip(),
                'category': str(row['分类']).strip()
            } for _, row in df.iterrows()
        }
    except Exception as e:
        print(f"标签表加载失败: {str(e)}")
        print("请检查：1.文件路径 2.Excel列名 3.文件权限")
        exit(1)

# 全局加载标签映射
try:
    LABEL_MAP = load_label_map()
except NameError:
    print("错误：请先安装pandas库 -> sudo pip3 install pandas openpyxl")
    exit(1)

def capture_image():
    """捕获并预处理图像"""
    print("正在初始化摄像头...")
    cap = cv2.VideoCapture("/dev/video8")
    if not cap.isOpened():
        raise Exception("摄像头初始化失败，请检查：\n1.设备路径 /dev/video8\n2.用户是否在video组")
    
    print("正在捕获图像...")
    ret, frame = cap.read()
    cap.release()
  
    if not ret or frame is None:
        raise Exception("图像捕获失败：1.检查摄像头连接 2.调整物体位置")
    print("图像捕获成功")

    # ==== 新增保存代码 ====
    save_path = "/home/sunrise/image/debug.jpg"
    cv2.imwrite(save_path, frame)
    print(f"调试图像已保存至: {save_path}")
    # =====================
  
    print("正在进行图像预处理...")
    # 图像增强处理
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.GaussianBlur(frame, (3,3), 0)  # 降噪
    print("图像预处理完成")
    return cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])[1].tobytes()

def detect_objects():
    try:
        print("正在生成请求参数...")
        # 生成请求参数
        X_CurTime = str(int(time.time()))
        business_params = {"image_name": "cam_capture.jpg"}
        X_Param = base64.b64encode(json.dumps(business_params).encode()).decode()
        X_CheckSum = hashlib.md5((API_KEY + X_CurTime + X_Param).encode()).hexdigest()

        headers = {
            "X-Appid": APP_ID,
            "X-CurTime": X_CurTime,
            "X-Param": X_Param,
            "X-CheckSum": X_CheckSum,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # 获取图像
        image_data = capture_image()
        print(f"图像大小: {len(image_data)/1024:.1f}KB")

        # 发送请求
        print("正在发送请求...")
        response = requests.post(
            "http://tupapi.xfyun.cn/v1/currency",
            headers=headers,
            data=image_data,
            timeout=15
        )
        print("请求发送完成")

        # 解析结果
        print("正在解析响应结果...")
        result = response.json()
        if result.get("code") == 0:
            print("识别成功，正在处理结果...")
            for item in result["data"]["fileList"]:
                label_id = item["label"]
                label_info = LABEL_MAP.get(label_id, {"name": "未知物体", "category": "未分类"})
              
                # 格式化输出
                print("\n" + "="*40)
                print(f"中文名称: {label_info['name']}")
                print(f"所属分类: {label_info['category']}")
                print(f"识别置信度: {item['rate']:.2%}")
                print(f"原始标签ID: {label_id}")
                print("="*40)
        else:
            print(f"请求失败: {result.get('desc', '未知错误')} (代码: {result.get('code')})")

    except Exception as e:
        print(f"系统异常: {str(e)}")
        if 'response' in locals():
            print(f"原始响应: {response.text[:200]}")

if __name__ == "__main__":
    detect_objects()