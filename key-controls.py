#!/usr/bin/env python

from djitellopy import tello
import keypress_module as kp
from time import sleep

kp.init()

drone = tello.Tello()
drone.connect()

print(drone.get_battery())


def get_keyboard_input():
    # (L/R, bk/fwd, up/down, clock/counterclock-wise yaw) each in -/+100%
    left_right = 0
    bk_fwd = 0
    down_up = 0
    c_cc_yaw = 0
    speed = 50

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
        c_cc_yaw = -speed
    elif kp.is_key_pressed('a'):
        c_cc_yaw = speed

    return [left_right, bk_fwd, down_up, c_cc_yaw]


# wait for RETURN to take off

while True:
    if kp.is_key_pressed('RETURN') is True:
        break
drone.takeoff()

while True:
    commands = get_keyboard_input()
    drone.send_rc_control(
        commands[0],
        commands[1],
        commands[2],
        commands[3])
    sleep(0.05)
