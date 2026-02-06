from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QFileDialog,QSizePolicy,QLineEdit,QProgressBar,QApplication
from PyQt5.QtCore import Qt,QTimer
from gui.thread import EmbedWorker
import torch
from core.Search.search_res import SearchClass

class mainWindow(QWidget):
    def __init__(self):
       super().__init__()

       SearchClass.loadIndex()

       #Model initialization
       QApplication.setStyle("Fusion")
       self.model = None
       self.processor = None
       if torch.cuda.is_available():
           self.device = 'cuda'
       elif torch.backends.mps.is_available():
           self.device='mps'
       else:
           self.device='cpu'     
           
       self.setWindowTitle("The Great Eye")
       self.resize(1000, 700)

       #layout components
       main_layout = QVBoxLayout()
       row1 = QHBoxLayout()
       row2 = QHBoxLayout()
       row3 = QHBoxLayout()
       row4 = QHBoxLayout()
       row5 = QHBoxLayout()

       #components
       self.browse_button = QPushButton("Browse")
       self.search_button = QPushButton("Search")
       self.process_button = QPushButton("Process")
       self.searchInput = QLineEdit()
       self.progressBar = QProgressBar()

       self.progressBar.setValue(0)
       self.progressBar.setVisible(False)
       self.process_button.hide()
       sp_retain = self.progressBar.sizePolicy()
       sp_retain.setRetainSizeWhenHidden(True)
       self.progressBar.setSizePolicy(sp_retain)

       self.progressBar.setMinimumWidth(600)
       self.progressBar.setFixedHeight(40)
       self.browse_button.setMinimumHeight(40)
       self.folderPath = QLabel("Enter Folder")
       self.folderPath.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

       self.placeholder=QLabel(" ")

       #adding widgets
       row1.addWidget(self.folderPath,5)
       row1.addWidget(self.browse_button,1)

       row2.addStretch()
       row2.addWidget(self.process_button)
       row2.addStretch()
       
       row3.addStretch(1)
       row3.addWidget(self.progressBar,10)
       row3.addStretch(1)

       row4.addStretch()
       row4.addWidget(self.searchInput)
       row4.addWidget(self.search_button)
       row4.addStretch()


       row5.addWidget(self.placeholder)

       #CSS
       self.browse_button.setMinimumHeight(40)

       self.search_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
       self.process_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
       self.searchInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
       self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
       self.searchInput.setFixedWidth(500)
       self.searchInput.setFixedHeight(25)
       self.search_button.setFixedHeight(36)
       self.process_button.setFixedHeight(36)

       self.folderPath.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
       self.folderPath.setMinimumHeight(40)

       self.folderPath.setStyleSheet("""
        QLabel {
            border: 2px solid #555;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }
        QPushButton {
            background-color: #808080;
            border: 2px solid #555;
            border-radius: 10px;
            padding: 6px;
            font-size: 12px;
        }
                                     
        QPushButton:hover {
        background-color: #696969;
        }

        QPushButton:pressed {
            background-color: #666666;
        }
        
        QProgressBar {
            border: 2px solid #ffffff; /* White border to   see it against dark background */
            border-radius: 5px;
            text-align: center;
            background-color: #333333; /* Darker grey   background */
            color: white; /* Progress percentage text color     */
        }
        QProgressBar::chunk {
            background-color: #f39c12; /* Bright Orange     chunk */
            width: 20px;
        }
        """)
       
       #functionalities
       self.browse_button.clicked.connect(self.browseFunc)
       self.search_button.clicked.connect(self.searchFunc)
       self.process_button.clicked.connect(self.processFunc)

       #setting main layout
       main_layout.addLayout(row1)
       main_layout.addLayout(row2)
       main_layout.addLayout(row3)
       main_layout.addLayout(row4)
       main_layout.addLayout(row5,80)
       main_layout.addStretch(1)
       self.setLayout(main_layout)


# SETTING UP ALL REQUIRED FUNCTIONS

    #getting the paths of similar images
    def handleSearch(self,vector):
        paths=SearchClass.res(vector)
        self.placeholder.setText(paths)

    #called when the processing of a given folder is completed
    def onIndexingComplete(self):
        self.progressBar.setValue(100)
        self.placeholder.setText("Indexing complete")
        QTimer.singleShot(1000,lambda: self.progressBar.setVisible(False)) 
        self.process_button.setEnabled(True)
        self.browse_button.setEnabled(True)

    #opens a dialog to choose a folder
    def browseFunc(self):
        dirPath = QFileDialog.getExistingDirectory(None,"Select Folder","/Users/ashutosh/The_Great_Eye/App/Test_dir",QFileDialog.Option.ShowDirsOnly)
        if dirPath:
            self.folderPath.setText(dirPath)
            self.process_button.show()
    
    #starts the flow of the search operation for similar images
    def searchFunc(self):
        query = self.searchInput.text()
        self.worker=EmbedWorker(
            mode='text',
            payload=query,
            model=self.model,
            processor=self.processor,
            device=self.device
        )
        self.worker.result.connect(self.handleSearch)
        self.worker.finished.connect(lambda:self.placeholder.setText('someting working'))
        self.worker.start()

    #starts the process the embed the images using CLIP and then storing it in vectors.index(faiss)
    def processFunc(self):
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(100)

        QApplication.processEvents()

        self.worker = EmbedWorker(
            mode='image',
            payload=self.folderPath.text(),
            model = self.model,
            processor=self.processor,
            device = self.device
        )
        self.worker.progress.connect(self.progressBar.setValue)
        self.worker.finished.connect(self.onIndexingComplete)
        self.worker.start()

        self.process_button.setEnabled(False)
        self.browse_button.setEnabled(False)