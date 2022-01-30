#!/usr/bin/env python

import cv2
import numpy as np

from pick_color_mask import pick_color_mask

from djitellopy import tello

# Initialization
# drone

drone = tello.Tello()
drone.connect()

# Explore library in:
# ./myvenv/lib/python3.8/site-packages/djitellopy/tello.py

print(drone.get_battery())

drone.streamon()
drone.takeoff()

# variables

# isframe True for testing on still photos
# False to run on stream from video source

global isframe
isframe = True

# reduced size of images for processing
global frame_width, frame_height
frame_width = 480
frame_height = 360

# video source
# list available cameras with:
# $ v4l2-ctl --list-devices
# USB camera on laptop: '/dev/video2'
# integrated laptop cam: 0
video_stream = cv2.VideoCapture('/dev/video2')
video_stream = cv2.VideoCapture(0)

# color thresholds

# add an env file to store the values in XML?
# read values from XML and run color calibration
# only on request or if XML params not present
global lower_threshold, upper_threshold
lower_threshold = [0, 0, 0]
upper_threshold = [255, 255, 255]

# picked manually
# values for Cossio
lower_threshold = [85, 13, 177]
upper_threshold = [108, 97, 223]
# values for Durruti
lower_threshold = [25, 10, 179]
upper_threshold = [117,  54, 255]

# Call pick_color_mask to fine-tune initial values
lower_threshold, upper_threshold = pick_color_mask(video_stream,
                                                   lower_threshold,
                                                   upper_threshold)
# display final values
print("lower_threshold = ", lower_threshold)
print("upper_threshold = ", upper_threshold)

sensors = 3
threshold_value = .20
trans_gain = .33  # the higher the more sensitive
rota_gain = [-25, -15, 0, 15, 25]
yaw = 0
fwd_speed = 15

# Functions definition


def thresholding(frame, lower_threshold, upper_threshold):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv, lower_threshold, upper_threshold)
    return mask


def get_contours(mask, frame):
    GREEN = (0, 255, 0)
    PINK = (255, 0, 255)
    RED = (0, 0, 255)
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    largest_area_detected = max(contours, key=cv2.contourArea)
    x_r, y_r, w_r, h_r = cv2.boundingRect(largest_area_detected)
    cx = x_r + w_r//2
    cy = y_r + h_r//2
    cv2.drawContours(frame, largest_area_detected, -1, PINK, 3)
    cv2.circle(frame, (cx, cy), 5, GREEN, cv2.FILLED)
    cv2.rectangle(frame, (x_r, y_r), (x_r+w_r, y_r+h_r), RED, 2)

    return cx


def get_sensor_output(mask, sensors):
    # Note: hsplit only works if frame_width is divisible by sensors
    areas = np.hsplit(mask, sensors)

    pix_total = areas[0].shape[0]*areas[0].shape[1]//sensors
    sens_out = []
    for i, area in enumerate(areas):
        pix_count = cv2.countNonZero(area)
        if pix_count > threshold_value * pix_total:
            sens_out.append(1)
            win_title = str(i)+": 1"
        else:
            sens_out.append(0)
            win_title = str(i)+": 0"
        cv2.imshow(win_title, area)
    print(sens_out)
    return sens_out


def send_commands(sens_out, cx):
    global curve
    # translation
    left_right = (cx - frame_width/2) * trans_gain
    left_right = int(np.clip(left_right, -10, 10))
    if left_right > -2 and left_right < 2:
        left_right = 0

    # rotation
    if sens_out == [1, 0, 0]:
        yaw = rota_gain[0]
    elif sens_out == [1, 1, 0]:
        yaw = rota_gain[1]
    elif sens_out == [0, 1, 0]:
        yaw = rota_gain[2]
    elif sens_out == [0, 1, 1]:
        yaw = rota_gain[3]
    elif sens_out == [0, 0, 1]:
        yaw = rota_gain[4]
    else:
        yaw = 0

    drone.send_rc_control(left_right, fwd_speed, 0, yaw)


# main loop
while True:

    # get frame
    if isframe:
        frame = cv2.imread('./assets/data/IMG_7733_xs.PNG')
    else:
        frame = drone.get_frame_read().frame

    # resize
    frame = cv2.resize(frame, (frame_width, frame_height))
    frame = cv2.flip(frame, 0)  # flip vertically to avoid mirror effect

    mask = thresholding(frame, lower_threshold, upper_threshold)
    cx = get_contours(mask, frame)  # for translation
    sens_out = get_sensor_output(mask, sensors)  # for rotation
    send_commands(sens_out, cx)

    # show images
    cv2.imshow("Output", frame)
    cv2.imshow("Mask", mask)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    drone.streamoff()
    cv2.destroyAllWindows()
