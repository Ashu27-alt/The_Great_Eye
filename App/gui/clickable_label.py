from PyQt5.QtWidgets import QLabel
import subprocess
import platform
import os
from PyQt5.QtCore import Qt

class ClickableImage(QLabel):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.open_file()

    def open_file(self):
        try:
            if platform.system() == "Darwin":      
                subprocess.run(["open", self.path])
            elif platform.system() == "Windows":   
                os.startfile(self.path)
            else:                    
                subprocess.run(["xdg-open", self.path])
        except Exception as e:
            print(f"Could not open file: {e}")