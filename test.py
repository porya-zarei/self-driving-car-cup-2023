import serial
import RPi.GPIO as GPIO
import cv2 as cv
from image_processing import AprilTagDetector, RoadLinesDetector, TrafficLightDetector
from picamera2 import Picamera2
import time
import matplotlib.pyplot as plt
import apriltag

time.sleep(2)

# ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# ser.reset_input_buffer()

options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options=options)

picam2 = Picamera2()
config = picam2.create_preview_configuration({"format": "YUV420"})
picam2.configure(config)
picam2.start()

april_tag_detector = AprilTagDetector.AprilTagDetector()
road_lines_detector = RoadLinesDetector.RoadLinesDetector()
traffic_light_detector = TrafficLightDetector.TrafficLightDetector()

time.sleep(2)

start_time = 0
end_time = 0

if __name__ == "__main__":
    # setup
    last_error = 0
    prev_error = 0
    prev_april_result = -1
    april_result = -1
    while True:
        # loop
        start_time = time.time()
        image = picam2.capture_array("main")
        image = cv.cvtColor(image, cv.COLOR_YUV420P2RGB)
        
        traffic_light_detector.detect_red(image)
        april_tag_detector.detect(image)
        print(f"april result => {april_tag_detector.tag_id}")
        print(f"traffic light result => {traffic_light_detector.traffic_light_state}")
        # image_shape = image.shape
        # image_middle = (image.shape[0] // 2, image.shape[1] // 2)
        # image = road_lines_detector.frame_drawer(image)
        plt.imshow(image)
        end_time = time.time()
        print(f"time : {end_time - start_time}")
        plt.pause(0.01)
    plt.show()
