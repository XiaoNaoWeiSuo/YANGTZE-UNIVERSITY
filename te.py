import ctypes
import win32con
import win32api
import win32gui

# 定义快捷键的ID
HOTKEY_ID = 1

# 定义快捷键的组合（例如Ctrl+Shift+F）
MOD_KEY = win32con.MOD_CONTROL | win32con.MOD_SHIFT
VK_KEY = ord('F')

# 定义回调函数
def hotkey_callback(hwnd, msg, wparam, lparam):
    if wparam == HOTKEY_ID:
        # 使用ctypes调用ShellExecute函数打开WiFi和蓝牙控制菜单
        ctypes.windll.shell32.ShellExecuteW(None, 'open', 'ms-settings:', None, None, win32con.SW_SHOWNORMAL)

# 注册快捷键
# if not win32api.RegisterHotKey(None, HOTKEY_ID, MOD_KEY, VK_KEY):
#     print('注册快捷键失败')

# 获取消息循环所需的窗口句柄
hwnd = win32gui.GetForegroundWindow()

# 添加消息处理函数
win32gui.AddClipboardFormatListener(hwnd)
win32gui.PumpMessages()

# 注销快捷键
win32api.UnregisterHotKey(None, HOTKEY_ID)
