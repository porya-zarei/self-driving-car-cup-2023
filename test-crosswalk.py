import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_processing import CrossWalkDetector

img = cv2.imread("./data/crosswalk.jpg")

cw_detector = CrossWalkDetector.CrossWalkDetector()
cw_detector.detect(img)
print(f"cw => {cw_detector.cross_walk_state}")

cv2.imshow("test",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
