from PySide6.QtWidgets import ( QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton,
                                QLabel)
import os
from imagehandling import ImageHandling
from cellanalysiswindow import CellAnalysisWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Load Image")
        self.images = ImageHandling()

        container = QWidget()
        layout = QVBoxLayout(container)

        self.label = QLabel("Welcome to the image loader!")
        layout.addWidget(self.label)

        # choosing image
        inner_container1 = QWidget()
        inner_layout1 = QHBoxLayout(inner_container1)

        self.choose_button = QPushButton("Choose Image")
        self.choose_button.setFixedSize(100, 25)
        self.choose_button.clicked.connect(self.choose_file)
        inner_layout1.addWidget(self.choose_button)

        self.choose_label = QLabel("No Image File Selected")
        inner_layout1.addWidget(self.choose_label)

        layout.addWidget(inner_container1)


        # load image file
        inner_container2 = QWidget()
        inner_layout2 = QHBoxLayout(inner_container2)

        self.load_button = QPushButton("Load Image")
        self.load_button.setFixedSize(100, 25)
        self.load_button.clicked.connect(self.load_file)
        inner_layout2.addWidget(self.load_button)

        self.load_label = QLabel("No Image File Loaded")
        inner_layout2.addWidget(self.load_label)

        layout.addWidget(inner_container2)

        # analyze image file and cancel button
        inner_container3 = QWidget()
        inner_layout3 = QHBoxLayout(inner_container3)

        self.analyze_button = QPushButton("Analyze Image")
        self.analyze_button.setFixedSize(100, 25)
        self.analyze_button.clicked.connect(self.analyze_file)
        inner_layout3.addWidget(self.analyze_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(100, 25)
        self.cancel_button.clicked.connect(self.cancel)
        inner_layout3.addWidget(self.cancel_button)


        layout.addWidget(inner_container3)

        self.setCentralWidget(container)




    def choose_file(self):
        if self.images.choose_file(self):
            self.choose_label.setText(f"{os.path.basename(self.images.image_file)} Selected")

    def load_file(self):
        if self.images.load_image(self):
            self.load_label.setText(f"{os.path.basename(self.images.image_file)} Loaded")

    def analyze_file(self):
        self.analysis_window = CellAnalysisWindow(self.images.loaded_image)
        self.analysis_window.show()

    def cancel(self):
        self.close()





