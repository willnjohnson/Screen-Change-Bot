import pyautogui
from selectRegion import *
from textCapture import *
from pynput import mouse
import subprocess, threading

tmpx = tmpy = 0

def call_listener():
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()

def on_click(x, y, button, pressed):
    global tmpx
    global tmpy
    
    if button == mouse.Button.left:
        tmpx, tmpy = x, y

    return False

def set_xy(tmpx, tmpy):
    print(f'Position set: ({tmpx}, {tmpy})')
    return tmpx, tmpy

def get_coord(msg=None):
    while True:
        if msg: print(msg)
        call_listener()
        x, y = set_xy(tmpx, tmpy)
        res = input('Confirm (y/n/) or Exit (x): ')
        if res == 'y': return x, y
        if res == 'x': exit(1)

def sel_region(x1, y1, x2, y2):
    subprocess.call(f"python3 selectRegion.py {x1} {y1} {x2} {y2}", shell=False)

def main():
    calls = 0
    while True:
        x1, y1 = get_coord('\nSelect region 1 (top-left corner)')
        x2, y2 = get_coord('\nSelect region 2 (bottom-right corner)')

        if x2 < x1 or y2 < y1:
            print('\nRegion UNKNOWN. Try again!')
        else: break
    
    thread = threading.Thread(target=sel_region, args=(x1, y1, x2, y2)).start()

    im = im_to_check = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))

    while True:
        im_to_check = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
        if (list(im.getdata()) != list(im_to_check.getdata())):
            # pass im as an argument to some function to process image result
            calls += 1
            get_image(im_to_check, calls)

        im = im_to_check

if __name__ == "__main__":
    main()
