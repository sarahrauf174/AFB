from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy, \
    QFileDialog
from PySide6.QtGui import QImage, QPixmap
import cv2
from PySide6.QtCore import Qt
import csv

class ResultsWindow(QMainWindow):
    def __init__(self, processed_img, data, stats):
        super().__init__()
        self.setWindowTitle("Results")

        self.processed_img = processed_img
        self.data = data
        self.stats = stats

        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)

        stat_container = QWidget()
        stat_layout = QVBoxLayout(stat_container)

        self.stat = QLabel("Area Statistics")
        stat_layout.addWidget(self.stat)

        self.cell_count = QLabel(f"Cells: {self.stats[0]}")
        stat_layout.addWidget(self.cell_count)
        self.mean_area = QLabel(f"Mean: {self.stats[1].round(3)}")
        stat_layout.addWidget(self.mean_area)
        self.min_area = QLabel(f"Min: {self.stats[2]}")
        stat_layout.addWidget(self.min_area)
        self.max_area = QLabel(f"Max: {self.stats[3]}")
        stat_layout.addWidget(self.max_area)
        self.sd_area = QLabel(f"SD: {self.stats[4].round(3)}")
        stat_layout.addWidget(self.sd_area)

        self.download_button = QPushButton("Download CSV")
        self.download_button.clicked.connect(self.save_data)

        stat_layout.addWidget(self.download_button)

        self.image = QLabel()
        self.image.setFixedSize(400, 400)


        main_layout.addWidget(self.image)
        self.show_image()

        main_layout.addWidget(stat_container)

        self.setCentralWidget(main_container)


    def show_image(self):
        cv_img = self.processed_img
        if len(cv_img.shape) == 2:
            img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)
        else:
            img = cv_img.copy()
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_img.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg).scaled(self.image.width(), self.image.height(),
                                                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image.setPixmap(pixmap)

    def save_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save CSV File', 'results.csv', "CSV Files (*.csv")
        if not file_path:
            return

        with open(file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Label", "Area", "X-Cord", "Y-Cord", "Height", "Width"])
            writer.writerows(self.data)





