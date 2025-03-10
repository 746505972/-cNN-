# 2025/3/9 15:59
import pyautogui
import time

print("请在 5 秒内将鼠标放到窗口左上角...")
time.sleep(5)  # 等待 5 秒
print("鼠标当前位置：", pyautogui.position())  # 获取鼠标位置

