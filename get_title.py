# 2025/3/9 15:59
import mss
import cv2
import numpy as np
import time
import os

# 截图区域
locate = {'left': 0 + 224, 'top': 896 + 60, 'width': 1840 - 224, 'height': 1080 - 896}

# 设置截图保存路径
save_directory = "F:/GameScreenshots"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)


def is_card(window):
    # 判断背景是否为白色
    mean_color = np.mean(window, axis=(0, 1))  # 计算平均颜色
    is_white_background = np.all(mean_color > [200, 200, 200])  # 接近白色

    # 检测边缘颜色突变
    gray = cv2.cvtColor(window, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)  # Canny边缘检测
    edge_intensity = np.mean(edges)  # 计算边缘强度

    # 判断是否为牌
    return is_white_background and edge_intensity > 10  # 调整阈值


with mss.mss() as sct:
    while True:
        screenshot = sct.grab(locate)
        screenshot = np.asarray(screenshot)[:, :, :3]  # 提取 BGR 颜色通道
        window_w, window_h = 90, 130  # 根据手牌大小调整

        # 用于保存检测到的牌
        cards = []

        # 滑动窗口扫描
        for y in range(0, screenshot.shape[0] - window_h, window_h // 2):  # 步长为窗口高度的一半
            for x in range(0, screenshot.shape[1] - window_w, window_w // 2):
                # 提取窗口图像
                window = screenshot[y:y + window_h, x:x + window_w]

                # 判断是否包含手牌
                if is_card(window):
                    cards.append(window)

        # 如果检测到牌，将它们水平拼接在一起
        if cards:
            combined_image = cv2.hconcat(cards)
            cv2.imshow("Cards", combined_image)

        # 显示原始截图
        cv2.imshow("Game Screenshot", screenshot)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):  # 按空格键退出
            break
        elif key == ord("1"):  # 按 "1" 键保存截图
            timestamp = time.strftime("%Y%m%d_%H%M%S")  # 生成时间戳
            file_path = os.path.join(save_directory, f"screenshot_{timestamp}.png")
            cv2.imwrite(file_path, screenshot)
            print(f"截图已保存: {file_path}")

        time.sleep(0.3)  # 休眠降低CPU占用

cv2.destroyAllWindows()

