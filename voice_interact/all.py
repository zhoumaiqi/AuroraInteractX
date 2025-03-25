
# import subprocess
# import sys
# import threading
# import time
# from multiprocessing import Process  # 新增多进程支持

# # 音频路径配置保持不变
# HERE_WAV_PATH = '/home/sunrise/display_robot/audio/imhere.wav'
# WAV_FILE_PATH = '/home/sunrise/display_robot/audio/question.wav'
# ANSWER_WAV_PATHS = [
#     '/home/sunrise/display_robot/audio/answer1.wav',
#     '/home/sunrise/display_robot/audio/answer2.wav',
#     '/home/sunrise/display_robot/audio/answer3.wav',
#     '/home/sunrise/display_robot/audio/answer4.wav',
#     '/home/sunrise/display_robot/audio/answer5.wav'
# ]

# def run_script(script_path):
#     """运行子脚本（保持原逻辑）"""
#     result = subprocess.run(['python3', script_path], capture_output=True, text=True)
#     if result.returncode != 0:
#         print(f"Error running {script_path}: {result.stderr}")
#     else:
#         print(f"Output of {script_path}: {result.stdout}")

# def record_audio():
#     commands = [
#         ['arecord', '-D', 'hw:0,1', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-d', '5', WAV_FILE_PATH],
#         ['arecord', '-D', 'hw:0,0', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-d', '5', WAV_FILE_PATH],
#         ['arecord', '-D', 'hw:1,0', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-d', '5', WAV_FILE_PATH],
#         ['arecord', '-D', 'hw:1,1', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-d', '5', WAV_FILE_PATH]
#     ]

#     for command in commands:
#         try:
#             print(f"尝试执行命令: {' '.join(command)}")
#             subprocess.run(command, check=True)
#             print(f"录音完成，音频保存至 {WAV_FILE_PATH}")
#             break
#         except subprocess.CalledProcessError as e:
#             print(f"录音失败: {e}")
#     else:
#         print("所有录音命令均失败")
#         sys.exit(1)

# def play_audio(file_path):
#     """同步阻塞式音频播放（关键修改）"""
#     commands = [
#         ['aplay', '-D', 'plughw:0,1', file_path],
#         ['aplay', '-D', 'plughw:0,0', file_path],
#         ['aplay', '-D', 'plughw:1,1', file_path],
#         ['aplay', '-D', 'plughw:1,0', file_path]
#     ]
    
#     # 同步执行播放命令
#     for command in commands:
#         try:
#             print(f"尝试播放: {file_path}")
#             subprocess.run(command, check=True)
#             print(f"播放完成: {file_path}")
#             return  # 播放成功则退出
#         except subprocess.CalledProcessError as e:
#             print(f"播放失败: {e}")
#     print(f"全部设备尝试失败: {file_path}")
#     sys.exit(1)

# def play_audio1():
#     """提示音播放"""
#     play_audio(HERE_WAV_PATH)

# def play_audio2():
#     """严格顺序播放答案音频"""
#     for path in ANSWER_WAV_PATHS:
#         play_audio(path)  # 同步阻塞播放

# def run_scripts_concurrently(scripts):
#     """使用多进程运行脚本（关键修改）"""
#     processes = []
#     for script in scripts:
#         p = Process(target=run_script, args=(script,))  # 改用进程
#         processes.append(p)
#         p.start()
    
#     for p in processes:
#         p.join()

# def play_audio_with_delay():
#     """带延迟的音频播放"""
#     time.sleep(3)
#     play_audio2()

# if __name__ == "__main__":
#     # 第一阶段：初始播放和录音
#     play_audio1()
#     record_audio()

#     # 第二阶段：顺序执行核心脚本
#     phase1_scripts = [
#         '/home/sunrise/display_robot/iat_python3.py',
#         '/home/sunrise/display_robot/ai_answer.py',
#         '/home/sunrise/display_robot/bettertxt.py',
#         '/home/sunrise/display_robot/depart.py',
#         '/home/sunrise/display_robot/tts_python1.py'
#     ]
    
#     for script in phase1_scripts:
#         print(f"Running {script}...")
#         run_script(script)
#         print(f"Finished running {script}.\n")

#     # 第三阶段：并行执行TTS和播放
#     tts_scripts = [
#         '/home/sunrise/display_robot/tts_python2.py',
#         '/home/sunrise/display_robot/tts_python3.py',
#         '/home/sunrise/display_robot/tts_python4.py',
#         '/home/sunrise/display_robot/tts_python5.py'
#     ]

#     # 创建并启动线程/进程
#     audio_thread = threading.Thread(target=play_audio_with_delay)
#     tts_process = Process(target=run_scripts_concurrently, args=(tts_scripts,))  # TTS使用进程

#     audio_thread.start()
#     tts_process.start()

