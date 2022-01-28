#!/usr/bin/env python
import cv2
import numpy as np

from pick_color_mask import pick_color_mask
# Bus 002 Device 009: ID 046d:0826 Logitech, Inc. HD Webcam C525
# '/dev/video2'
video_stream = cv2.VideoCapture('/dev/video2')
# initialization
# add here a env file to store the values in XML?
# and run color calibration only on request or if params not present

# lower_threshold = [0, 0, 0]
# upper_threshold = [255, 255, 255]

# picked manually
global lower_threshold, upper_threshold
lower_threshold = [85, 13, 177]
upper_threshold = [108, 97, 223]

# Alternative: call pick_color_mask with initial values
lower_threshold, upper_threshold = pick_color_mask(video_stream,
                                                   lower_threshold,
                                                   upper_threshold)
print("lower limits:", lower_threshold)
print("upper limits:", upper_threshold)


def thresholding(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_threshold, upper_threshold)
    return mask


while True:
    _, frame = video_stream.read()
    frame = cv2.resize(frame, (480, 360))
    # frame = cv2.flip(frame,0 ) # flip vertically to avoid mirror effect

    mask = thresholding(frame)

    cv2.imshow("Output", frame)
    cv2.imshow("Mask", mask)
    cv2.waitKey(1)
