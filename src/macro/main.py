import ctypes
import time
import sys
import subprocess
import json
import os
import pynput
import threading
import keyboard

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
inputkeyboard = pynput.keyboard.Controller()
left = pynput.mouse.Button.left
right = pynput.mouse.Button.right

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

    inputkeyboard.press("w")

    T_FPS = [
        [30, 60, 100, 120, 220],
        [1.5, 1.366, 1.34, 1.32, 1.285]
    ]

    t = fps2t(T_FPS, fps)

    while time.perf_counter() - start < t:
        pass

    inputkeyboard.release("w")

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
            range(int(0.2 * fps))
        else:
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
            range(int(0.2 * fps))
        else:
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
            range(int(2 * fps))
        else:
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
    keys = [
        "caps lock",
        "w",
        "a",
        "s",
        "d",
        "left",
        "right"
    ]

    return not any(keyboard.is_pressed(key) for key in keys)

def skke(fps):
    start = time.perf_counter()
    for _ in range(int(0.1 * fps)):
        if time.perf_counter() - start > 0.1:
            range(int(0.1 * fps))
        else:
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

def skk0eqa_220(fps):
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



#Xử lý code chạy macro
running = False

def worker():
    global running

    while running and keyboard.is_pressed("caps lock"):
        skk0eqa_220(120)   # hoặc fps của bạn

    running = False


def on_press(event):
    global running

    if running:
        return

    running = True
    threading.Thread(target=worker, daemon=True).start()


def on_release(event):
    global running
    running = False


keyboard.on_press_key("caps lock", on_press)
keyboard.on_release_key("caps lock", on_release)

keyboard.wait()

