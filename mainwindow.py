from PySide6.QtWidgets import ( QWidget, QMainWindow, QHBoxLayout,
                                QVBoxLayout, QPushButton, QLabel)

from infobutton import InfoButton
from imagehandling import ImageHandling
from maskgeneratorwindow import MaskGeneratorWindow
from cellcountwindow import CellCountWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Load Image")
        self.images = ImageHandling()

        # --- Layout structure ---
        container = QWidget()
        layout = QVBoxLayout(container)

        # Top row: load image controls
        inner_container1 = QWidget()
        inner_layout1 = QHBoxLayout(inner_container1)
        # Middle row: mask generation
        inner_container2 = QWidget()
        inner_layout2 = QHBoxLayout(inner_container2)
        inner_container2.setFixedWidth(130)
        # Bottom row: cell counting
        inner_container3 = QWidget()
        inner_layout3 = QHBoxLayout(inner_container3)
        inner_container3.setFixedWidth(130)

        # --- Load image controls ---
        load_info = InfoButton("Click to choose an image\n" 
                               "file (.png, .jpg, .jpeg,\n"
                               ".tif, .tiff) for cell \n" 
                               "counting.")
        self.load_button = QPushButton("Load Image")
        self.load_button.setFixedSize(100, 25)
        self.load_button.clicked.connect(self.load_file)
        self.load_label = QLabel("No Image Loaded")

        # --- Generate mask controls ---
        mask_info = InfoButton("Optional. Click here to \n" 
                               "define area where cells \n"
                               "should be counted.")
        self.mask_button = QPushButton("Generate Mask")
        self.mask_button.setFixedSize(100, 25)
        self.mask_button.clicked.connect(self.generate_mask)
        self.mask_button.setEnabled(False) # disabled until image is loaded

        # --- Cell count controls ---
        count_info = InfoButton("Click here to begin cell\n" 
                               "counting without applying\n"
                               "mask.")
        self.analyze_button = QPushButton("Count Cells")
        self.analyze_button.setFixedSize(100, 25)
        self.analyze_button.clicked.connect(self.analyze_file)
        self.analyze_button.setEnabled(False) # disabled until image is loaded

        # Widgets added left to right
        inner_layout1.addWidget(load_info)
        inner_layout1.addWidget(self.load_button)
        inner_layout1.addWidget(self.load_label)
        inner_layout2.addWidget(mask_info)
        inner_layout2.addWidget(self.mask_button)
        inner_layout3.addWidget(count_info)
        inner_layout3.addWidget(self.analyze_button)
        # Widgets added top to bottom
        layout.addWidget(inner_container1)
        layout.addWidget(inner_container2)
        layout.addWidget(inner_container3)

        self.setCentralWidget(container)

    def load_file(self):
        """
        Load image with ImageHandling, enables mask generation and cell counting
        """
        if self.images.load_file(self):
            self.load_label.setText(f"{self.images.filename} Loaded")
            self.mask_button.setEnabled(True)
            self.analyze_button.setEnabled(True)

    def generate_mask(self):
        """
        Opens MaskGeneratorWindow for optional mask generation and closes MainWindow
        """
        self.mask_window = MaskGeneratorWindow(self.images.loaded_image)
        self.mask_window.show()
        self.close()


    def analyze_file(self):
        """
        Opens CellAnalysisWindow with loaded image as input and closes MainWindow
        """
        self.analysis_window = CellCountWindow(self.images.loaded_image)
        self.analysis_window.show()
        self.close()
