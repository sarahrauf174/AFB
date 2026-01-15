import numpy as np
import cv2 as cv

class MaskGenerator:
    def __init__(self, img, start_curve, stop_curve):
        self.img = img
        self.start_curve = start_curve
        self.stop_curve = stop_curve

        # =========================
        # Build mask
        # =========================
        H, W = self.img.shape[:2]
        self.mask = np.zeros((H, W), dtype=np.uint8)

        # Build polygon:
        # top curve left→right
        # bottom curve right→left
        polygon = start_curve + stop_curve[::-1]
        polygon = np.array(polygon, dtype=np.int32)

        cv.fillPoly(self.mask, [polygon], 255)

        # =========================
        # Apply mask
        # =========================
        self.masked = cv.bitwise_and(self.img, self.img, mask=self.mask)

