import ctypes
import time
import sys
import subprocess
import json
import os
import pynput
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        os.path.abspath(__file__),
        None,
        1,
    )
    sys.exit()
print(ctypes.windll.shell32.IsUserAnAdmin())

mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
left = pynput.mouse.Button.left
right = pynput.mouse.Button.right

FPSinput = 120
keyinput = "caps_lock"

# ── Config file (giao tiếp với frontend) ────────────────────────────────────
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
DEFAULT_CONFIG = {
    "combo": "22q223 223 22cd23 25",
    "bind_key": keyinput
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# NỘI SUY FPS => ĐỘ TRỄ
# T_FPS = [
#         [
#             30,
#             60,
#             100,
#             120,
#             220],
#         [
#             1.5,
#             1.366,
#             1.34,
#             1.32,
#             1.285]]
def fps2t(T_FPS, fps): #T_FPS: array, fps: float
    """
    Truy xuất giá trị t tương ứng từ bảng FPS bằng nội suy tuyến tính.

    Parameters
    ----------
    T_FPS : list[list]
        [
            [fps1, fps2, fps3, ...],
            [t1,   t2,   t3,   ...]
        ]

    fps : float

    Returns
    -------
    float
    """

    fps_values = T_FPS[0]
    t_values = T_FPS[1]

    # FPS lớn hơn giá trị lớn nhất
    if fps >= fps_values[-1]:
        return t_values[-1]

    # FPS nhỏ hơn giá trị nhỏ nhất
    if fps <= fps_values[0]:
        print("Tốc độ khung hình quá thấp để hỗ trợ")
        return t_values[0]

    # tìm đoạn chứa fps
    for i in range(len(fps_values) - 1):

        if fps_values[i] <= fps <= fps_values[i + 1]:

            fps1 = fps_values[i]
            fps2 = fps_values[i + 1]

            t1 = t_values[i]
            t2 = t_values[i + 1]

            weight = (fps - fps1) / (fps2 - fps1)

            return t1 + (t2 - t1) * weight

    # fallback
    return t_values[0]

#n3w
def skk3aw(fps):
    start = time.perf_counter()

    for _ in range(int(0.6 * fps)):
        if time.perf_counter() - start > 0.6:
            break

        mouse.press(left)
        mouse.release(left)
        time.sleep(2 / fps)

    keyboard.press("w")

    T_FPS = [
        [30, 60, 100, 120, 220],
        [1.5, 1.366, 1.34, 1.32, 1.285]
    ]

    t = fps2t(T_FPS, fps)

    while time.perf_counter() - start < t:
        pass

    keyboard.release("w")

#n2d
def skk2as(fps):
    start = time.perf_counter()

    for _ in range(int(0.26 * fps)):
        if time.perf_counter() - start > 0.32:
            break

        mouse.press(left)
        mouse.release(left)
        time.sleep(2 / fps)

    t = fps2t([
        [60, 120, 220],
        [0.44, 0.40, 0.37]
    ], fps)

    while time.perf_counter() - start < t:
        pass

    mouse.press(right)
    time.sleep(1 / fps)
    mouse.release(right)

    time.sleep(1 / (1.2*fps))

    t = fps2t([
        [60, 120, 220],
        [0.63, 0.57, 0.56]
    ], fps)

    while time.perf_counter() - start < t:
        pass

#n2c
def skk2az(fps):

    start = time.perf_counter()

    t = fps2t([
        [60,120,220],
        [0.24,0.22,0.20]
    ], fps)

    for _ in range(int(0.2 * fps)):
        if time.perf_counter() - start > t:
            break

        mouse.press(left)
        mouse.release(left)
        time.sleep(2 / fps)

    while time.perf_counter() - start < t + 2 / fps:
        pass

    mouse.press(left)
    time.sleep(0.44)
    mouse.release(left)

    t = fps2t([
        [60,120,220],
        [1.16,1.12,1.09]
    ], fps)

    while time.perf_counter() - start < t:
        pass

def skk2azs(fps):
    start = time.perf_counter()
    T_FPS = [
        [
            60,
            120,
            220],
        [
            0.24,
            0.22,
            0.2]]
    t = fps2t(T_FPS, fps)
    for _ in range(int(0.2 * fps)):
        if time.perf_counter() - start > t:
            break
        mouse.press(left)
        mouse.release(left)
        time.sleep(2 / fps)
    while time.perf_counter() - start < t + 2 / fps:
        pass
    mouse.press(left)
    time.sleep(0.44)
    mouse.release(left)
    time.sleep(1 / fps)
    mouse.press(right)
    time.sleep(1 / fps)
    mouse.release(right)
    time.sleep(1 / fps)
    keyboard.press('w')
    time.sleep(1 / fps)
    keyboard.release('w')
    time.sleep(1 / fps)
    T_FPS = [
        [
            60,
            120,
            220],
        [
            0.9,
            0.86,
            0.82]]
    t = fps2t(T_FPS, fps)
    while time.perf_counter() - start < t:
        pass
    return None



def skk2azs_slow(fps):
    if fps < 105:
        skk2azs(fps)
        return None
    start = time.perf_counter()
    for _ in range(int(0.2 * fps)):
        if time.perf_counter() - start > 0.26:
            break
        mouse.press(left)
        mouse.release(left)
        time.sleep(2 / fps)
    while time.perf_counter() - start < 0.28:
        pass
    mouse.press(left)
    time.sleep(0.44)
    mouse.release(left)
    time.sleep(1 / fps)
    while time.perf_counter() - start < 0.725:
        pass
    mouse.press(right)
    time.sleep(1 / fps)
    mouse.release(right)
    time.sleep(1 / fps)
    keyboard.press('w')
    time.sleep(1 / fps)
    keyboard.release('w')
    time.sleep(1 / fps)
    while time.perf_counter() - start < 0.87:
        pass
    return None

def skk5as(fps):
    start = time.perf_counter()
    for _ in range(int(2 * fps)):
        if time.perf_counter() - start > 2.1:
            break
        mouse.press(left)
        mouse.release(left)
        time.sleep(2 / fps)
    T_FPS = [
        [
            60,
            120,
            220],
        [
            2.22,
            2.14,
            2.12]]
    t = fps2t(T_FPS, fps)
    while time.perf_counter() - start < t + 2 / fps:
        pass
    
    T_FPS = [
        [
            60,
            120,
            220],
        [
            2.41,
            2.28,
            2.24]]
    t = fps2t(T_FPS, fps)
    while time.perf_counter() - start < t + 2 / fps:
        pass
    return None

#n2q
def skk2aq(fps):
    start = time.perf_counter()

    # Spam click chuột trái
    for _ in range(int(0.26 * fps)):
        if time.perf_counter() - start > 0.32:
            break

        mouse.press(left)
        mouse.release(left)
        time.sleep(2 / fps)

    # Đợi đến mốc đầu tiên
    T_FPS = [
        [60, 120, 220],
        [0.44, 0.39, 0.37]
    ]

    t = fps2t(T_FPS, fps)

    while time.perf_counter() - start < t:
        pass

    # Bấm Q đúng 1 frame
    keyboard.press("q")
    time.sleep(1 / fps)
    keyboard.release("q")

    time.sleep(1 / fps)

    # Đợi đến mốc kết thúc
    T_FPS = [
        [60, 120, 220],
        [1.17, 1.09, 1.07]
    ]

    t = fps2t(T_FPS, fps)

    while time.perf_counter() - start < t:
        pass

def is_no_key_pressed():
    return target not in pressed

def skke(fps):
    start = time.perf_counter()
    for _ in range(int(0.1 * fps)):
        if time.perf_counter() - start > 0.1:
            break
        keyboard.press('e')
        time.sleep(1 / fps)
        keyboard.release('e')
        time.sleep(1 / fps)
    time.sleep(0.19)

#BLOCK 223
def skk223_loop(fps):

    start = time.perf_counter()

    while time.perf_counter() - start < 20:

        skk2as(fps)
        skk2as(fps)
        skk3aw(fps)

        if is_no_key_pressed():
            break

def skk0eqa_223_225(fps):
    skke(fps)
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2aq(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2azs_slow(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk5as(fps)

def skk0eqa_main(fps):
    skke(fps)
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2aq(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2az(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)

def skk0qea(fps):
    skke(fps)
    if is_no_key_pressed():
        return None
    skk2azs(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2azs_slow(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)

# ── Combo map: chuỗi frontend → hàm Python ──────────────────────────────────
COMBO_MAP = {
    "22q223 223 22cd23 25":        skk0eqa_223_225,
    "222q 223 223 22c3 223 3":     skk0eqa_main,
    "qe 2cd23 223 223 2cd23 222":  skk0qea,
}

active_combo_fn = skk0eqa_223_225  # mặc định, sẽ cập nhật từ config

#Xử lý code chạy macro
from pynput import keyboard as kb
from pynput import mouse as ms
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button

pressed = set()
running = False

def parse_input(name):
    if hasattr(Button, name):
        return getattr(Button, name)
    if hasattr(Key, name):
        return getattr(Key, name)
    if len(name) == 1:
        return KeyCode.from_char(name.lower())
    raise ValueError(f"Unknown key: {name}")

# ── apply_config: cập nhật target + active_combo_fn ─────────────────────────
def apply_config(cfg):
    global target, active_combo_fn
    target = parse_input(cfg.get("bind_key", keyinput))
    active_combo_fn = COMBO_MAP.get(cfg.get("combo"), skk0eqa_223_225)

# ── HTTP Server để nhận config từ frontend ────────────────────────────────────
class ConfigHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/save":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length))
                save_config(body)
                apply_config(body)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b'{"ok": true}')
            except Exception:
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, *args):
        pass

def start_http_server():
    server = HTTPServer(("localhost", 5000), ConfigHandler)
    server.serve_forever()

# ── Khởi tạo target + active_combo_fn từ config (mục 1 — đã được phép) ───────
_cfg = load_config()
active_combo_fn = COMBO_MAP.get(_cfg.get("combo"), skk0eqa_223_225)
target = parse_input(_cfg.get("bind_key", keyinput))

def worker():
    global running
    while running:
        active_combo_fn(FPSinput)  # mục 2 — đã được phép

def on_press(key):
    global running
    pressed.add(key)
    if target in pressed and not running:
        running = True
        threading.Thread(target=worker, daemon=True).start()

def on_release(key):
    global running
    pressed.discard(key)
    if target not in pressed:
        running = False

def on_click(x, y, button, is_pressed):
    global running
    if is_pressed:
        pressed.add(button)
        if target in pressed and not running:
            running = True
            threading.Thread(target=worker, daemon=True).start()
    else:
        pressed.discard(button)
        if target not in pressed:
            running = False

kb.Listener(on_press=on_press,on_release=on_release).start()
ms.Listener(on_click=on_click).start()

threading.Thread(target=start_http_server, daemon=True).start()
threading.Event().wait()
