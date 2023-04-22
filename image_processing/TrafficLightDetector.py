import os
import cv2 as cv
import numpy as np


class TrafficLightDetector:
    def __init__(self):
        self.traffic_light_state = -1
        self.traffic_lights = []

    def detect(self, image):
        font = cv.FONT_HERSHEY_SIMPLEX
        img = image
        cimg = img
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # color range
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        lower_green = np.array([40, 50, 50])
        upper_green = np.array([90, 255, 255])
        lower_yellow = np.array([15, 150, 150])
        upper_yellow = np.array([35, 255, 255])
        mask1 = cv.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv.inRange(hsv, lower_red2, upper_red2)
        maskg = cv.inRange(hsv, lower_green, upper_green)
        masky = cv.inRange(hsv, lower_yellow, upper_yellow)
        maskr = cv.add(mask1, mask2)
        size = img.shape
        # print size
        # hough circle detect
        r_circles = cv.HoughCircles(
            maskr,
            cv.HOUGH_GRADIENT,
            1,
            80,
            param1=50,
            param2=10,
            minRadius=0,
            maxRadius=30,
        )
        g_circles = cv.HoughCircles(
            maskg,
            cv.HOUGH_GRADIENT,
            1,
            60,
            param1=50,
            param2=10,
            minRadius=0,
            maxRadius=30,
        )

        y_circles = cv.HoughCircles(
            masky,
            cv.HOUGH_GRADIENT,
            1,
            30,
            param1=50,
            param2=5,
            minRadius=0,
            maxRadius=30,
        )
        # traffic light detect
        founded_lights = []
        r = 5
        bound = 4.0 / 10
        if r_circles is not None:
            r_circles = np.uint16(np.around(r_circles))
            print(f"red => {r_circles}")
            for i in r_circles[0, :]:
                print(f"i => {i}")
                # if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                #     continue

                h, s = 0.0, 0.0
                for m in range(-r, r):
                    for n in range(-r, r):
                        if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:
                            continue
                        h += maskr[i[1] + m, i[0] + n]
                        s += 1
                print(f"h,s => {h/s} {h} {s}")
                if h / s > 50:
                    # cv.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                    # cv.circle(maskr, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                    # cv.putText(cimg,'RED',(i[0], i[1]), font, 1,(255,0,0),2,cv.LINE_AA)
                    founded_lights.append({"type": "RED", "center": (i[0], i[1])})

        if g_circles is not None:
            g_circles = np.uint16(np.around(g_circles))

            for i in g_circles[0, :]:
                if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                    continue

                h, s = 0.0, 0.0
                for m in range(-r, r):
                    for n in range(-r, r):
                        if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:
                            continue
                        h += maskg[i[1] + m, i[0] + n]
                        s += 1
                if h / s > 100:
                    # cv.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                    # cv.circle(maskg, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                    # cv.putText(cimg,'GREEN',(i[0], i[1]), font, 1,(255,0,0),2,cv.LINE_AA)
                    founded_lights.append({"type": "GREEN", "center": (i[0], i[1])})

        if y_circles is not None:
            y_circles = np.uint16(np.around(y_circles))

            for i in y_circles[0, :]:
                if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                    continue

                h, s = 0.0, 0.0
                for m in range(-r, r):
                    for n in range(-r, r):
                        if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:
                            continue
                        h += masky[i[1] + m, i[0] + n]
                        s += 1
                if h / s > 50:
                    # cv.circle(cimg, (i[0], i[1]), i[2] + 10, (0, 255, 0), 2)
                    # cv.circle(masky, (i[0], i[1]), i[2] + 30, (255, 255, 255), 2)
                    # cv.putText(
                    #     cimg,
                    #     "YELLOW",
                    #     (i[0], i[1]),
                    #     font,
                    #     1,
                    #     (255, 0, 0),
                    #     2,
                    #     cv.LINE_AA,
                    # )
                    founded_lights.append({"type": "YELLOW", "center": (i[0], i[1])})
        return founded_lights

    def detect_red(self, image):
        img = image
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # color range
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv.inRange(hsv, lower_red2, upper_red2)
        maskr = cv.add(mask1, mask2)
        size = img.shape

        r_circles = cv.HoughCircles(
            maskr,
            cv.HOUGH_GRADIENT,
            1,
            80,
            param1=50,
            param2=10,
            minRadius=0,
            maxRadius=30,
        )
        # traffic light detect
        founded_lights = []
        r = 5
        bound = 4.0 / 10

        if r_circles is not None:
            r_circles = np.uint16(np.around(r_circles))
            for i in r_circles[0, :]:
                # if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                #     continue
                h, s = 0.0, 0.0
                for m in range(-r, r):
                    for n in range(-r, r):
                        if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:
                            continue
                        h += maskr[i[1] + m, i[0] + n]
                        s += 1
                if h / s > 50:
                    # cv.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                    # cv.circle(maskr, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                    # cv.putText(cimg,'RED',(i[0], i[1]), font, 1,(255,0,0),2,cv.LINE_AA)
                    founded_lights.append({"type": "RED", "center": (i[0], i[1])})
        if len(founded_lights) > 0:
            self.traffic_light_state = 2
        else:
            self.traffic_light_state = -1
        self.traffic_lights = founded_lights
        return founded_lights