#     # 等待任务完成
#     audio_thread.join()
#     tts_process.join()

#     print("所有任务执行完成")
import subprocess
import sys
import threading
import time
from multiprocessing import Process  # 新增多进程支持

# 音频路径配置保持不变
HERE_WAV_PATH = '/home/sunrise/display_robot/audio/imhere.wav'
WAV_FILE_PATH = '/home/sunrise/display_robot/audio/question.wav'
ANSWER_WAV_PATHS = [
    '/home/sunrise/display_robot/audio/answer1.wav',
    '/home/sunrise/display_robot/audio/answer2.wav',
    '/home/sunrise/display_robot/audio/answer3.wav',
    '/home/sunrise/display_robot/audio/answer4.wav',
    '/home/sunrise/display_robot/audio/answer5.wav'
]
ADD_WAV_PATH = '/home/sunrise/display_robot/audio/add.wav'  # 新增音频路径

def run_script(script_path):
    """运行子脚本（保持原逻辑）"""
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script_path}: {result.stderr}")
    else:
        print(f"Output of {script_path}: {result.stdout}")

def record_audio():
    commands = [
        ['arecord', '-D', 'hw:0,1', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-d', '5', WAV_FILE_PATH],
        ['arecord', '-D', 'hw:0,0', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-d', '5', WAV_FILE_PATH],
        ['arecord', '-D', 'hw:1,0', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-d', '5', WAV_FILE_PATH],
        ['arecord', '-D', 'hw:1,1', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-d', '5', WAV_FILE_PATH]
    ]

    for command in commands:
        try:
            print(f"尝试执行命令: {' '.join(command)}")
            subprocess.run(command, check=True)
            print(f"录音完成，音频保存至 {WAV_FILE_PATH}")
            break
        except subprocess.CalledProcessError as e:
            print(f"录音失败: {e}")
    else:
        print("所有录音命令均失败")
        sys.exit(1)

def play_audio(file_path):
    """同步阻塞式音频播放（关键修改）"""
    commands = [
        ['aplay', '-D', 'plughw:0,1', file_path],
        ['aplay', '-D', 'plughw:0,0', file_path],
        ['aplay', '-D', 'plughw:1,1', file_path],
        ['aplay', '-D', 'plughw:1,0', file_path]
    ]
    
    # 同步执行播放命令
    for command in commands:
        try:
            print(f"尝试播放: {file_path}")
            subprocess.run(command, check=True)
            print(f"播放完成: {file_path}")
            return  # 播放成功则退出
        except subprocess.CalledProcessError as e:
            print(f"播放失败: {e}")
    print(f"全部设备尝试失败: {file_path}")
    sys.exit(1)

def play_audio1(): 
    """提示音播放"""
    play_audio(HERE_WAV_PATH)

def play_audio2():
    """严格顺序播放答案音频"""
    for path in ANSWER_WAV_PATHS:
        play_audio(path)  # 同步阻塞播放

def run_scripts_concurrently(scripts):
    """使用多进程运行脚本（关键修改）"""
    processes = []
    for script in scripts:
        p = Process(target=run_script, args=(script,))  # 改用进程
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()

def play_audio_with_delay():
    """带延迟的音频播放"""
    time.sleep(3)
    play_audio2()

if __name__ == "__main__":
    # 第一阶段：初始播放和录音
    play_audio1()
    record_audio()

    # 第二阶段：顺序执行核心脚本并播放音频
    phase1_scripts = [
        '/home/sunrise/display_robot/iat_python3.py',
        '/home/sunrise/display_robot/ai_answer.py',
        '/home/sunrise/display_robot/bettertxt.py',
        '/home/sunrise/display_robot/depart.py',
        '/home/sunrise/display_robot/tts_python1.py'
    ]
    
    # 创建并启动播放音频的线程
    add_audio_thread = threading.Thread(target=play_audio, args=(ADD_WAV_PATH,))
    add_audio_thread.start()

    for script in phase1_scripts:
        print(f"Running {script}...")
        run_script(script)
        print(f"Finished running {script}.\n")

    # 等待音频播放完成
    add_audio_thread.join()

    # 第三阶段：并行执行TTS和播放
    tts_scripts = [
        '/home/sunrise/display_robot/tts_python2.py',
        '/home/sunrise/display_robot/tts_python3.py',
        '/home/sunrise/display_robot/tts_python4.py',
        '/home/sunrise/display_robot/tts_python5.py'
    ]

    # 创建并启动线程/进程
    audio_thread = threading.Thread(target=play_audio_with_delay)
    tts_process = Process(target=run_scripts_concurrently, args=(tts_scripts,))  # TTS使用进程

    audio_thread.start()
    tts_process.start()

    # 等待任务完成
    audio_thread.join()
    tts_process.join()

    print("所有任务执行完成")