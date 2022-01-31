#!/usr/bin/env python

import cv2
import numpy as np

from djitellopy import tello
from pick_color_mask import pick_color_mask, get_frame, reduce_frame

import os
from time import sleep

# Functions definition


def thresholding(frame, lower_threshold, upper_threshold):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv, lower_threshold, upper_threshold)
    return mask


def get_contours(mask, frame):
    GREEN = (0, 255, 0)
    PINK = (255, 0, 255)
    RED = (0, 0, 255)

    cx = 0
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        largest_area_detected = max(contours, key=cv2.contourArea)
        x_r, y_r, w_r, h_r = cv2.boundingRect(largest_area_detected)
        cx = x_r + w_r//2
        cy = y_r + h_r//2
        cv2.drawContours(frame, largest_area_detected, -1, PINK, 3)
        cv2.circle(frame, (cx, cy), 5, GREEN, cv2.FILLED)
        cv2.rectangle(frame, (x_r, y_r), (x_r+w_r, y_r+h_r), RED, 2)

    return cx


def get_sensor_output(mask, SENSORS):
    # Note: hsplit only works if frame_width is divisible by SENSORS
    areas = np.hsplit(mask, SENSORS)

    pix_total = areas[0].shape[0]*areas[0].shape[1]//SENSORS
    sens_out = []
    for i, area in enumerate(areas):
        pix_count = cv2.countNonZero(area)
        if pix_count > THRESHOLD * pix_total:
            sens_out.append(1)
            win_title = str(i)+": 1"
        else:
            sens_out.append(0)
            win_title = str(i)+": 0"
        cv2.imshow(win_title, area)
    print(sens_out)
    return sens_out


def send_commands(sens_out, cx):
    global TRANS_GAIN, ROTA_GAIN, FWD_SPEED
    # translation
    left_right = (cx - frame_width/2) * TRANS_GAIN
    left_right = int(np.clip(left_right, -10, 10))
    if left_right > -2 and left_right < 2:
        left_right = 0

    # rotation
    fwd_speed = FWD_SPEED
    if sens_out == [1, 0, 0]:
        yaw = ROTA_VALS[0]
    elif sens_out == [1, 1, 0]:
        yaw = ROTA_VALS[1]
    elif sens_out == [0, 1, 0]:
        yaw = ROTA_VALS[2]
        fwd_speed = 0
    elif sens_out == [0, 1, 1]:
        yaw = ROTA_VALS[3]
    elif sens_out == [0, 0, 1]:
        yaw = ROTA_VALS[4]
    else:
        yaw = 0
        fwd_speed = 0

    drone.send_rc_control(left_right, fwd_speed, 0, yaw)


def countdown(n):
    os.system('spd-say "Stand by"')
    sleep(2)
    for i in range(n):
        msg = f'spd-say "{str(n-i)}"'
        os.system(msg)
        sleep(1)
    os.system('spd-say "Take off!"')
    sleep(1)


if __name__ == "__main__":

    # Initialization of variables

    # reduced size of images for processing
    frame_width = 360
    frame_height = 240

    THRESHOLD = .20  # % of detection in area to set to 1
    TRANS_GAIN = .33  # translation gain, the higher the more sensitive
    SENSORS = 3  # number of areas for track sensing
    ROTA_VALS = [-25, -15, 0, 15, 25]  # rotation gain, match with SENSORS
    FWD_SPEED = 15  # default fwd speed

    # video_source = "STATIC" for testing on still photos
    # video_source = "WEBCAM" for testing on stream from video source
    # video_source = "DRONE" for testing on Tello drone

    video_source = "DRONE"

    # Initialization
    if video_source == "WEBCAM":
        # list of available cameras with:
        # $ v4l2-ctl --list-devices
        # USB camera on laptop: '/dev/video2'
        # integrated laptop cam: 0
        video_stream = cv2.VideoCapture('/dev/video2')
        video_stream = cv2.VideoCapture(0)
        video_link = video_stream
    elif video_source == "DRONE":
        drone = tello.Tello()
        drone.connect()
        print(f"Battery: {drone.get_battery()}%")
        drone.streamon()
        video_link = drone
    elif video_source == "STATIC":
        IMAGE_PATH = './assets/data/IMG_7733_xs.PNG'
        video_link = IMAGE_PATH
    else:
        print(f"Video Source: {video_source} not recognized.")

    # color thresholds

    # add an env file to store the values in XML?
    # read values from XML and run color calibration
    # only on request or if XML params not present
    # HSV values for no filter
    """
    lower_threshold = [0, 0, 0]
    upper_threshold = [179, 255, 255]
    """

    # picked manually
    # HSV values for Cossio
    """
    lower_threshold = [85, 13, 177]
    upper_threshold = [108, 97, 223]
    """

    # HSV values for Durruti
    """
    lower_threshold = [25, 10, 179]
    upper_threshold = [117,  54, 255]
    """
    # HSV values from Tello for Durruti - night
    lower_threshold = [94,   0, 189]
    upper_threshold = [179, 255, 255]

    # Call pick_color_mask to fine-tune initial values
    lower_threshold, upper_threshold = pick_color_mask(
        video_source, video_link, (frame_width, frame_height),
        lower_threshold, upper_threshold)

    # display final values
    print("lower_threshold = ", lower_threshold)
    print("upper_threshold = ", upper_threshold)

    if video_source == "DRONE":
        countdown(5)
        drone.takeoff()

    # main loop
    while True:

        # get frame
        frame = get_frame(video_source, video_link)

        # resize
        frame = reduce_frame(frame, frame_size)
        frame_width, frame_height, _ = frame.shape

        mask = thresholding(frame, lower_threshold, upper_threshold)
        cx = get_contours(mask, frame)  # for translation
        sens_out = get_sensor_output(mask, SENSORS)  # for rotation
        send_commands(sens_out, cx)

        # show images
        cv2.imshow("Output", frame)
        cv2.imshow("Mask", mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if video_source == "DRONE":
            drone.land
            drone.streamoff()
            drone.end()
        cv2.destroyAllWindows()
