import os
import cv2
import time
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
                time.sleep(1)
        else:
            retry_count += 1

    if not haveFound:
        print("Template not found. Stopping execution.")


# 识别模板并点击模板中心位置
def templateClick(template_path, retry_limit=3):
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
            for pt in zip(*loc[::-1]):
                # 计算模板中心位置
                center_x = pt[0] + w // 2
                center_y = pt[1] + h // 2
                click_position(center_x, center_y)
                time.sleep(1)
        else:
            capture_screenshot()
            retry_count += 1

    if not haveFound:
        print("Template not found. Stopping execution.")

# 自动战斗技能点击坐标生成
def generate_click_positions(skill_numbers):
    #positions
    #Char1: 630, 1250
    #Char2: 1270, 1250
    #Char3: 1510, 1250
    #Char4: 1950, 1250
    #S1: 830, 1050
    #S2: 1330, 1050
    #S3: 1830, 1050
    char_positions = [(630, 1250), (1270, 1250), (1510, 1250), (1950, 1250)]
    skill_positions = [(830, 1050), (1330, 1050), (1830, 1050)]
    
    click_positions = []
    num_chars = len(char_positions)
    num_skills = len(skill_positions)
    
    for i, skill_number in enumerate(skill_numbers):
        char_index = i % num_chars
        skill_index = (skill_number - 1) % num_skills
        click_positions.append((char_positions[char_index][0], char_positions[char_index][1]))
        click_positions.append((skill_positions[skill_index][0], skill_positions[skill_index][1]))
    
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

    for template in templates:
      templateClick(template, retry_limit=3)

def autoFight():
    template_path = "template/AutoFight/attack.png"
    skill_number_sequences = [[2, 1, 1, 3], [1, 1, 1, 2]]

    for skill_numbers in skill_number_sequences:
        click_positions = generate_click_positions(skill_numbers)
        positionClick(template_path, click_positions, retry_limit=3)
        templateClick(template_path, retry_limit=3)