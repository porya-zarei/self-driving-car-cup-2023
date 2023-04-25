import matplotlib.pyplot as plt
from picamera2 import *
import numpy as np
import cv2 as cv
import os
import glob
from time import time


class RoadLinesDetector:
    def __init__(
        self,
    ):
        self.steer = 0
        self.middle = 0
        self.img_middle = (240, 320)

    def RGB_color_selection(self, image):
        """
        Apply color selection to RGB images to blackout everything except for white and yellow lane lines.
            Parameters:
                image: An np.array compatible with plt.imshow.
        """
        # White color mask
        lower_threshold = np.uint8([200, 200, 200])
        upper_threshold = np.uint8([255, 255, 255])
        white_mask = cv.inRange(image, lower_threshold, upper_threshold)

        # Yellow color mask
        lower_threshold = np.uint8([175, 175, 0])
        upper_threshold = np.uint8([255, 255, 255])
        yellow_mask = cv.inRange(image, lower_threshold, upper_threshold)

        # Combine white and yellow masks
        mask = cv.bitwise_or(white_mask, yellow_mask)
        masked_image = cv.bitwise_and(image, image, mask=mask)

        return masked_image

    def convert_hsv(self, image):
        """
        Convert RGB images to HSV.
            Parameters:
                image: An np.array compatible with plt.imshow.
        """
        return cv.cvtColor(image, cv.COLOR_RGB2HSV)

    def HSV_color_selection(self, image):
        """
        Apply color selection to the HSV images to blackout everything except for white and yellow lane lines.
            Parameters:
                image: An np.array compatible with plt.imshow.
        """
        # Convert the input image to HSV
        converted_image = self.convert_hsv(image)

        # White color mask
        lower_threshold = np.uint8([0, 0, 210])
        upper_threshold = np.uint8([255, 30, 255])
        white_mask = cv.inRange(converted_image, lower_threshold, upper_threshold)

        # Yellow color mask
        lower_threshold = np.uint8([18, 80, 80])
        upper_threshold = np.uint8([30, 255, 255])
        yellow_mask = cv.inRange(converted_image, lower_threshold, upper_threshold)

        # Combine white and yellow masks
        mask = cv.bitwise_or(white_mask, yellow_mask)
        masked_image = cv.bitwise_and(image, image, mask=mask)

        return masked_image

    def convert_hsl(self, image):
        """
        Convert RGB images to HSL.
            Parameters:
                image: An np.array compatible with plt.imshow.
        """
        return cv.cvtColor(image, cv.COLOR_RGB2HLS)

    def HSL_color_selection(self, image):
        """
        Apply color selection to the HSL images to blackout everything except for white and yellow lane lines.
            Parameters:
                image: An np.array compatible with plt.imshow.
        """
        # Convert the input image to HSL
        converted_image = self.convert_hsl(image)

        # White color mask
        lower_threshold = np.uint8([0, 200, 0])
        upper_threshold = np.uint8([255, 255, 255])
        white_mask = cv.inRange(converted_image, lower_threshold, upper_threshold)

        # Yellow color mask
        lower_threshold = np.uint8([10, 0, 100])
        upper_threshold = np.uint8([40, 255, 255])
        yellow_mask = cv.inRange(converted_image, lower_threshold, upper_threshold)

        # Combine white and yellow masks
        mask = cv.bitwise_or(white_mask, yellow_mask)
        masked_image = cv.bitwise_and(image, image, mask=mask)

        return masked_image

    def gray_scale(self, image):
        """
        Convert images to gray scale.
            Parameters:
                image: An np.array compatible with plt.imshow.
        """
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    def gaussian_smoothing(self, image, kernel_size=13):
        """
        Apply Gaussian filter to the input image.
            Parameters:
                image: An np.array compatible with plt.imshow.
                kernel_size (Default = 13): The size of the Gaussian kernel will affect the performance of the detector.
                It must be an odd number (3, 5, 7, ...).
        """
        return cv.GaussianBlur(image, (kernel_size, kernel_size), 0)

    def canny_detector(self, image, low_threshold=50, high_threshold=150):
        """
        Apply Canny Edge Detection algorithm to the input image.
            Parameters:
                image: An np.array compatible with plt.imshow.
                low_threshold (Default = 50).
                high_threshold (Default = 150).
        """
        return cv.Canny(image, low_threshold, high_threshold)

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
        top_left = [70, rows * 0.7]
        bottom_right = [cols - 1, rows - 1]
        top_right = [cols - 70, rows * 0.7]
        vertices = np.array(
            [[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32
        )
        # cv.circle(image,vertices[0][0],10,(255,0,0),10)
        # cv.circle(image,vertices[0][1],10,(255,0,0),10)
        # cv.circle(image,vertices[0][2],10,(255,0,0),10)
        # cv.circle(image,vertices[0][3],10,(255,0,0),10)
        # print(f" points => {vertices}")
        cv.fillPoly(mask, vertices, ignore_mask_color)
        
        # plt.plot(image)
        masked_image = cv.bitwise_and(image, mask)
        # print(f"{mask} . {image}")
        # plt.imshow(masked_image)
        return masked_image

    def hough_transform(self, image):
        """
        Determine and cut the region of interest in the input image.
            Parameters:
                image: The output of a Canny transform.
        """
        rho = 1  # Distance resolution of the accumulator in pixels.
        theta = np.pi / 180  # Angle resolution of the accumulator in radians.
        threshold = 20  # Only lines that are greater than threshold will be returned.
        minLineLength = 20  # Line segments shorter than that are rejected.
        maxLineGap = (
            300  # Maximum allowed gap between points on the same line to link them
        )
        return cv.HoughLinesP(
            image,
            rho=rho,
            theta=theta,
            threshold=threshold,
            minLineLength=minLineLength,
            maxLineGap=maxLineGap,
        )

    def draw_lines(self, image, lines, color=[255, 0, 0], thickness=2):
        """
        Draw lines onto the input image.
            Parameters:
                image: An np.array compatible with plt.imshow.
                lines: The lines we want to draw.
                color (Default = red): Line color.
                thickness (Default = 2): Line thickness.
        """
        image = np.copy(image)
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(image, (x1, y1), (x2, y2), color, thickness)
        return image

    def average_slope_intercept(self, lines):
        """
        Find the slope and intercept of the left and right lanes of each image.
            Parameters:
                lines: The output lines from Hough Transform.
        """
        left_lines = []  # (slope, intercept)
        left_weights = []  # (length,)
        right_lines = []  # (slope, intercept)
        right_weights = []  # (length,)

        try:
            if len(lines) >= 2:
                for line in lines:
                    for x1, y1, x2, y2 in line:
                        if x1 == x2:
                            continue
                        slope = (y2 - y1) / (x2 - x1)
                        intercept = y1 - (slope * x1)
                        length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
                        if slope < 0:
                            left_lines.append((slope, intercept))
                            left_weights.append((length))
                        else:
                            right_lines.append((slope, intercept))
                            right_weights.append((length))
        except:
            pass

        left_lane = (
            np.dot(left_weights, left_lines) / np.sum(left_weights)
            if len(left_weights) > 0
            else None
        )
        right_lane = (
            np.dot(right_weights, right_lines) / np.sum(right_weights)
            if len(right_weights) > 0
            else None
        )
        return left_lane, right_lane

    def pixel_points(self, y1, y2, line):
        """
        Converts the slope and intercept of each line into pixel points.
            Parameters:
                y1: y-value of the line's starting point.
                y2: y-value of the line's end point.
                line: The slope and intercept of the line.
        """
        if line is None:
            return None
        slope, intercept = line
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        y1 = int(y1)
        y2 = int(y2)
        return ((x1, y1), (x2, y2))

    def lane_lines(self, image, lines):
        """
        Create full lenght lines from pixel points.
            Parameters:
                image: The input test image.
                lines: The output lines from Hough Transform.
        """
        try:
            left_lane, right_lane = self.average_slope_intercept(lines)
            y1 = image.shape[0]
            y2 = y1 * 0.6
            left_line = self.pixel_points(y1, y2, left_lane)
            right_line = self.pixel_points(y1, y2, right_lane)
            print(f"left line => {left_line} , right line => {right_line}")
            middle_y1 = (left_line[0][0] + left_line[1][0]) / 2
            middle_y2 = (right_line[0][0] + right_line[1][0]) / 2
            middle_y = (middle_y1 + middle_y2) / 2
            middle_x = image.shape[0] / 2
            print(f"middle => {(middle_x,middle_y)}")
            return left_line, right_line, (int(middle_x), int(middle_y))
        except:
            return ((0, 0), (0, 0)), ((0, 0), (0, 0)), (0, 0)

    def draw_lane_lines(self, image, lines, color=[255, 0, 0], thickness=12):
        """
        Draw lines onto the input image.
            Parameters:
                image: The input test image.
                lines: The output lines from Hough Transform.
                color (Default = red): Line color.
                thickness (Default = 12): Line thickness.
        """
        line_image = np.zeros_like(image)
        for line in lines:
            if line is not None:
                # print(f"line => {line}")
                cv.line(line_image, *line, color, thickness)
        return cv.addWeighted(image, 1.0, line_image, 1.0, 0.0)

    def frame_processor(self, image):
        """
        Process the input frame to detect lane lines.
            Parameters:
                image: Single video frame.
        """
        color_select = self.HSL_color_selection(image)
        # plt.imshow(color_select)
        gray = self.gray_scale(color_select)
        # plt.imshow(gray)
        smooth = self.gaussian_smoothing(gray)
        # plt.imshow(smooth)
        edges = self.canny_detector(smooth)
        # plt.imshow(edges)
        region = self.region_selection(edges)
        # plt.imshow(region)
        hough = self.hough_transform(region)
        # print(hough)
        result = self.lane_lines(image, hough)
        self.middle = result[2]
        return result

    def frame_drawer(self, image):
        left_line, right_line, middle_point = self.frame_processor(image)
        print(f"l => {left_line} , r => {right_line}")
        result = self.draw_lane_lines(image, (left_line, right_line))
        result = cv.circle(
            result, (middle_point[1], middle_point[0]), 10, (0, 0, 255), -1
        )
        result = cv.circle(
            result,
            (int(image.shape[1] / 2), int(image.shape[0] / 2)),
            10,
            (0, 255, 255),
            -1,
        )
        return result

    def get_steer(self):
        if self.middle[0] != 0:
            self.steer = (((self.middle[1] - self.img_middle[1]) * 0.5) // 5) * 5
            print(f"last error => {self.steer}")
        return self.steer
