import apriltag
import cv2 as cv


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

    def detect(self, image):
        image = self.preprocess(image)
        result = self.detector.detect(image)
        if result is not None and len(result) > 0:
            self.april_results = result
            self.prev_april_result = self.april_result
            self.april_result = result[0]
            self.tag_id = result[0].tag_id
            print(f"result => {self.april_result}")
            return self.april_result
        self.tag_id = -1
        return None
