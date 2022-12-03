import pyautogui
from textCapture import *
from pynput import mouse

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

def get_coord(m=None):
    while True:
        if m: print(m)
        call_listener()
        x, y = set_xy(tmpx, tmpy)
        res = input('Confirm (y/n/) or Exit (x): ')
        if res == 'y': return x, y
        if res == 'x': exit(1)

def main():
    calls = 0
    x1, y1 = get_coord('\nSelect region 1')
    x2, y2 = get_coord('\nSelect region 2')
    
    im = im_to_check = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))

    while True:
        im_to_check = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
        if (list(im.getdata()) != list(im_to_check.getdata())):
            # pass im as an argument to some function to process image result
            calls += 1
            getImage(im_to_check, calls)

        im = im_to_check

if __name__ == "__main__":
    main()
