import serial
import json
import subprocess
from time import sleep
from threading import Lock

# ===== 用户配置区 =====
TARGET_SCRIPT = "/home/sunrise/display_robot/all.py"
MAX_SCRIPT_RUNTIME = 30

# ===== 全局变量 =====
script_lock = Lock()

def execute_script():
    """非阻塞方式执行目标脚本"""
    try:
        if not script_lock.acquire(blocking=False):
            print("已有脚本正在运行，跳过本次执行")
            return False
        
        print(f"开始执行脚本：{TARGET_SCRIPT}")
        process = subprocess.Popen(
            ["python3", TARGET_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 等待脚本完成执行，去掉了 timeout
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print("脚本执行成功")
        else:
             
            print(f"脚本异常退出（代码{process.returncode}）：{stderr.decode()}")

    except Exception as e:
        print(f"执行异常：{str(e)}")
    finally:
        script_lock.release()
    return True



def parse_json(buffer):
    """增强版JSON解析器"""
    decoder = json.JSONDecoder()
    start_idx = buffer.find(b'{"content":')
    
    if start_idx == -1:
        return None, buffer
    
    try:
        # 尝试解析完整JSON
        obj, end_idx = decoder.raw_decode(buffer[start_idx:].decode('utf-8', 'ignore'))
        end_idx += start_idx
        return obj, buffer[end_idx:]
    except json.JSONDecodeError:
        # 数据不完整时保留剩余数据
        return None, buffer[start_idx:]

def main():
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        xonxoff=True,
        timeout=1
    )
    
    buffer = b''
    print(f"开始监听串口 {ser.name}...")

    try:
        while True:
            buffer += ser.read_all()
            
            while True:
                # 尝试解析JSON
                data, new_buffer = parse_json(buffer)
                if data is None:
                    break
                
                buffer = new_buffer
                try:
                    if data.get('content', {}).get('eventType') == 4:
                        # 处理嵌套的info字段
                        info_str = data['content'].get('info', '{}')
                        try:
                            info_data = json.loads(info_str)
                        except:
                            info_data = {}
                            print("警告：info字段解析失败")
                        
                        keyword = data['content'].get('result', '')
                        print(f"\n=== 唤醒成功！关键词：{keyword} ===")
                        execute_script()
                        
                except Exception as e:
                    print(f"数据处理异常：{str(e)}")

            sleep(0.01)

    except KeyboardInterrupt:
        print("\n程序已终止")
    finally:
        ser.close()

if __name__ == "__main__":
    main()