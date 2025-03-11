import mss
import cv2
import numpy as np
import time
import os

# 截图区域
locate1 = {'left': 0, 'top': 60, 'width': 500, 'height': 600}
locate2 = {'left': 0 + 300, 'top': 60 + 600, 'width': 1000, 'height': 1000}
# 设置截图保存路径
save_directory = "F:/GameScreenshots"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

with mss.mss() as sct:
    while True:
        screenshot1 = sct.grab(locate1)
        screenshot1 = np.asarray(screenshot1)[:, :, :3]  # 提取 BGR 颜色通道
        screenshot2 = sct.grab(locate2)
        screenshot2 = np.asarray(screenshot2)[:, :, :3]  # 提取 BGR 颜色通道
        resized1 = cv2.resize(screenshot1, (locate1['width'] // 2, 300))  # 缩小图像
        resized2 = cv2.resize(screenshot2, (locate2['width'] // 2, 300))
        # 将两个图像水平拼接在一起
        combined_image = cv2.hconcat([resized1, resized2])
        cv2.imshow("game", combined_image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):  # 按空格键退出
            break
        time.sleep(0.3)  # 休眠降低CPU占用

cv2.destroyAllWindows()
