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

# 第一张牌的区域
locate = {'left': 224, 'top': 936 + 60, 'width': 88, 'height': 1066 - 936}

# 设置截图保存路径
save_directory = "F:/GameScreenshots"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

with mss.mss() as sct:
    while True:
        # 用于保存所有牌
        cards = []

        # 捕获 13 张牌
        for i in range(13):
            # 计算当前牌的区域
            card_locate = {
                'left': locate['left'] + i * 95,  # 每张牌相差 3 个像素
                'top': locate['top'],
                'width': locate['width'],
                'height': locate['height']
            }
            # 捕获当前牌
            card = sct.grab(card_locate)
            card = np.asarray(card)[:, :, :3]  # 提取 BGR 颜色通道
            cards.append(card)

        # 将 13 张牌水平拼接在一起
        combined_image = cv2.hconcat(cards)

        # 显示拼接后的图像
        cv2.imshow("13 Cards", combined_image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):  # 按空格键退出
            break
        elif key == ord("1"):  # 按 "1" 键保存截图
            timestamp = time.strftime("%m%d_%H%M")  # 生成时间戳
            for idx, card in enumerate(cards):
                file_path = os.path.join(save_directory, f"c_{idx + 1}_{timestamp}.png")
                cv2.imwrite(file_path, card)
                print(f"牌 {idx + 1} 已保存: {file_path}")

        time.sleep(0.3)  # 休眠降低CPU占用

cv2.destroyAllWindows()
