import win32gui
import win32con
import ctypes
import random
import time
import math
import webbrowser  # 用於打開網頁
import threading   # 用於多線程，防止彈窗卡死主程式

# 1. 初始化與環境設定
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
user32.SetProcessDPIAware() 
sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# MessageBox 常數設定
MB_OKCANCEL = 0x00000001
MB_ICONWARNING = 0x00000030
WH_CBT = 5
HCBT_ACTIVATE = 5

# 經典 MEMZ 迷因網址清單（可自行擴充）
MEME_URLS = [
    "https://www.google.com/search?q=how+to+remove+a+virus",
    "https://www.google.com/search?q=my+computer+is+melting",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ", # Rickroll
    "https://www.spacejam.com/1996/",
    "https://itscoops.com/"
]

# 隨機訊息框的文字庫
MSG_POOL = [
    ("lol", "Still Using This Computer?"),
    ("Credits", "Dark Army Presents"),
    ("LOL", "Clicking OK may cause system became unbootable"),
    ("Windows授權已過期", "更新您的授權")
]

# --- 獨立功能 1: 隨機位置訊息框 (使用獨立執行緒) ---
def spawn_random_box():
    hook_id = 0
    title, text = random.choice(MSG_POOL)

    def hook_callback(nCode, wParam, lParam):
        if nCode == HCBT_ACTIVATE:
            # 隨機產生座標
            rx = random.randint(0, max(0, sw - 300))
            ry = random.randint(0, max(0, sh - 150))
            user32.SetWindowPos(wParam, 0, rx, ry, 0, 0, 0x0001 | 0x0040)
            user32.UnhookWindowsHookEx(hook_id)
        return user32.CallNextHookEx(hook_id, nCode, wParam, lParam)

    CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    callback_ptr = CMPFUNC(hook_callback)
    hook_id = user32.SetWindowsHookExW(WH_CBT, callback_ptr, 0, kernel32.GetCurrentThreadId())
    user32.MessageBoxW(0, text, title, MB_OKCANCEL | MB_ICONWARNING)

# --- 獨立功能 2: 隨機打開網頁 (使用獨立執行緒) ---
def open_random_url():
    url = random.choice(MEME_URLS)
    webbrowser.open(url)

# --- 主程式核心迴圈 ---
def run_ultimate_memz():
    icon_warning = user32.LoadIconW(0, win32con.IDI_WARNING)
    icon_error = user32.LoadIconW(0, win32con.IDI_ERROR)
    angle = 0
    
    try:
        while True:
            # 獲取安全 DC
            hdc = win32gui.GetDC(0)
            if not hdc:
                time.sleep(0.01)
                continue

            try:
                # 1. 垂直位移 (gdi.py)
                x_pos = random.randint(0, sw)
                win32gui.BitBlt(hdc, x_pos, random.randint(-3, 3), 10, sh, hdc, x_pos, 0, win32con.SRCCOPY)
                
                # 2. 隧道效果 (tunnel.py)
                slow_size = 6
                win32gui.StretchBlt(hdc, int(slow_size/2), int(slow_size/2), sw-slow_size, sh-slow_size, hdc, 0, 0, sw, sh, win32con.SRCCOPY)

                # 3. 隨機圖示
                if random.random() < 0.12:
                    rx = random.randint(0, sw)
                    ry = random.randint(0, sh)
                    chosen_icon = icon_warning if random.random() < 0.5 else icon_error
                    user32.DrawIcon(hdc, rx, ry, chosen_icon)

                # 4. 顏色反轉 (invertcolors.py)
                if random.random() < 0.01:
                    win32gui.InvertRect(hdc, (0, 0, sw, sh))

            except:
                pass
            finally:
                win32gui.ReleaseDC(0, hdc)

            # 5. 滑鼠抖動
            try:
                if random.random() < 0.25:
                    mx, my = user32.GetCursorPos()
                    angle += 0.5
                    nx = max(0, min(sw, mx + int(math.sin(angle) * 15) + random.randint(-5, 5)))
                    ny = max(0, min(sh, my + int(math.cos(angle) * 15) + random.randint(-5, 5)))
                    user32.SetCursorPos(nx, ny)
            except:
                pass

            # 6. 【新增】隨機播放 Windows 錯誤聲音
            if random.random() < 0.04: # 4% 機率
                # 0x10 = 紅色錯誤音, 0x30 = 黃色警告音, 0x40 = 提示音
                sound_type = random.choice([0x10, 0x30, 0x40])
                user32.MessageBeep(sound_type)

            # 7. 【新增】隨機彈出訊息框 (透過 Thread 避免卡死)
            if random.random() < 0.005: # 約 0.5% 機率，不要設太高否則彈窗點不完
                t = threading.Thread(target=spawn_random_box)
                t.daemon = True # 設定為守護線程，主程式關閉時隨之關閉
                t.start()

            # 8. 【新增】隨機打開網頁 (透過 Thread 避免卡死)
            if random.random() < 0.003: # 約 0.3% 機率
                t = threading.Thread(target=open_random_url)
                t.daemon = True
                t.start()

            time.sleep(0.04)

    except KeyboardInterrupt:
        print("\n程式已手動停止。")

if __name__ == "__main__":
    run_ultimate_memz()
