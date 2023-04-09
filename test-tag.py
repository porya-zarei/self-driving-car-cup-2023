from picamera2 import *
import cv2 as cv
import time
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import apriltag

picam2 = Picamera2()
config = picam2.create_preview_configuration({"format":"YUV420"})
picam2.configure(config)
picam2.start()
time.sleep(1)

image = picam2.capture_array("main")

image = cv.cvtColor(image,cv.COLOR_YUV420P2RGB)
gray = cv.cvtColor(image,cv.COLOR_RGB2GRAY)
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector()
result = detector.detect(gray)
print(f"result => {result[0].tag_id}")

plt.imshow(gray)
plt.show()