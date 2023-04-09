import serial
import RPi.GPIO as GPIO
import cv2 as cv
import imageprcessing
from picamera2 import Picamera2
import time
import matplotlib.pyplot as plt
import apriltag

time.sleep(2)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector()

picam2 = Picamera2()
config = picam2.create_preview_configuration({"format":"YUV420"})
picam2.configure(config)
picam2.start()

time.sleep(2)

def apriltag_detector(image):
    gray = cv.cvtColor(image,cv.COLOR_RGB2GRAY)
    result = detector.detect(gray)
    if result is not None and len(result) > 0:
        print(f"result => {result[0].tag_id}")
        return result[0].tag_id
    return None

def serial_send(steer,tag_id):
    data = f"{steer},{tag_id}".encode()
    ser.write(data)

def serial_read():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        return line
    else:
        return None

# ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# ser.reset_input_buffer()

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
        image = cv.cvtColor(image,cv.COLOR_YUV420P2RGB)
        prev_april_result = april_result
        april_result = apriltag_detector(image)
        if april_result is None:
            april_result = -1
        print(f"april result => {april_result}")
        image_shape = image.shape
        image_middle = (image.shape[0]//2,image.shape[1]//2)
        # plt.imshow(image)
        left_line,right_line,middle = imageprcessing.frame_processor(image)
        # image = imageprcessing.frame_drawer(image)
        # plt.imshow(image)
        # plt.pause(0.03)
        print(f"image middle => {image_middle} , middle => {middle}")
        
        if middle[0] != 0:
            prev_error = last_error
            last_error = (((middle[1] - image_middle[1]) * 0.5)//5 ) * 5
            print(f"last error => {last_error}")

        serial_send(last_error,april_result)
        
        data = serial_read()
        if data is not None:
            print(f"data arrived => --{data}--")
        
        end_time = time.time()
        # time.sleep(0.1)
        print(f"time : {end_time - start_time}")
    # plt.show()

# if __name__ == "__main__":
#     # setup
#     last_error = 0
#     prev_error = 0
#     prev_april_result = -1
#     april_result = -1 
#     while True:
#         # loop
#         start_time = time.time()
#         image = picam2.capture_array("main")
#         image = cv.cvtColor(image,cv.COLOR_YUV420P2RGB)
#         prev_april_result = april_result
#         april_result = apriltag_detector(image)
#         if april_result is None:
#             april_result = -1
#         print(f"april result => {april_result}")
#         image_shape = image.shape
#         image_middle = (image.shape[0]//2,image.shape[1]//2)
#         image = imageprcessing.frame_drawer(image)
#         plt.imshow(image)
#         plt.pause(0.03)

#         end_time = time.time()
#         # time.sleep(0.1)
#         print(f"time : {end_time - start_time}")
#     # plt.show()
