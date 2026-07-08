import ctypes
import time
import sys
import subprocess
import json
import os
import pynput

mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
left = pynput.mouse.Button.left
right = pynput.mouse.Button.right
