import sys, pyautogui, threading
from textCapture import *
from processText import *
from pynput import mouse
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction

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
        
class Region(QMainWindow):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()

        self.setFixedSize(x2-x1, y2-y1)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.move(x1, y1) # top-left

        widget = QWidget(self);
        widget.setStyleSheet("background-color: rgba(255, 255, 255, 0); border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop: 0 yellow, stop: 1 red);")
        self.setCentralWidget(widget)
        self.show()
        
        self.finish = QAction("Quit", self)
        self.finish.triggered.connect(self.closeEvent)

        self.t1 = threading.Thread(target=self.run)
        self.t1.start()

    def closeEvent(self, e):
        try:
            self.isFound = True
            self.isClose = True
            self.t1.join()
        except: pass
        print('Closed!')

    def run(self):
        self.isClose = False
        while True:
            calls = 0
            self.isFound = False
            im1 = im2 = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))

            while not self.isFound:
                im2 = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
                if (list(im1.getdata()) != list(im2.getdata())):
                    text = get_image(im2)
                    self.isFound = processText(text)

                im1 = im2

            if self.isClose: break
            res = input('Run again (y/n): ')
            if res != 'y': self.close() ; break

if __name__ == '__main__':
    x1, y1 = get_coord('\nSelect region 1')
    x2, y2 = get_coord('\nSelect region 2')

    if x2 < x1: x1, x2 = x2, x1
    if y2 < y1: y1, y2 = y2, y1

    app = QApplication(sys.argv)

    ex = Region(x1, y1, x2, y2)

    sys.exit(app.exec_())
