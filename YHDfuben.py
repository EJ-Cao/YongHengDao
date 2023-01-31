# coding = utf-8
# 永恒岛手游自动副本一条龙

import cv2 as cv
import numpy as np
import time
import os
import pyautogui
import logging
from datetime import datetime, timedelta
import sys
import re

logging.basicConfig(
    level = logging.INFO,
    # filename = 'log.txt',
    # filemode = 'w'
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

pyautogui.FAILSAFE = False

# 备用运行
##schedule.every().day.at("15:52").do(job)
##while 1:
##    schedule.run_pending()
##    time.sleep(1)


# 自定义报错

class NoBottomFoundException(Exception):
    pass

class ExceedsRetryTimes(Exception):
    pass


# 进入副本与返回城镇相关按钮

bottom_1 = 'screenshot/bottom1.PNG'
bottom_2 = 'screenshot/bottom2.PNG'
bottom_3 = 'screenshot/bottom3.PNG'
guaiwu = 'screenshot/guaiwu.PNG'
enter = 'screenshot/enter.PNG'
close_0 = 'screenshot/close0.PNG'
close_1 = 'screenshot/close1.PNG'
close_2 = 'screenshot/close2.PNG'
finsihed = 'screenshot/finished.PNG'

ptdrag = 'screenshot/ptdrag.PNG'
ptfuben = 'screenshot/ptfb.PNG'
tzdrag = 'screenshot/tzdrag.PNG'
tzfuben = 'screenshot/tzfb.PNG'
emdrag = 'screenshot/emdrag.PNG'
emfuben = 'screenshot/emfb.PNG'


# 所有将要被运行副本的名字
# 100级以前一共10个

img_list = os.listdir('screenshot')
allfuben = img_list[:9]
logging.info(allfuben)
putong = img_list[1:9]
logging.info(putong)

# 定义方程

def FindBottom(img_path):
    """
    在屏幕上寻找要点击的按钮

    :param img_path: 按钮图片
    :return: 按钮坐标
    """

    time.sleep(0.5)
    location = pyautogui.locateOnScreen(img_path, confidence=0.78)
    if location is not None:
        return location
    else:
        raise NoBottomFoundException

def ClickBottom(img_path):
    """
    点击找到的按钮
    如果没有找到按钮，将持续寻找直至按钮出现
    并确保每个按钮都已经被成功点击，且从屏幕上消失

    :param img_path: 按钮图片
    """
    def _ClickBottom(img_path):
        location = FindBottom(img_path)
        left, top, width, height = location
        center = pyautogui.center((left, top, width, height))
        pyautogui.click(center)
        
    logging.info(f"{img_path} trying")
    while True:
        try:
            _ClickBottom(img_path)
        except NoBottomFoundException:
            continue
        else:
            try: 
                _ClickBottom(img_path)
                return
            except NoBottomFoundException:      
                logging.info(f"{img_path} successful")
                return

def ClickEnter(img_path = enter):
    """
    点击“进入副本”按钮

    :param img_path: “进入副本”按钮图片
    """
    def _ClickEnter(img_path):
        location = FindBottom(img_path)
        left, top, width, height = location
        center = pyautogui.center((left, top, width, height))
        pyautogui.click(center)
    logging.info(f"{img_path} trying")
    while True:
        try:
            _ClickEnter(img_path)
        except NoBottomFoundException:
            continue
        else:
            logging.info(f"{img_path} successful")
            return

def Drag(img_path):
    """
    向下拖动两次副本列表（本脚本中未被使用）
    
    :param img_path: 定位拖动起始坐标
    """
    def _Drag(img_path):
        location = FindBottom(img_path)
        left, top, width, height = location
        center = pyautogui.center((left, top, width, height))
        x, y = center
        pyautogui.click(x, y+100, clicks=1, duration=0.2)
        pyautogui.dragRel(0, 200, duration=0.5)
        pyautogui.moveTo(x, y+90, duration=0.2)  
        pyautogui.dragRel(0, 200, duration=0.5)
    logging.info(f"{img_path} trying")
    while True:
        try:
            _Drag(img_path)
        except NoBottomFoundException:
            continue
        else:
            logging.info(f"{img_path} successful")
            return

def DragDown(img_path):
    def _DragDown(img_path):
        location = FindBottom(img_path)
        left, top, width, height = location
        center = pyautogui.center((left, top, width, height))
        x, y = center
        pyautogui.click(x, y+100, clicks=1, duration=0.2)
        pyautogui.dragRel(0, 300, duration=0.5)
        pyautogui.moveTo(x, y+90, duration=0.2)  
        pyautogui.dragRel(0, 300, duration=0.5)
    logging.info(f"{img_path} trying")
    while True:
        try:
            _DragDown(img_path)
        except NoBottomFoundException:
            continue
        else:
            logging.info(f"{img_path} successful")
            return

def DragUp(img_path):
    def _DragUp(img_path):
        location = FindBottom(img_path)
        left, top, width, height = location
        center = pyautogui.center((left, top, width, height))
        x, y = center
        pyautogui.click(x, y+400, clicks=1, duration=0.2)
        pyautogui.dragRel(0, -300, duration=0.5)
        pyautogui.moveTo(x, y+390, duration=0.2)  
        pyautogui.dragRel(0, -300, duration=0.5)
    logging.info(f"{img_path} trying")
    while True:
        try:
            _DragUp(img_path)
        except NoBottomFoundException:
            continue
        else:
            logging.info(f"{img_path} successful")
            return
            
def FindFuben(img_path, drag_path):
    try:
        return FindBottom(img_path)
    except NoBottomFoundException:
        DragDown(drag_path)
        try:
            return FindBottom(img_path)
        except NoBottomFoundException:
            DragUp(drag_path)
            return FindBottom(img_path)

def FubenBottom(img_path, drag_path):
    location = FindFuben(img_path, drag_path)
    left, top, width, height = location
    center = pyautogui.center((left, top, width, height))
    pyautogui.doubleClick(center)
    
def Fuben(num, fuben_num, fuben_kind, drag_path):
    """
    运行所有副本指定次数

    :param num: 每个副本运行次数
    :param fuben_num: 需要运行的副本（蛇龙、鬼怪……）
    :param fuben_kind: 副本种类（普通、挑战、噩梦）
    :param drag_path: 定位拖动起始坐标
    """
    for i in fuben_num:
        for j in range(1,num+1):
            fuben_path = f'screenshot/{i}'
            logging.info(f"**********{fuben_path} Started**********")
            ClickBottom(bottom_1)
            ClickBottom(bottom_2)

            # 错误点击怪物大厦
            try:
                if FindBottom(guaiwu):
                    #ClickBottom(close_1)
                    ClickBottom(close_1)
                    ClickBottom(bottom_3)
                    break
            except:
                ClickBottom(fuben_kind)

            FubenBottom(fuben_path, drag_path)
            ClickEnter() #副本
            time.sleep(1)
            
            try:
                if FindBottom(drag_path):
                    #ClickBottom(close_1)
                    ClickBottom(close_1)
                    ClickBottom(bottom_3)
                    break
            except:
                logging.info(f'进入{i}副本，第{j}次')
        
            # 打副本
            time.sleep(15)

            ClickBottom(close_0)
            time.sleep(1)
            try:
                if FindBottom(close_2):
                    ClickBottom(close_2)
                    time.sleep(0.5)
                    ClickBottom(finsihed)
            except:
                ClickBottom(finsihed)
            logging.info('副本已关闭')
            time.sleep(1)
            logging.info(f'**********{fuben_path} Finished**********')        
        else:
            continue

def job():
    """
    每日副本一条所有任务
    普通、挑战副本各三次
    噩梦副本一次
    
    """
    #Fuben(3, allfuben, tzfuben, tzdrag)
    #Fuben(1, allfuben, emfuben, emdrag)
    Fuben(3, allfuben, ptfuben, ptdrag)


# 设定自动运行时间

now = datetime.now()

if now.hour > 5:
    start_day = datetime.now().date()+ timedelta(days=1)
    start_time = datetime(start_day.year, \
                        start_day.month, start_day.day, 5, 15)
else:
    start_time = datetime(now.year, now.month, now.day, 5, 15)

diff = start_time - now
logging.info(diff.seconds)


# 运行

#time.sleep(diff.seconds)
try:
    if FindBottom(bottom_3):
        ClickBottom(bottom_3)
        time.sleep(0.5)
        job()
except:
    job()
