import serial

# import RPi.GPIO as GPIO
import cv2 as cv
from image_processing import AprilTagDetector, RoadLinesDetector, TrafficLightDetector, CrossWalkDetector
from picamera2 import Picamera2
import time
import apriltag

time.sleep(2)

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
ser.reset_input_buffer()

options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector()

picam2 = Picamera2()
config = picam2.create_preview_configuration({"format": "YUV420"})
picam2.configure(config)
picam2.start()

april_tag_detector = AprilTagDetector.AprilTagDetector()
road_lines_detector = RoadLinesDetector.RoadLinesDetector()
traffic_light_detector = TrafficLightDetector.TrafficLightDetector()
cross_walk_detector = CrossWalkDetector.CrossWalkDetector()


time.sleep(1)


def serial_send(steer, tag_id, traffic_light_state,cross_walk_state):
    data = f"{steer},{tag_id},{traffic_light_state},{cross_walk_state}".encode()
    print(f"serial data => {data}")
    ser.write(data)


def serial_read():
    if ser.in_waiting > 0:
        line = ser.readline().decode("utf-8").rstrip()
        return line
    else:
        return None


def get_image_middle(image):
    return (image.shape[0] // 2, image.shape[1] // 2)


def main():
    # setup
    start_time = 0
    end_time = 0

    last_error = 0
    prev_error = 0

    while True:
        # loop
        start_time = time.time()

        image = picam2.capture_array("main")
        image = cv.cvtColor(image, cv.COLOR_YUV420P2RGB)

        traffic_light_detector.detect_red(image)

        april_tag_detector.detect(image)
        
        cross_walk_detector.detect(image)

        image_middle = get_image_middle(image)

        left_line, right_line, middle = road_lines_detector.frame_processor(image)

        # print(f"image middle => {image_middle} , middle => {middle}")

        if middle[0] != 0:
            prev_error = last_error
            last_error = (((middle[1] - image_middle[1]) * 0.3) // 1) * 1
            # print(f"last error => {last_error}")

        serial_send(
            last_error,
            april_tag_detector.tag_id,
            traffic_light_detector.traffic_light_state,
            int(cross_walk_detector.cross_walk_state)
        )

        data = serial_read()
        if data is not None:
            print(f"data arrived => --{data}--")

        end_time = time.time()

        print(f"time : {end_time - start_time}")


if __name__ == "__main__":
    # plt.show()
    main()
