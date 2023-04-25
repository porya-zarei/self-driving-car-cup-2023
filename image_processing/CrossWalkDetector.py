import cv2 as cv
import numpy as np


class CrossWalkDetector:
    def __init__(self, rect_area=100000):
        self.rect_area = rect_area
        self.cross_walk_state = False
    def detect_draw(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, 200, 255, 0)
        contours, hierarchy = cv.findContours(thresh, 1, 2)
        self.cross_walk_state = False
        for cnt in contours:
            x1, y1 = cnt[0][0]
            approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), True)
            if len(approx) == 4:
                x, y, w, h = cv.boundingRect(cnt)
                if w * h > self.rect_area:
                    self.cross_walk_state = True
                    ratio = float(w) / h
                    if ratio >= 0.9 and ratio <= 1.1:
                        img = cv.drawContours(img, [cnt], -1, (0, 255, 255), 3)
                        img = cv.putText(
                            img,
                            "Square",
                            (x1, y1),
                            cv.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (255, 255, 0),
                            2,
                        )
                    else:
                        print(f"founded => {(x,y,w,h)}")
                        img = cv.putText(
                            img,
                            "Rectangle",
                            (x1, y1),
                            cv.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2,
                        )
                        img = cv.drawContours(img, [cnt], -1, (0, 255, 0), 3)
        return img

    def detect(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, 200, 255, 0)
        contours, hierarchy = cv.findContours(thresh, 1, 2)

        for cnt in contours:
            x1, y1 = cnt[0][0]
            approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), True)
            if len(approx) == 4:
                x, y, w, h = cv.boundingRect(cnt)
                if w * h > self.rect_area:
                    self.cross_walk_state = True
                    return True
        self.cross_walk_state = False
        return False

    def region_selection(self, image):
        """
        Determine and cut the region of interest in the input image.
            Parameters:
                image: An np.array compatible with plt.imshow.
        """
        mask = np.zeros_like(image)
        # Defining a 3 channel or 1 channel color to fill the mask with depending on the input image
        if len(image.shape) > 2:
            channel_count = image.shape[2]
            ignore_mask_color = (255,) * channel_count
        else:
            ignore_mask_color = 255
        # We could have used fixed numbers as the vertices of the polygon,
        # but they will not be applicable to images with different dimesnions.
        rows, cols = image.shape[:2]
        # print(f"{rows} , {cols}")
        bottom_left = [1, rows - 1]
        top_left = [1, rows * 0.6]
        bottom_right = [cols - 1, rows - 1]
        top_right = [cols - 1, rows * 0.6]
        vertices = np.array(
            [[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32
        )
        cv.fillPoly(mask, vertices, ignore_mask_color)
        masked_image = cv.bitwise_and(image, mask)
        return masked_image
