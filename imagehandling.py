import os

from PySide6.QtWidgets import QFileDialog, QMessageBox
import cv2


class ImageHandling:
    def __init__(self):
        self.image_file = None
        self.loaded_image = None
        self.filename = None



    def choose_file(self, parent):

        file_path, _ = QFileDialog.getOpenFileName(parent, "Choose image file", filter = "Images (*.jpg *.jpeg *.png)" )
        print(file_path)

        if not file_path:
            self.image_file = None
            return False

        valid_extensions = ['.jpg', '.jpeg', '.png']
        ext = os.path.splitext(file_path)[1].lower()

        if ext not in valid_extensions:
            QMessageBox.critical(parent, "Error", f"Image file must be one of {valid_extensions}")
            self.image_file = None
            return False

        self.image_file = file_path
        self.filename = os.path.basename(file_path)
        return True

    def load_image(self, parent):
        self.loaded_image = cv2.imread(self.image_file)

        if self.loaded_image is None:
            QMessageBox.critical(parent, "Error", f"Could not load image file")

        return True


