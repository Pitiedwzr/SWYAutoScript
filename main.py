import os
import cv2
import time
import json
import ast
import socket
import numpy as np
from minicap import capture_screen
import subprocess

# 停止并启动ADB服务器
subprocess.run(['adb', 'kill-server'])
subprocess.run(['adb', 'start-server'])

# 获取ADB设备列表
subprocess.run(['adb', 'devices'])

# 连接Minicap
process = subprocess.Popen("adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 2560x1440@2560x1440/0", shell=True)
time.sleep(3)
process.terminate()
time.sleep(1)
process = subprocess.Popen("adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 2560x1440@2560x1440/0", shell=True)
subprocess.run(['adb', 'forward', 'tcp:1717', 'localabstract:minicap'])

# 连接minitouch
subprocess.run(['adb', 'shell', '/data/local/tmp/minitouch'])
subprocess.run(['adb', 'forward', 'tcp:1111', 'localabstract:minitouch'])

# 创建全局变量存储Socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接Minitouch服务
minitouch_host = 'localhost'  # Minitouch的主机地址
minitouch_port = 1111  # Minitouch的端口号
s.connect((minitouch_host, minitouch_port))

# 点击指定位置
def click_position(x, y):
    global s  # 声明使用全局变量s
    # 发送触摸事件命令
    command = f'd 0 {x} {y} 50\nc\nu 0\nc\n'  # 模拟按下和释放触摸事件命令格式：d <device-id> <x> <y> <pressure>\nu <device-id>
    s.sendall(command.encode())

# Debug
#click_position(10, 550)
#capture_screen()

# 识别模板并点击指定位置
def positionClick(template_path, click_positions, retry_limit=3, time_wait=0.3):
    retry_count = 0
    haveFound = False

    while retry_count < retry_limit and not haveFound:
        capture_screen()
        img_rgb = cv2.imread('screenshot.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(template_path, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            haveFound = True
            for position in click_positions:
                click_position(position[0], position[1])
                time.sleep({time_wait})
        else:
            retry_count += 1

    if not haveFound:
        print("Template not found. Stopping execution.")

# 识别模板并点击模板中心位置（循环时会出现问题，暂时弃用）
def templateClick(template_path, retry_limit=3):
    retry_count = 0
    haveFound = False

    while retry_count < retry_limit and not haveFound:
       capture_screen()  # 在循环开始前获取最新的屏幕截图
       img_rgb = cv2.imread('screenshot.jpg')
       img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

       template = cv2.imread(template_path, 0)
       w, h = template.shape[::-1]
       res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
       threshold = 0.8
       loc = np.where(res >= threshold)
       if len(loc[0]) > 0:
          haveFound = True
          for pt in zip(*loc[::-1]):
                # 计算模板中心位置
              center_x = pt[0] + w // 2
              center_y = pt[1] + h // 2
              click_position(center_x, center_y)
              time.sleep(0.2)  # 在点击后进行延时
       else:
          retry_count += 1

    if not haveFound:
       print("Template not found. Stopping execution.")

# 自动战斗技能点击坐标生成
def generate_click_positions(skill_numbers, skill_click):
    # Positions
    # Char1: 630, 1250
    # Char2: 1070, 1250
    # Char3: 1510, 1250
    # Char4: 1950, 1250
    # S1: 830, 1050
    # S2: 1330, 1050
    # S3: 1830, 1050
    char_positions = [(630, 1250), (1070, 1250), (1510, 1250), (1950, 1250)]
    skill_positions = [(830, 1050), (1330, 1050), (1830, 1050)]
    attack_position = (2350, 1280)

    click_positions = []
    num_chars = len(char_positions)
    num_skills = len(skill_positions)
    skill_index = 0

    for i, skill_number in enumerate(skill_numbers):
        char_index = i % num_chars
        skill_index = (skill_number - 1) % num_skills
        click_positions.append((char_positions[char_index][0], char_positions[char_index][1]))
        click_positions.append((skill_positions[skill_index][0], skill_positions[skill_index][1]))

        if isinstance(skill_click[char_index], tuple):
            skill_click[char_index] = [skill_click[char_index]]

        for pos in skill_click[char_index]:
            click_positions.append(pos)


        if char_index == num_chars - 1:
            click_positions.append(attack_position)

    return click_positions


def testTemplate():
  img_rgb = cv2.imread('screenshot.jpg')
  img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

  template = cv2.imread('template/AutoExplore/ExploreNotion.png',0)
  w, h = template.shape[::-1]
  res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
  threshold = 0.9
  loc = np.where( res >= threshold)
  for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)

  cv2.imshow('Detected',img_rgb)
  cv2.waitKey(0)

