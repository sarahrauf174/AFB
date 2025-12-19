import cv2
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QMainWindow,
                               QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel,
                               QSlider, QPushButton)
from cellanalysis import CellAnalysis
from resultswindow import ResultsWindow


class CellAnalysisWindow(QMainWindow):
    def __init__(self, loaded_image):
        super().__init__()

        self.setWindowTitle("Cell Analysis Window")
        self.img = loaded_image

        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)



        # setting labels (left)

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)

        welcome_label = QLabel("Set parameters to find cells")
        left_layout.addWidget(welcome_label)

        setting_container = QWidget()
        setting_layout = QHBoxLayout(setting_container)

        label_container = QWidget()
        label_layout = QVBoxLayout(label_container)
        label_container.setFixedSize(100,200)

        self.blur_label = QLabel("Blur:")
        self.blur_label.setToolTip("Kernel size setting for \n"
                                  "Gaussian blur. A larger \n"
                                  "kernel size results in a \n"
                                  "more aggressive blurring. ")
        self.enhance_label = QLabel("Enhance:")
        self.enhance_label.setToolTip("I dunno ")
        self.threshold_label = QLabel("Threshold:")
        self.threshold_label.setToolTip("Converts image to binary \n"
                                   "image. A stronger threshold\n"
                                   " does something")
        self.min_area_label = QLabel("Min Area:")
        self.min_area_label.setToolTip("Filters out components\n"
                                       " smaller than the given\n"
                                       " threshold.")
        self.max_area_label = QLabel("Max Area:")
        self.max_area_label.setToolTip("Filters out components\n"
                                       " larger than the given\n"
                                       " threshold.")

        label_layout.addWidget(self.blur_label)
        label_layout.addWidget(self.enhance_label)
        label_layout.addWidget(self.threshold_label)
        label_layout.addWidget(self.min_area_label)
        label_layout.addWidget(self.max_area_label)

        setting_layout.addWidget(label_container)


        slider_container = QWidget()
        slider_layout = QVBoxLayout(slider_container)
        slider_container.setFixedSize(200,200)


        self.kernel_sizes = [1,3,5,7,9]
        self.current_blur = 7
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(0, len(self.kernel_sizes)-1)
        self.blur_slider.setValue(3)
        self.blur_slider.sliderReleased.connect(self.blur_changed)

        self.current_enhance = 50
        self.enhance_slider = QSlider(Qt.Horizontal)
        self.enhance_slider.setRange(0, 100)
        self.enhance_slider.setValue(50)
        self.enhance_slider.sliderReleased.connect(self.enhance_changed)

        self.current_thresh = 50
        self.thresh_slider = QSlider(Qt.Horizontal)
        self.thresh_slider.setRange(0, 255)
        self.thresh_slider.setValue(self.current_thresh)
        self.thresh_slider.sliderReleased.connect(self.threshold_changed)

        self.current_min = 200
        self.min_slider = QSlider(Qt.Horizontal)
        self.min_slider.setRange(0, 2000)
        self.min_slider.setValue(self.current_min)
        self.min_slider.sliderReleased.connect(self.min_area_changed)

        self.current_max = 2000
        self.max_slider = QSlider(Qt.Horizontal)
        self.max_slider.setRange(500, 10000)
        self.max_slider.setValue(self.current_max)
        self.max_slider.sliderReleased.connect(self.max_area_changed)

        slider_layout.addWidget(self.blur_slider)
        slider_layout.addWidget(self.enhance_slider)
        slider_layout.addWidget(self.thresh_slider)
        slider_layout.addWidget(self.min_slider)
        slider_layout.addWidget(self.max_slider)

        setting_layout.addWidget(slider_container)

        self.analysis = CellAnalysis(img=self.img,
                                      blur=self.current_blur,
                                      enhance=self.current_enhance,
                                      thresh=self.current_thresh,
                                      min_area=self.current_min,
                                      max_area=self.current_max,
                                      )



        value_container = QWidget()
        value_layout = QVBoxLayout(value_container)
        label_container.setFixedSize(100, 200)

        self.blur_value = QLabel(f"{self.current_blur}")
        self.enhance_value = QLabel(f"{self.current_enhance}")
        self.threshold_value = QLabel(f"{self.current_thresh}")
        self.min_area_value = QLabel(f"{self.current_min}")
        self.max_area_value = QLabel(f"{self.current_max}")

        value_layout.addWidget(self.blur_value)
        value_layout.addWidget(self.enhance_value)
        value_layout.addWidget(self.threshold_value)
        value_layout.addWidget(self.min_area_value)
        value_layout.addWidget(self.max_area_value)

        setting_layout.addWidget(value_container)

        left_layout.addWidget(setting_container)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)

        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.save_data)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)

        button_layout.addWidget(ok_button)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(cancel_button)

        left_layout.addWidget(button_container)

        self.image_label = QLabel()
        self.image_label.setFixedSize(400,400)





        main_layout.addWidget(left_container)
        main_layout.addWidget(self.image_label)

        self.update_preview()

        self.setCentralWidget(main_container)


    def blur_changed(self):
        pos = self.blur_slider.value()
        self.current_blur = self.kernel_sizes[pos]
        self.blur_value.setText(f"{self.current_blur}")
        self.update_preview()

    def enhance_changed(self):
        pos = self.enhance_slider.value()
        self.current_enhance = pos
        self.enhance_value.setText(f"{self.current_enhance}")
        self.update_preview()

    def threshold_changed(self):
        pos = self.thresh_slider.value()
        self.current_thresh = pos
        self.threshold_value.setText(f"{self.current_thresh}")
        self.update_preview()

    def min_area_changed(self):
        pos = self.min_slider.value()
        self.current_min = pos
        self.min_area_value.setText(f"{self.current_min}")
        self.update_preview()

    def max_area_changed(self):
        pos = self.max_slider.value()
        self.current_max = pos
        self.max_area_value.setText(f"{self.current_max}")
        self.update_preview()

    def show_image(self, cv_img):
        if len(cv_img.shape) == 2:
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)
        img_copy = cv_img.copy()
        rgb_img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytesPerLine = 3 * w
        qImg = QImage(rgb_img.data, w, h, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg).scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio,
                                                Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

    def update_preview(self):
        self.analysis.blur = self.current_blur
        self.analysis.enhance = self.current_enhance
        self.analysis.thresh = self.current_thresh
        self.analysis.min = self.current_min
        self.analysis.max = self.current_max
        self.preview = self.analysis.run()
        self.show_image(self.preview)

    def cancel(self):
        self.close()

    def save_data(self):
        self.analysis.get_data()
        self.results = ResultsWindow(processed_img=self.preview,
                                     data = self.analysis.data,
                                     stats = self.analysis.area_stat)
        self.results.show()
        self.cancel()

    def reset(self):
        self.blur_slider.setValue(3)
        self.enhance_slider.setValue(50)
        self.thresh_slider.setValue(50)
        self.min_slider.setValue(200)
        self.max_slider.setValue(2000)

        self.update_preview()








