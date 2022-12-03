import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

class Region(QMainWindow):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()

        self.setFixedSize(x2-x1, y2-y1)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.move(x1, y1) # top-left

        widget = QWidget(self);
        widget.setStyleSheet("background-color: rgba(255, 255, 255, 0); border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop: 0 yellow, stop: 1 red);");
        self.setCentralWidget(widget);
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    try: ex = Region(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    except: print('Error creating region.')

    sys.exit(app.exec_())
