"""
用1920*1080窗口打开游戏并放在左上角，最好像素级对其，即窗口左上角放在（0，0）
按“1”截屏，在截屏前要先点一下监视窗口
按空格关闭，同样要先点一下监视窗口
"""

import mss
import cv2
import numpy as np
import time
import os

# 截图区域
locate = {'left': 0, 'top': 60, 'width': 1920, 'height': 1080}

# 设置截图保存路径
save_directory = "F:/GameScreenshots"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

with mss.mss() as sct:
    while True:
        screenshot = sct.grab(locate)
        screenshot = np.asarray(screenshot)[:, :, :3]  # 提取 BGR 颜色通道
        resized = cv2.resize(screenshot, (800, 450))  # 缩小图像
        cv2.imshow("game", resized)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):  # 按空格键退出
            break
        elif key == ord("1"):  # 按 "S" 键保存截图
            timestamp = time.strftime("%Y%m%d_%H%M%S")  # 生成时间戳
            file_path = os.path.join(save_directory, f"screenshot_{timestamp}.png")
            cv2.imwrite(file_path, screenshot)
            print(f"截图已保存: {file_path}")

        time.sleep(0.3)  # 休眠降低CPU占用

cv2.destroyAllWindows()
