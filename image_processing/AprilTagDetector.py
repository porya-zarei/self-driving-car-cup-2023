import apriltag
import cv2 as cv
import numpy as np

class AprilTagDetector:
    def __init__(self):
        options = apriltag.DetectorOptions(families="tag36h11")
        self.detector = apriltag.Detector(options=options)
        self.april_result = None
        self.prev_april_result = None
        self.april_results = []
        self.tag_id = -1

    def preprocess(self, image):
        return cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    def get_tag_area(self,tag):
        corners = tag.corners.astype(int)
        # Use the shoelace formula to calculate the area of the tag in pixels
        return (0.5 * abs(np.dot(corners[:,0], np.roll(corners[:,1],1)) - np.dot(corners[:,1], np.roll(corners[:,0],1))))

    def detect(self, image):
        image = self.preprocess(image)
        result = self.detector.detect(image)
        if result is not None and len(result) > 0:
            self.april_results = result
            self.prev_april_result = self.april_result
            self.april_result = result[0]
            tag_area = self.get_tag_area(result[0])
            print(f"tag area => {tag_area}")
            if tag_area > 14000:
                self.tag_id = result[0].tag_id
            else:
                self.tag_id = -1
                self.april_result = None
                self.april_results = []
        else:
            self.tag_id = -1
            self.april_result = None
            self.april_results = []
        # print(f"result => {self.tag_id}")
        return self.april_result
