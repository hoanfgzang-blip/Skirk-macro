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

keyinput = "caps_lock"

# ── Config file (giao tiếp với frontend) ────────────────────────────────────
if getattr(sys, 'frozen', False):
    CONFIG_PATH = os.path.join(os.path.dirname(sys.executable), "config.json")
else:
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULT_CONFIG = {
    "comboSignKeys": {}
}

FPSinput = 120

def load_config():
    global FPSinput
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
                FPSinput = int(config.get("FPS", 120))
                return config
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

    time.sleep(1 / fps)

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
    key = getattr(_thread_local, "bind_key", None)
    if key is None:
        return True
    return not any(key == k for k in pressed)

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
    log_debug(f"Macro running with FPS: {fps}")
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
    log_debug(f"Macro running with FPS: {FPSinput}")
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
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk2as(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)
    if is_no_key_pressed():
        return None
    skk3aw(fps)

def skk0qea(fps):
    log_debug(f"Macro running with FPS: {FPSinput}")
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
    if is_no_key_pressed():
        return None
    skk3aw(fps)

def skk0e2aq(fps):
    log_debug(f"Macro running with FPS: {FPSinput}")
    skke(fps)
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
    skk2azs(fps)
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
    skk2as(fps)


# ── Combo map: chuỗi frontend → hàm Python ──────────────────────────────────
COMBO_MAP = {
    "Combo gảy chan" : skk0e2aq,
    "C0:22q223 223 22cd23 25":        skk0eqa_223_225,
    "C0:222q 223 223 22c3 223 3":     skk0eqa_main,
    "C0:qe 2cd23 223 223 2cd23 222":  skk0qea,
}

run_enabled     = False          # Run button toggle
active_bindings = {}             # { pynput_key: combo_fn }
running_states  = {}             # { pynput_key: bool }
_thread_local   = threading.local()

#Xử lý code chạy macro
from pynput import keyboard as kb
from pynput import mouse as ms
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button

pressed = set()

# ── Logging để debug ──────────────────────────────────────────────────────────
DEBUG_LOG_PATH = os.path.join(os.path.dirname(CONFIG_PATH), "debug.log")

def log_debug(msg):
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {msg}\n")
    except Exception:
        pass

def parse_input(name):
    log_debug(f"parse_input: {name}")
    if name == "mouse_4":
        return Button.x2
    if name == "mouse_3":
        return Button.x1

    if hasattr(Button, name):
        return getattr(Button, name)

    if hasattr(Key, name):
        return getattr(Key, name)

    if len(name) == 1:
        return KeyCode.from_char(name.lower())

    raise ValueError(f"Unknown key: {name}")

# ── apply_all_bindings: build active_bindings từ full sign_keys map ─────────
def apply_all_bindings(sign_keys_map):
    """Nhận dict { combo_str: key_name } → build active_bindings."""
    global active_bindings, running_states
    log_debug(f"apply_all_bindings called with: {sign_keys_map}")
    for key in list(running_states):
        running_states[key] = False
    active_bindings = {}
    running_states  = {}
    for combo_str, key_name in sign_keys_map.items():
        fn = COMBO_MAP.get(combo_str)
        if fn is None:
            log_debug(f"Combo not found in COMBO_MAP: {combo_str}")
            continue
        try:
            parsed = parse_input(key_name)
            active_bindings[parsed] = fn
            log_debug(f"Bound: {parsed} -> {fn.__name__}")
        except Exception as e:
            log_debug(f"Error binding {key_name}: {e}")

# Hàm nhập FPS từ config.json
def get_fps():
    global FPSinput
    FPSinput = load_config().get("FPS", 120)
    log_debug(f"FPS set to: {FPSinput}")

# ── HTTP Server để nhận config từ frontend ────────────────────────────────────
class ConfigHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        log_debug(f"POST request received on: {self.path}")
        if self.path in ("/save", "/run", "/shutdown"):
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length)) if length > 0 else {}
                log_debug(f"POST body: {body}")
                if self.path == "/save":
                    save_config(body)
                    apply_all_bindings(body.get("comboSignKeys", {}))
                    get_fps()
                elif self.path == "/run":
                    global run_enabled
                    run_enabled = bool(body.get("enabled", False))
                    log_debug(f"run_enabled toggled to: {run_enabled}")
                    if not run_enabled:
                        for key in list(running_states):
                            running_states[key] = False
                elif self.path == "/shutdown":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(b'{"ok": true}')
                    log_debug("Shutdown command received, exiting process.")
                    threading.Thread(target=lambda: os._exit(0), daemon=True).start()
                    return
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

# ── Khởi tạo active_bindings từ config đã lưu ───────────────────────────────
_cfg = load_config()
apply_all_bindings(_cfg.get("comboSignKeys", {}))

def worker(key):
    _thread_local.bind_key = key
    log_debug(f"Worker thread started for key: {key}")
    while running_states.get(key, False):
        fn = active_bindings.get(key)
        if fn is None:
            log_debug(f"Worker: no function bound to {key}")
            break
        try:
            log_debug(f"Worker: executing {fn.__name__}")
            fn(FPSinput)
            log_debug(f"Worker: finished executing {fn.__name__}")
        except Exception as e:
            log_debug(f"Worker Exception running {fn.__name__}: {e}")
            import traceback
            log_debug(traceback.format_exc())
            break
    log_debug(f"Worker thread stopped for key: {key}")

def on_press(key):
    pressed.add(key)
    log_debug(f"on_press: {key} (run_enabled={run_enabled})")
    if not run_enabled:
        return
    for tgt in list(active_bindings):
        if any(tgt == k for k in pressed) and not running_states.get(tgt, False):
            running_states[tgt] = True
            log_debug(f"Trigger worker for target key: {tgt}")
            threading.Thread(target=worker, args=(tgt,), daemon=True).start()

def on_release(key):
    pressed.discard(key)
    log_debug(f"on_release: {key}")
    for tgt in list(active_bindings):
        if not any(tgt == k for k in pressed):
            running_states[tgt] = False

def on_click(x, y, button, is_pressed):
    if is_pressed:
        pressed.add(button)
        log_debug(f"on_click (press): {button} (run_enabled={run_enabled})")
        if not run_enabled:
            return
        for tgt in list(active_bindings):
            if any(tgt == k for k in pressed) and not running_states.get(tgt, False):
                running_states[tgt] = True
                log_debug(f"Trigger worker for target button: {tgt}")
                threading.Thread(target=worker, args=(tgt,), daemon=True).start()
    else:
        pressed.discard(button)
        log_debug(f"on_click (release): {button}")
        for tgt in list(active_bindings):
            if not any(tgt == k for k in pressed):
                running_states[tgt] = False

kb.Listener(on_press=on_press,on_release=on_release).start()
ms.Listener(on_click=on_click).start()



threading.Thread(target=start_http_server, daemon=True).start()
threading.Event().wait()
