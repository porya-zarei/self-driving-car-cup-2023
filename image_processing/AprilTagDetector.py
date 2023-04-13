import apriltag
import cv2 as cv


class AprilTagDetector:
    def __init__(self):
        self.options = apriltag.DetectorOptions(families="tag36h11")
        self.detector = apriltag.Detector()

    def preprocess(self, image):
        return cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    def detect(self, image):
        image = self.preprocess(image)
        result = self.detector.detect(image)
        if result is not None and len(result) > 0:
            print(f"result => {result[0].tag_id}")
            return result[0]
        return None

    def detect_id(self, image):
        result = self.detect(image)
        if result is not None:
            return result.tag_id
        return result
