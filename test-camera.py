from picamera2 import *
import cv2 as cv
import time
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

picam2 = Picamera2()
config = picam2.create_preview_configuration({"format":"YUV420"})
picam2.configure(config)
picam2.start()
time.sleep(1)

image = picam2.capture_array("main")

image_rgb = cv.cvtColor(image,cv.COLOR_YUV420P2RGB)

cv.imwrite("test.jpg",image_rgb)

image = np.array(image)
print(f"image => {image.shape}")

plt.imshow(image)
plt.show()