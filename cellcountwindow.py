import cv2 as cv
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QMainWindow,
                               QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel,
                               QSlider, QPushButton)

from cellcount import CellCount
from infobutton import InfoButton


class CellCountWindow(QMainWindow):
    def __init__(self, img):
        super().__init__()

        self.img = img
        self.setWindowTitle("Cell Counting Window")

        # --- Layout structure ---
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        # Control Panel
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_container.setFixedSize(400, 200)
        # 1st and 2nd row: peak_thresh_frac information and slider
        container_1 = QWidget()
        layout_1 = QHBoxLayout(container_1)
        container_2 = QWidget()
        layout_2 = QHBoxLayout(container_2)
        # 3rd and 4th row: min_area information and slider
        container_3 = QWidget()
        layout_3 = QHBoxLayout(container_3)
        container_4 = QWidget()
        layout_4 = QHBoxLayout(container_4)
        # Results Display
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_container.setMaximumHeight(420)



        # --- Peak Thresh Frac controls ---
        ptf_min = QLabel("0.25")
        ptf_max = QLabel("0.5")
        self.ptf_slider = QSlider(Qt.Horizontal)
        self.ptf_slider.setRange(25, 50)
        self.ptf_slider.setValue(35)
        self.ptf_slider.sliderReleased.connect(self.ptf_changed)
        self.current_ptf = self.ptf_slider.value() / 100
        ptf_label = QLabel("peak_thresh_frac:")
        ptf_info = InfoButton("Sensitivity of cell detection\n"
                              "Lower values detect \n"
                              "more cells (may over-split)\n"
                              "Higher values detect \n"
                              "fewer cells (may merge\n" 
                              "cells)")
        self.ptf_value = QLabel(f"{self.current_ptf}")

        # --- Min area controls ---
        min_min = QLabel("20px")
        min_max = QLabel("200px")
        self.min_slider = QSlider(Qt.Horizontal)
        self.min_slider.setRange(20, 200)
        self.min_slider.setValue(40)
        self.min_slider.sliderReleased.connect(self.min_area_changed)
        self.current_min = self.min_slider.value()
        min_info = InfoButton("Minimum size counted\n" 
                              "as cell during area \n" 
                              "filtration step.")
        min_area_label = QLabel("min_area:")
        self.min_area_value = QLabel(f"{self.current_min}px")

        # --- Cancel controls ---
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)
        cancel_button.setFixedSize(100, 25)

        # --- Initial cellcount ---
        self.analysis = CellCount(img=self.img,
                                  peak_thresh_frac=self.current_ptf,
                                  min_area=self.current_min)

        # --- Result display ---
        self.cell_count_label = QLabel(f"Cell Count: {self.analysis.run()[0]}")
        self.image = QLabel()
        h, w = img.shape[:2]
        display_w = min(400, w)
        display_h = min(400, h)
        self.image.setFixedSize(display_w, display_h)


        # Widgets added left to right
        layout_1.addWidget(ptf_info)
        layout_1.addWidget(ptf_label)
        layout_1.addWidget(self.ptf_value)
        layout_2.addWidget(ptf_min)
        layout_2.addWidget(self.ptf_slider)
        layout_2.addWidget(ptf_max)
        layout_3.addWidget(min_info)
        layout_3.addWidget(min_area_label)
        layout_3.addWidget(self.min_area_value)
        layout_4.addWidget(min_min)
        layout_4.addWidget(self.min_slider)
        layout_4.addWidget(min_max)
        # Widgets added top to bottom
        left_layout.addWidget(container_1)
        left_layout.addWidget(container_2)
        left_layout.addWidget(container_3)
        left_layout.addWidget(container_4)
        left_layout.addWidget(cancel_button)

        # Widgets added top to bottom
        right_layout.addWidget(self.cell_count_label)
        right_layout.addWidget(self.image)
        # Widgets added left to right
        main_layout.addWidget(left_container)
        main_layout.addWidget(right_container)

        self.setCentralWidget(main_container)

        # --- Displays results ---
        self.update_preview()

    def show_image(self, img):
        """
        input: img
        creates QImage from img and QPixmap from QImage
        Pixmap displayed as preview image in CellCountWindow
        """
        if img.ndim == 2:
            img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

        h, w = img.shape[:2]
        qimg = QImage(img.data, w, h, img.strides[0],QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(qimg)
        pixmap = pixmap.scaled(self.image.width(), self.image.height(), Qt.KeepAspectRatio,
                                                Qt.SmoothTransformation)
        self.image.setPixmap(pixmap)


    def update_preview(self):
        """
        Runs CellCount with current peak_thresh_frac and min_area values
        Displays updated preview and updated cell count in CellCountWindow
        """
        self.analysis.peak_thresh_frac = self.current_ptf
        self.analysis.min_area = self.current_min
        count, preview, = self.analysis.run()[:2]
        self.show_image(preview)
        self.cell_count_label.setText(f"Cell Count: {count}")

    def ptf_changed(self):
        """
        Update slider value and update preview
        """
        pos = self.ptf_slider.value()
        self.current_ptf = pos / 100
        self.ptf_value.setText(f"{self.current_ptf}")
        self.update_preview()

    def min_area_changed(self):
        """
        Update slider value and update preview
        """
        pos = self.min_slider.value()
        self.current_min = pos
        self.min_area_value.setText(f"{self.current_min} px")
        self.update_preview()

    def cancel(self):
        """Closes window"""
        self.close()
