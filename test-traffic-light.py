import cv2 as cv
import time
import matplotlib.pyplot as plt
from image_processing import TrafficLightDetector

traffic_light_detector = TrafficLightDetector.TrafficLightDetector()

start_time = 0
end_time = 0

if __name__ == "__main__":
    # setup
    img = cv.imread("./data/tf2.jpg")
    while True:
        # loop
        start_time = time.time()
        image = img
        # image = cv.cvtColor(image, cv.COLOR_YUV420P2RGB)
        traffic_light_detector.detect_red(image)
        print(f"traffic light result => {traffic_light_detector.traffic_light_state} , {traffic_light_detector.traffic_lights}")
        for c in traffic_light_detector.traffic_lights:
            image = cv.circle(image,c["center"],20,(200,0,0),3)
        # cv.imshow("img",image)
        plt.imshow(image)
        plt.pause(0.1)
        end_time = time.time()
        print(f"time : {end_time - start_time}")
        cv.waitKey(0)
