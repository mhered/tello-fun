#!/usr/bin/env python

import cv2
import numpy as np

from pick_color_mask import pick_color_mask


# initialization

global isframe
isframe = False


# list devices with: $ v4l2-ctl --list-devices
# USB camera on laptop: '/dev/video2'
video_stream = cv2.VideoCapture('/dev/video2')
video_stream = cv2.VideoCapture(0)

# initialization
# add here a env file to store the values in XML?
# and run color calibration only on ren XML?
# and run  if params not present
# lower_threshold = [0, 0, 0]
# upper_threshold = [255, 255, 255]

# picked manually
global lower_threshold, upper_threshold

# values for Cossio
lower_threshold = [85, 13, 177]
upper_threshold = [108, 97, 223]
# values for Durruti
lower_threshold = [25, 10, 179]
upper_threshold = [117,  54, 255]

# Alternative: call pick_color_mask with initial values
lower_threshold, upper_threshold = pick_color_mask(video_stream,
                                                   lower_threshold,
                                                   upper_threshold)
print("lower_threshold = ", lower_threshold)
print("upper_threshold = ", upper_threshold)

# functions definition


def thresholding(frame):
    mask = cv2.inRange(frame, lower_threshold, upper_threshold)
    return mask


def get_contours(mask, frame):

    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    largest_area_detected = max(contours, key=cv2.contourArea)
    x, y, width, height = cv2.boundingRect(largest_area_detected)
    cx = x + width//2
    cy = y + height//2
    cv2.drawContours(frame, largest_area_detected, -1, (255, 0, 255), 7)
    cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(frame, (x, y), (x+width, y+height), 3, (0, 0, 255))

    return cx


# main loop

while True:
    if isframe:
        frame = cv2.imread('./assets/data/IMG_7733_xs.PNG')
        frame_width = 480
        frame_height = 360
        frame = cv2.resize(frame, (frame_width, frame_height))

    else:
        _, frame = video_stream.read()

    frame = cv2.resize(frame, (480, 360))
    # frame = cv2.flip(frame,0 ) # flip vertically to avoid mirror effect

    mask = thresholding(frame)
    cx = get_contours(mask, frame)  # for translation

    cv2.imshow("Output", frame)
    cv2.imshow("Mask", mask)
    cv2.waitKey(1)
