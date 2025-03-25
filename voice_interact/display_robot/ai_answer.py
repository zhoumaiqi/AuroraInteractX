import requests

# 设置您的 Kimi API 密钥
api_key = 'sk-UhVXohb8ZD5vdGGfzjICECWd6L5WHhIhV9oQkoRVUhHe3qZs'

# 读取问题
with open('/home/sunrise/display_robot/txt/question.txt', 'r', encoding='utf-8') as file:
    question = file.read().strip()

# 设置请求头
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# 设置请求体
data = {
    'model': 'moonshot-v1-8k',
    'messages': [
        {'role': 'user', 'content': question}
    ]
}

# 发送 POST 请求
response = requests.post('https://api.moonshot.cn/v1/chat/completions', headers=headers, json=data)

# 检查请求是否成功
if response.status_code == 200:
    # 获取回答内容
    answer = response.json()['choices'][0]['message']['content'].strip()

    # 将回答保存到文件
    with open('/home/sunrise/display_robot/txt/answer.txt', 'w', encoding='utf-8') as file:
        file.write(answer)
else:
    print(f'请求失败，状态码：{response.status_code}，错误信息：{response.text}')
