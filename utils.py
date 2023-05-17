#!/usr/bin/env python

import os
from time import sleep
import datetime
import cv2
from djitellopy import tello
from icon_overlay import icon_overlay


def countdown(n):
    os.system('spd-say "Stand by"')
    sleep(2)
    for i in range(n):
        msg = f'spd-say "{str(n-i)}"'
        os.system(msg)
        sleep(1)
    os.system('spd-say "Take off!"')
    sleep(1)


def process_frame(frame, text_bat):
    # resize
    # frame = cv2.resize(frame, (360, 240))
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = .35
    thickness = 1  # in pixels
    color = (0.0, 255.0, 255.0)  # Yellow in BGR

    # battery status
    loc_bat = (290, 223)

    battery_icon = cv2.imread('./assets/icons/battery.png', -1)
    frame = icon_overlay(frame, battery_icon,
                         [200, 283], color, [40, 40])

    frame = cv2.putText(frame, text_bat, loc_bat, font,
                        font_scale, color, thickness, cv2.LINE_AA)

    # datestamp
    loc_date = (10, 223)  # in pixels
    text_date = f"{datetime.datetime.now().isoformat(timespec='milliseconds')}"
    frame = cv2.putText(frame, text_date, loc_date, font,
                        font_scale, color, thickness, cv2.LINE_AA)

    return frame


def reduce_frame(img, desired_shape):
    scale = min(
        desired_shape[0]/img.shape[0], desired_shape[1]/img.shape[1])
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    print(f"Scaled to {scale} so resized to {resized_img.shape}")
    return resized_img
