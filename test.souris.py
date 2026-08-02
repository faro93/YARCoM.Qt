import sys

from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PySide6 import QtWidgets as qtw

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.version = "0.1"
        self.version_string = "2024/10/31"
        
        self.setWindowTitle(f"YARCoM for Qt")
        self.setMouseTracking(True)
        
        self.label = qtw.QLabel("Click in this window")
        
        self.setCentralWidget(self.label)
        
    def mouseMoveEvent(self, event):
        self.label.setText("mouseMoveEvent")
    
    def mousePressEvent(self, event):
        if event.button() == qtc.Qt.MouseButton.LeftButton:
            self.label.setText("Left button pressed")
        elif event.button() == qtc.Qt.MouseButton.RightButton:
            self.label.setText("Right button pressed")
        elif event.button() == qtc.Qt.MouseButton.MiddleButton:
            self.label.setText("Middle button pressed")
        # self.label.setText("mousePressEvent")
        
    def mouseReleaseEvent(self, event):
        if event.button() == qtc.Qt.MouseButton.LeftButton:
            self.label.setText("Left button released")
        elif event.button() == qtc.Qt.MouseButton.RightButton:
            self.label.setText("Right button releassed")
        elif event.button() == qtc.Qt.MouseButton.MiddleButton:
            self.label.setText("Middle button released")
        # self.label.setText("mouseReleaseEvent")
        
    def mouseDoubleClickEvent(self, event):
        self.label.setText("mouseDoubleClickEvent")

if __name__ == "__main__":
    main = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(main.exec())