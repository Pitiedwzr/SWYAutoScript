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
def positionClick(template_path, click_x, click_y, retry_limit=3):
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
            click_position(click_x, click_y)
        else:
            capture_screenshot()
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
        else:
            capture_screenshot()
            retry_count += 1

    if not haveFound:
        print("Template not found. Stopping execution.")

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