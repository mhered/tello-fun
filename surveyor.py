#!/usr/bin/env python

import cv2
from djitellopy import tello
import keypress_module as kp
import time
import datetime
from icon_overlay import icon_overlay


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

    if kp.is_key_pressed('p'):
        cv2.imwrite(f'./assets/images/PIC{time.time()}.jpg', frame)
        time.sleep(0.3)

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


def process_frame(frame, drone):
    # resize
    frame = cv2.resize(frame, (360, 240))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = .35
    thickness = 1  # in pixels
    color = (0, 255, 0)  # Green in BGR

    # battery
    loc_bat = (290, 225)
    text_bat = f"{drone.get_battery()}%"

    bat_icon_url = './assets/icons/battery2.png'
    ovl_bat = icon_overlay(bat_icon_url, 40,
                           [201, 283], frame.shape, 1)

    # frame[:, :, 3] = 1-ovl_bat[:, :, 3]
    cv2.addWeighted(ovl_bat, 1.0, frame, 1.0, 0.0, frame)

    frame = cv2.putText(frame, text_bat, loc_bat, font,
                        font_scale, color, thickness, cv2.LINE_AA)

    # datestamp
    loc_date = (10, 225)  # in pixels
    text_date = f"{datetime.datetime.now().isoformat(timespec='milliseconds')}"
    frame = cv2.putText(frame, text_date, loc_date, font,
                        font_scale, color, thickness, cv2.LINE_AA)

    return frame


if __name__ == "__main__":

    # initializations
    # gamepy window to capture keystrokes
    kp.init()
    # tello drone
    drone = tello.Tello()
    drone.connect()
    # start streaming
    drone.streamon()
    global frame

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
        cv2.imshow("Frame", process_frame(frame, drone))
        cv2.waitKey(1)

    drone.streamoff()
    cv2.destroyAllWindows()
