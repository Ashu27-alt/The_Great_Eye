from gui.main_window import mainWindow
from PyQt5.QtWidgets import QApplication
import os

if __name__ == "__main__":
    os.environ["KMP_DUPLICATE_LIB_OK"]="True"
    app = QApplication([])
    window = mainWindow()
    window.show()
    app.exec()
    