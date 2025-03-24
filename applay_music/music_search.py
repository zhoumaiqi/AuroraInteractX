import os
import re
import requests
import subprocess
from pathlib import Path
import vlc
import time

# 配置参数
API_TOKEN = "zljvjxxxmpzijryxmgex1rn64ihnfr"
KEYWORDS_PATH = "/home/zhoumaiqi/MY_ROBOT/AuroraInteractX/applay_music/commands/keywords.txt"  # 关键词输出路径
AUDIO_TEXT_PATH = "/home/zhoumaiqi/MY_ROBOT/AuroraInteractX/applay_music/commands/audio_text.txt"  # 音频转文本文件路径

def ensure_directory(path):
    """创建目录（如果不存在）"""
    Path(path).mkdir(parents=True, exist_ok=True)

def read_text_from_file(file_path):
    """读取指定路径的文本文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_text_to_file(file_path, text):
    """将文本写入指定路径的文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def parse_music_command(text):
    """解析语音指令"""
    patterns = [
        r"播放(.+?)的(.+)",    
        r"来一首(.+)",         
        r"我想听(.+?)唱的(.+)" # 匹配 "我想听林俊杰唱的江南"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.groups()
    return None

def search_music_on_netease(keyword):
    """通过网易云音乐API进行音乐搜索"""
    url = f"http://music.163.com/api/search/get"
    params = {
        's': keyword,
        'type': 1,
        'limit': 1
    }
    headers = {
        'Referer': 'http://music.163.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.post(url, data=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result['result']['songs']:
            return result['result']['songs'][0]
    return None


def play_music(url):
    print(f"Playing music from URL: {url}")
    player = vlc.MediaPlayer(url)
    player.play()
    time.sleep(1)  # 等待播放器初始化

    state = player.get_state()
    print(f"Player state after play: {state}")

    while player.is_playing():
        time.sleep(1)
        state = player.get_state()
        print(f"Player state: {state}")


def process_audio_text():
    """处理音频转文本文件"""
    ensure_directory(Path(KEYWORDS_PATH).parent)
    text = read_text_from_file(AUDIO_TEXT_PATH)
    print(f"Read text: {text}")
    command = parse_music_command(text)
    print(f"Parsed command: {command}")
    
    if command:
        # 将解析出的关键词写入文件
        keywords = ' '.join(command)
        write_text_to_file(KEYWORDS_PATH, keywords)
        print(f"Written keywords to file: {keywords}")
        
        # 进行音乐搜索
        song = search_music_on_netease(keywords)
        print(f"Search results: {song}")
        
        if song:
            title = song["name"]
            artists = ", ".join(artist["name"] for artist in song["artists"])
            album = song["album"]["name"]
            url = f"http://music.163.com/song/media/outer/url?id={song['id']}.mp3"
            print(f"Title: {title}, Artists: {artists}, Album: {album}, URL: {url}")
            
            # 播放音乐
            play_music(url)
        else:
            print("No songs found.")

if __name__ == "__main__":
    process_audio_text()