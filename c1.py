__author__ = 'ChthollyNotaSenioriouss'

from selenium import webdriver
import numpy as np
import cv2
import base64
from selenium.webdriver import ActionChains
from c3 import get_vibrator_track, time_sleep_random
import random
import configparser

cf = configparser.ConfigParser()
cf.read('./config.ini')

driver = webdriver.Chrome(executable_path=cf['asd']['driver_path'])
driver.get("https://passport.bilibili.com/login")
driver.find_element_by_id("login-username").send_keys(
    cf['asd']['username'])
driver.find_element_by_id("login-passwd").send_keys(cf['asd']['passwd'])
driver.find_element_by_class_name("btn-login").click()
time_sleep_random()

# 下载缺口背景
JS = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
im_info = driver.execute_script(JS)
im_base64 = im_info.split(",")[1]
im_bytes = base64.b64decode(im_base64)
nparr = np.frombuffer(im_bytes, np.uint8)
bg_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# 下载滑块图
JS = 'return document.getElementsByClassName("geetest_canvas_slice geetest_absolute")[0].toDataURL("image/png");'
im_info = driver.execute_script(JS)
im_base64 = im_info.split(",")[1]
im_bytes = base64.b64decode(im_base64)
nparr = np.frombuffer(im_bytes, np.uint8)
slider_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# 处理滑块图
# 去阴影
for x in range(slider_img.shape[0]):
    for y in range(slider_img.shape[1]):
        if slider_img[x, y][0] == slider_img[x, y][1] == slider_img[x, y][2]:
            slider_img[x, y] = [0, 0, 0]
slider_img_gray = cv2.cvtColor(slider_img, cv2.COLOR_BGR2GRAY)

for i in range(slider_img_gray.shape[0]):
    right_vertex_x = 0
    controller = 0
    color_count = 0
    left_blank_count = 0
    for j in range(slider_img_gray.shape[1]):
        if slider_img_gray[i][j]:
            controller = 1
            color_count += 1
            right_vertex_x += 1
            if not left_blank_count:
                left_blank_count = right_vertex_x - 1
            continue
        if controller:
            break
        right_vertex_x += 1
    if controller:
        # 过滤圆角
        if color_count > 30:
            break
# 右顶点x坐标
right_vertex_x = right_vertex_x - 1

y_list = []
for y in range(slider_img_gray.shape[0]):
    if slider_img_gray[y][right_vertex_x]:
        y_list.append(y)
# 右顶点y坐标，右底点y坐标
right_vertex_y = y_list[0]
right_bottom_y = y_list[-1]

# 处理缺口图
i_count = 0
diff_list = []
for i in range(bg_img.shape[1]):
    i_col = [bg_img[x, i] for x in range(right_vertex_y, right_bottom_y + 1)]
    if i_count == 0:
        arr_mean = np.mean(i_col)
        diff_list.append(0)
    else:
        arr_mean2 = np.mean(i_col)
        diff_list.append(round(arr_mean2 - arr_mean, 2))
        arr_mean = arr_mean2
    i_count += 1
# 缺口右边界x坐标
right_border_x = diff_list.index(max(diff_list)) - 1

# 移动距离
distance = right_border_x - right_vertex_x # - left_blank_count

slider = driver.find_element_by_class_name("geetest_slider_button")
ActionChains(driver).click_and_hold(slider).perform()
time_sleep_random()
vibrator_track = get_vibrator_track(distance)
# for x in vibrator_track:
#     ActionChains(driver).move_by_offset()
#     ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
ActionChains(driver).move_by_offset(xoffset=distance,yoffset=0).perform()
time_sleep_random()
ActionChains(driver).release().perform()
