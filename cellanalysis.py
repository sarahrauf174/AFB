import cv2
import numpy as np


class CellAnalysis:
    def __init__(self, img, blur, enhance, thresh, min_area, max_area):
        self.img = img
        self.blur = blur
        self.enhance = enhance
        self.thresh = thresh
        self.min_area = min_area
        self.max_area = max_area



    def run(self):
        if len(self.img.shape) == 2:
            gray = self.img.copy()
        else:
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (self.blur, self.blur), 0)
        _, thresh = cv2.threshold(blurred, self.thresh, 255, cv2.THRESH_BINARY)
        (self.numlabels, self.labels, self.stats, self.centroids) = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)
        self.output = np.zeros(gray.shape, dtype="uint8")

        self.data = []

        for i in range(1, self.numlabels):
            area = self.stats[i, cv2.CC_STAT_AREA]
            x_cord = self.stats[i, cv2.CC_STAT_LEFT]
            y_cord = self.stats[i, cv2.CC_STAT_TOP]
            h = self.stats[i, cv2.CC_STAT_HEIGHT]
            w = self.stats[i, cv2.CC_STAT_WIDTH]
            cx, cy = self.centroids[i]

            if self.min_area < area < self.max_area:
                self.data.append([i, area, x_cord, y_cord, h, w, cx, cy])
                mask = (self.labels == i).astype("uint8") * 255
                self.output = cv2.bitwise_or(self.output, mask)

        return self.output

    def get_data(self):
        if not hasattr(self, "data"):
            raise RuntimeError("CellAnalysis.run() must be called first")

        self.area_stat = []

        areas = [row[1] for row in self.data]

        if not areas:
            self.area_stat = [0,0,0,0,0]
            return

        cell_count = len(areas)
        mean_area = np.mean(areas)
        min_area = np.min(areas)
        max_area = np.max(areas)
        sd_area = np.std(areas)

        self.area_stat = [cell_count, mean_area, min_area, max_area, sd_area]



