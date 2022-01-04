#!/usr/bin/env python

import cv2
from djitellopy import tello
import keypress_module as kp
import time


def get_keyboard_input():
    # (L/R, bk/fwd, up/down, clock/counterclock-wise yaw) each in -/+100%
    left_right = 0
    bk_fwd = 0
    down_up = 0
    cc_c_yaw = 0
    speed = 50

    if kp.is_key_pressed('RETURN'):
        drone.takeoff()

    if kp.is_key_pressed('q'):
        drone.land()

    if kp.is_key_pressed('LEFT'):
        left_right = -speed
    elif kp.is_key_pressed('RIGHT'):
        left_right = speed

    if kp.is_key_pressed('DOWN'):
        bk_fwd = -speed
    elif kp.is_key_pressed('UP'):
        bk_fwd = speed

    if kp.is_key_pressed('s'):
        down_up = -speed
    elif kp.is_key_pressed('w'):
        down_up = speed

    if kp.is_key_pressed('d'):
        cc_c_yaw = speed
    elif kp.is_key_pressed('a'):
        cc_c_yaw = -speed

    return [left_right, bk_fwd, down_up, cc_c_yaw]


def process_frame(frame):
    # resize & mirror
    frame_xs = cv2.resize(frame, (360, 240))
    return frame_xs


# initializations
# gamepy window to capture keystrokes
kp.init()
# tello drone
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
# start streaming
drone.streamon()

# main loop
while True:
    # move drone
    commands = get_keyboard_input()

    drone.send_rc_control(
        commands[0],
        commands[1],
        commands[2],
        commands[3])

    # get frame
    frame = drone.get_frame_read().frame
    # display processed frame
    cv2.imshow("Frame", process_frame(frame))
    cv2.waitKey(1)

drone.streamoff()
cv2.destroyAllWindows()
