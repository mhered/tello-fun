#!/usr/bin/env python

import cv2
import numpy as np


def icon_overlay(icon_url, icon_size, icon_position, frame_shape, color):

    icon = cv2.imread(icon_url)
    icon = cv2.resize(icon, (icon_size, icon_size))
    icon = cv2.cvtColor(icon, cv2.COLOR_BGR2BGRA)
    icon_h, icon_w, icon_c = icon.shape
    ovlay_h, ovlay_w, ovlay_c = frame_shape

    overlay = np.zeros((ovlay_h, ovlay_w, 4), dtype='uint8')
    for i in range(0, icon_h):
        for j in range(0, icon_w):
            shifted_i = icon_position[0]+i
            shifted_j = icon_position[1]+j
            if shifted_i < ovlay_h and shifted_j < ovlay_w:
                if icon[i, j][3] != 0:
                    overlay[icon_position[0]+i,
                            icon_position[1]+j][color] = icon[i, j][color]
    return overlay


if __name__ == "__main__":

    frame = cv2.imread("./assets/icons/test.jpg")
    frame = cv2.resize(frame, (360, 240))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    frame_shape = frame.shape
    pos = [frame.shape[0] // 2 - 15, frame.shape[1] // 2 - 15]
    arrow_size = 50
    bat_icon_url = './assets/icons/battery2.png'
    down_icon_url = './assets/icons/arrow-down-short.png'
    up_icon_url = './assets/icons/arrow-up-short.png'
    left_icon_url = './assets/icons/arrow-left-short.png'
    right_icon_url = './assets/icons/arrow-right-short.png'
    bullseye_icon_url = './assets/icons/bullseye2.png'

    ovl_up = icon_overlay(
        up_icon_url, arrow_size, pos, frame_shape, 2)
    ovl_down = icon_overlay(
        down_icon_url, arrow_size, pos, frame_shape, 2)
    ovl_right = icon_overlay(
        right_icon_url, arrow_size, pos, frame_shape, 2)
    ovl_left = icon_overlay(
        left_icon_url, arrow_size, pos, frame_shape, 2)
    ovl_ok = icon_overlay(
        bullseye_icon_url, arrow_size, pos, frame_shape, 1)

    ovl_bat = icon_overlay(
        bat_icon_url, 30, [0, 10], frame.shape, [0, 1, 2])

    ovl = ovl_bat + ovl_up

    frame[:, :, 3] = 1-ovl[:, :, 3]
    cv2.addWeighted(ovl, 1.0, frame, 1.0, 0.0, frame)

    cv2.imshow("Weighted", frame)

    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()
