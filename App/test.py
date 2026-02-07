from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QPixmap Tutorial")
        self.resize(1000,700)
        layout = QVBoxLayout()
        
        # 1. Create label
        label = QLabel(self)
        path="/Users/ashutosh/The_Great_Eye/App/Test_dir/Puja' 24 and Bhavesh lagn/IMG20240608150101.jpg"
        # 2. Load and set QPixmap
        pixmap = QPixmap(path)
        scaled_pixmap = pixmap.scaled(50, 100, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        if not pixmap.isNull():
            label.setPixmap(scaled_pixmap)
        else:
            label.setText("Image not found")
        
        layout.addWidget(label)
        self.setLayout(layout)
        self.show()

app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec())
