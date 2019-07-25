import pyautogui
import win32api
import win32con
import win32gui

a = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
QQWin = win32gui.FindWindow("TXGuiFoundation", "TIM")
aa = pyautogui.size()
print(aa)