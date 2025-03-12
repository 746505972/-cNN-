import mss
import cv2
import numpy as np
import time
import os
from PIL import Image, ImageDraw, ImageFont

# 截图区域
locate00 = {'left': 0 + 224, 'top': 896 + 60, 'width': 1840 - 224, 'height': 1080 - 896}
locate01 = {'left': 0 + 224, 'top': 896 + 60, 'width': 1840 - 224, 'height': 1080 - 896}
locate02 = {'left': 0 + 224, 'top': 896 + 60, 'width': 1840 - 224, 'height': 1080 - 896}
locate03 = {'left': 0 + 224, 'top': 896 + 60, 'width': 1840 - 224, 'height': 1080 - 896}
locate10 = {'left': 754, 'top': 598, 'width': 1140 - 754, 'height': 796 - 598}
locate11 = {'left': 1134, 'top': 344, 'width': 1498 - 1134, 'height': 590 - 344}
locate12 = {'left': 804, 'top': 174, 'width': 1128 - 804, 'height': 346 - 174}
locate13 = {'left': 422, 'top': 340, 'width': 775 - 422, 'height': 588 - 340}
# 设置截图保存路径
save_directory = "F:/GameScreenshots"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

with mss.mss() as sct:
    while True:
        hand0 = cv2.resize(np.asarray(sct.grab(locate00))[:, :, :3], (800, 90))
        river0 = cv2.resize(np.asarray(sct.grab(locate10))[:, :, :3], (200, 200))
        river1 = cv2.rotate(cv2.resize(np.asarray(sct.grab(locate11))[:, :, :3], (200, 200)), cv2.ROTATE_90_CLOCKWISE)
        river2 = cv2.rotate(cv2.resize(np.asarray(sct.grab(locate12))[:, :, :3], (200, 200)), cv2.ROTATE_180)
        river3 = cv2.rotate(cv2.resize(np.asarray(sct.grab(locate13))[:, :, :3], (200, 200)),
                            cv2.ROTATE_90_COUNTERCLOCKWISE)

        # 将牌河画面水平拼接在一起
        river = cv2.hconcat([river0, river1, river2, river3])
        # 创建一个白色矩形区域
        white_rect0 = np.ones((40, 800, 3), dtype=np.uint8) * 255  # 200是矩形宽度
        # 将 OpenCV 图像转换为 PIL 图像
        white_rect_pil = Image.fromarray(cv2.cvtColor(white_rect0, cv2.COLOR_BGR2RGB))
        # 在白色矩形上添加中文文本
        draw = ImageDraw.Draw(white_rect_pil)
        draw.text((0, 10), "我的牌河", font=ImageFont.truetype("simsun.ttc", 20), fill=(0, 0, 0))  # 黑色文本
        draw.text((200, 10), "下家牌河", font=ImageFont.truetype("simsun.ttc", 20), fill=(0, 0, 0))  # 黑色文本
        draw.text((400, 10), "对家牌河", font=ImageFont.truetype("simsun.ttc", 20), fill=(0, 0, 0))  # 黑色文本
        draw.text((600, 10), "上家牌河", font=ImageFont.truetype("simsun.ttc", 20), fill=(0, 0, 0))  # 黑色文本
        # 将 PIL 图像转换回 OpenCV 图像
        white_rect0 = cv2.cvtColor(np.array(white_rect_pil), cv2.COLOR_RGB2BGR)

        # 将截图和白色矩形拼接在一起
        river = cv2.vconcat([white_rect0, river])

        # 创建一个白色矩形区域
        white_rect = np.ones((40, 800, 3), dtype=np.uint8) * 255  # 200是矩形宽度
        # 将 OpenCV 图像转换为 PIL 图像
        white_rect_pil = Image.fromarray(cv2.cvtColor(white_rect, cv2.COLOR_BGR2RGB))
        # 在白色矩形上添加中文文本
        draw = ImageDraw.Draw(white_rect_pil)
        draw.text((0, 10), "我的手牌", font=ImageFont.truetype("simsun.ttc", 20), fill=(0, 0, 0))  # 黑色文本
        # 将 PIL 图像转换回 OpenCV 图像
        white_rect = cv2.cvtColor(np.array(white_rect_pil), cv2.COLOR_RGB2BGR)

        # 将截图和白色矩形拼接在一起
        combined_image = cv2.vconcat([cv2.vconcat([white_rect, hand0]), river])

        cv2.imshow("game", combined_image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):  # 按空格键退出
            break
        time.sleep(0.3)  # 休眠降低CPU占用

cv2.destroyAllWindows()
