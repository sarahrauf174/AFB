
from PySide6.QtWidgets import (QMainWindow,
                               QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton)
from curvedrawingwidget import CurveDrawingWidget
from infobutton import InfoButton
from maskgenerator import MaskGenerator
from cellcountwindow import CellCountWindow


class MaskGeneratorWindow(QMainWindow):
    def __init__(self, img):
        super().__init__()

        self.setWindowTitle("Mask Generator Window")
        self.curve_drawer = CurveDrawingWidget(img)
        self.img = img

        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)

        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_container.setFixedSize(250, 150)

        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_container.setFixedSize(30, 150)

        self.start_info = InfoButton("Click on image to \n"
                                     "draw line from which\n"
                                     "cell counting should\n"
                                     " start.")
        self.start_button = QPushButton("Start Line")
        self.start_button.setFixedSize(100, 25)
        self.start_button.clicked.connect(lambda: self.set_mode("start"))

        self.stop_info = InfoButton("Click on image to \n"
                                     "draw line to which\n"
                                     "cell counting should\n"
                                     " continue.")
        self.stop_button = QPushButton("Stop Line")
        self.stop_button.setFixedSize(100, 25)
        self.stop_button.clicked.connect(lambda: self.set_mode("stop"))

        self.done_info = InfoButton("Click here when \n"
                                         "you are satisfied\n"
                                         " with the borders.")
        self.done_button = QPushButton("OK")
        self.done_button.setFixedSize(100, 25)
        self.done_button.clicked.connect(self.done)

        info_layout.addWidget(self.start_info)
        info_layout.addWidget(self.stop_info)
        info_layout.addWidget(self.done_info)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.done_button)

        main_layout.addWidget(info_container)
        main_layout.addWidget(button_container)
        main_layout.addWidget(self.curve_drawer)

        self.setCentralWidget(main_container)

    def set_mode(self, mode):
        """
        Changes curve drawing mode (start or stop curve)
        """
        self.curve_drawer.mode = mode

    def done(self):
        """
        Generates mask between curves using MaskGenerator.
        Calls CellAnalysisWindow with masked image
        """
        if len(self.curve_drawer.start_curve) < 2 or len(self.curve_drawer.stop_curve) < 2:
            return

        generator = MaskGenerator(self.img, self.curve_drawer.start_curve, self.curve_drawer.stop_curve)
        masked_image = generator.masked
        self.analysis = CellCountWindow(masked_image)
        self.analysis.show()
        self.close()
