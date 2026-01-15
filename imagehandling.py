import os
from PySide6.QtWidgets import QFileDialog, QMessageBox
import cv2 as cv
import tifffile as tiff


class ImageHandling:
    def __init__(self):
        self.file_path = None
        self.loaded_image = None
        self.filename = None
        self.ext = None

    def load_file(self, parent):
        """
        User chooses image file (.jpg, .jpeg, .png, .tif, .tiff)
        Image loaded with tifffile or OpenCV imread
        """
        path, _ = QFileDialog.getOpenFileName(
            parent,
            "Choose image file",
            filter="Images (*.jpg *.jpeg *.png *.tif *.tiff)"
        )

        if not path:
            self.file_path = None
            return False

        valid_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff']
        self.ext = os.path.splitext(path)[1].lower()

        if self.ext not in valid_extensions:
            QMessageBox.critical(
                parent,
                "Error",
                f"Image file must be one of {valid_extensions}"
            )
            self.file_path = None
            self.loaded_image = None
            return False

        self.file_path = path
        self.filename = os.path.basename(path)

        if self.ext in ('.tif', '.tiff'):
            self.loaded_image = tiff.imread(self.file_path)
        else:
            self.loaded_image = cv.imread(self.file_path)

        if self.loaded_image is None:
            QMessageBox.critical(
                parent,
                "Error",
                "Could not load image file"
            )
            self.file_path = None
            return False

        return True
