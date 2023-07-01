import os
import cv2
import time
import json
import ast
import numpy as np


# 使用ADB截取设备屏幕截图
def capture_screenshot():
  os.system("adb disconnect")
  os.system("adb devices")
  os.system("adb shell screencap -p /sdcard/screenshot.png")
  os.system("adb pull /sdcard/screenshot.png .")

# 点击指定位置
def click_position(x, y):
    os.system(f"adb shell input tap {x} {y}")


# 识别模板并点击指定位置
def positionClick(template_path, click_positions, retry_limit=3):
    retry_count = 0
    haveFound = False

    while retry_count < retry_limit and not haveFound:
        capture_screenshot()
        img_rgb = cv2.imread('screenshot.png')
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
                time.sleep(0.25)
        else:
            retry_count += 1

    if not haveFound:
        print("Template not found. Stopping execution.")


# 识别模板并点击模板中心位置（循环时会出现问题，暂时弃用）
def templateClick(template_path, retry_limit=3):
    retry_count = 0
    haveFound = False

    while retry_count < retry_limit and not haveFound:
       capture_screenshot()  # 在循环开始前获取最新的屏幕截图
       img_rgb = cv2.imread('screenshot.png')
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
              time.sleep(0.5)  # 在点击后进行延时
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
  img_rgb = cv2.imread('screenshot.png')
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
        "template/AutoExplore/SwitchToFinishedExplore.png",
        "template/AutoExplore/ClickFinishExplore.png",
        "template/AutoExplore/GetReward.png",
        "template/AutoExplore/SwitchToFinishedExplore.png",
        "template/AutoExplore/ClickFinishExplore.png",
        "template/AutoExplore/GetReward.png",
        "template/AutoExplore/SwitchToFinishedExplore.png",
        "template/AutoExplore/ClickFinishExplore.png",
        "template/AutoExplore/GetReward.png",
        "template/AutoExplore/clickGetTianGongStone.png"
    ]
    click_positions = [
      (10, 550),
      (440, 650),
      (2300, 1300),
      (1720, 1250),
      (170, 350)
    ]
    for template in templates, click_position in click_positions:
       positionClick(template, click_positions, retry_limit=3)
    
    

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
        positionClick(template_path, click_positions, retry_limit=100)
        time.sleep(10)