def autoExplore():
    templates = [
        "template/AutoExplore/ExploreNotion.png",
        "template/AutoExplore/ExploreNotion2.png",
        "template/AutoExplore/ClickFinishExplore.png",
        "template/AutoExplore/GetReward.png",
        "template/AutoExplore/startExplore.png",
        "template/AutoExplore/SwitchToFinishedExplore.png",
        "template/AutoExplore/ClickFinishExplore.png",
        "template/AutoExplore/GetReward.png",
        "template/AutoExplore/startExplore.png",
        "template/AutoExplore/SwitchToFinishedExplore.png",
        "template/AutoExplore/ClickFinishExplore.png",
        "template/AutoExplore/GetReward.png",
        "template/AutoExplore/startExplore.png",
        "template/AutoExplore/SwitchToFinishedExplore.png",
        "template/AutoExplore/ClickFinishExplore.png",
        "template/AutoExplore/GetReward.png",
        "template/AutoExplore/startExplore.png",
        "template/AutoExplore/clickGetTianGongStone.png"
    ]
    click_positions = [[(10, 550), (440, 650), (2300, 1300), (1720, 1250), (2300, 1300), (170, 350), (2300, 1300), (1720, 1250), (2300, 1300), (170, 350), (2300, 1300), (1720, 1250), (2300, 1300), (170, 350), (2300, 1300), (1720, 1250), (2300, 1300), (750, 520)]]
    for template_path, click_position in zip(templates, click_positions):
        positionClick(template_path, click_position, retry_limit=3, time_wait=0.8)
    # 关闭socket连接
    s.close()
    
    

def autoFight():
    template_path = "template/AutoFight/attack.png"
    # 读取 JSON 文件
    with open('skill_number_sequences.json', 'r') as f:
        skill_number_sequences = json.load(f)

    with open('skill_click.json', 'r') as f:
        skill_click = json.load(f)
        
        # 解析字符串为包含元组的列表
        skill_click = [[ast.literal_eval(item) for item in sublist] for sublist in skill_click]

    for i, skill_numbers in enumerate(skill_number_sequences):
        click_positions = generate_click_positions(skill_numbers, skill_click[i])
        positionClick(template_path, click_positions, retry_limit=100, time_wait=0.5)
        time.sleep(5)
    # 关闭socket连接
    s.close()

def autoKeChao():
    click_positions = [
            (340, 245), (525, 240), (707, 235), (335, 620), (505, 615), (660, 625), (450, 905), (670, 895), (885, 910),
            (1230, 890), (1320, 745), (1395, 700), (1235, 815), (1310, 860), (1910, 630), (2080, 625), (2250, 635),
            (1685, 920), (1900, 895), (2115, 900)
        ]  # 点击位置循环列表
    
    positionClick("template/AutoKeChao/startKeChao.jpg", [(1055, 1170)], retry_limit=3, time_wait=0.2)

    haveFound = False
    KeChaoEnd = False
    start_time = time.time()
    while not haveFound:
        capture_screen()
        img_rgb = cv2.imread('screenshot.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread("template/AutoKeChao/officialStart.jpg", 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            haveFound = True
            while not KeChaoEnd:
              for position in click_positions:
                click_position(position[0], position[1])
                capture_screen()
              if time.time() - start_time >= 50:
                img_rgb = cv2.imread('screenshot.jpg')
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

                template = cv2.imread("template/AutoKeChao/officialEnd.jpg", 0)
                w, h = template.shape[::-1]
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                loc = np.where(res >= threshold)
                if len(loc[0]) > 0:
                  KeChaoEnd = True

    # 关闭socket连接
    s.close()



