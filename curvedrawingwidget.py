import cv2 as cv
import numpy as np
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen
from PySide6.QtWidgets import QWidget


class CurveDrawingWidget(QWidget):
    def __init__(self, img):
        super().__init__()

        self.img = img
        self.orig_h, self.orig_w = img.shape[:2]

        # Sets maximum display size (preserves aspect ratio)
        self.display_w = min(400, self.orig_w)
        self.display_h = min(400, self.orig_h)
        self.pixmap = self.get_scaled_pixmap()
        self.setFixedSize(self.pixmap.width(), self.pixmap.height())

        # =========================
        # Storage for curves
        # =========================
        self.start_curve = []
        self.stop_curve = []
        self.mode = "start"



    def get_scaled_pixmap(self):
        """
        Creates pixmap from input image
        Scales pixmap down
        """

        img = self.img
        h, w = img.shape[:2]

        qimg = QImage(img.data, w, h, img.strides[0], QImage.Format_RGB888)

        img = np.ascontiguousarray(img)  
        h, w = img.shape[:2]

        pixmap = QPixmap.fromImage(qimg)
        pixmap = pixmap.scaled(self.display_w, self.display_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap

    def paintEvent(self, event):
        """
        Paint curves on display image. 
        Red color for start curve,
        blue color for stop curve. Draws line between points in start/stop curves.
        """
        painter = QPainter(self)
        if self.pixmap:
            painter.drawPixmap(0, 0, self.pixmap)

        start_pen = QPen(Qt.red, 2)
        stop_pen = QPen(Qt.blue, 2)

        if len(self.start_curve) > 1:
            painter.setPen(start_pen)
            for i in range(1, len(self.start_curve)):
                p1 = self.to_display_coords(self.start_curve[i-1])
                p2 = self.to_display_coords(self.start_curve[i])
                painter.drawLine(p1, p2)

        if len(self.stop_curve) > 1:
            painter.setPen(stop_pen)
            for i in range(1, len(self.stop_curve)):
                p1 = self.to_display_coords(self.stop_curve[i-1])
                p2 = self.to_display_coords(self.stop_curve[i])
                painter.drawLine(p1, p2)

    def to_display_coords(self, point):
        """
        Scaled coordinates of points
        """
        x, y = point
        scale_x = self.pixmap.width() / self.orig_w
        scale_y = self.pixmap.height() / self.orig_h
        return QPoint(int(x * scale_x), int(y * scale_y))

    def mousePressEvent(self, event):
        """
        Writes coordinates from left click on image to curves
        """
        if event.button() == Qt.LeftButton:

            scale_x = self.orig_w / self.pixmap.width()
            scale_y = self.orig_h / self.pixmap.height()
            x = int(event.position().x() * scale_x)
            y = int(event.position().y() * scale_y)

            if self.mode == "start":
                self.start_curve.append((x, y))
            elif self.mode == "stop":
                self.stop_curve.append((x, y))

            self.update()
