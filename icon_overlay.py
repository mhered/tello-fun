#!/usr/bin/env python3

import cv2
import numpy as np


def icon_overlay(icon_url, icon_size, icon_position, frame_shape, color):
    """
    icon_overlay(icon_url, icon_size, icon_position, frame_shape, color)
    Read icon from `icon_url`, resize it to `icon_size`,
    recolor it to `color` and place it in position `pos`
    in a transparent overlay of size `frame_shape`.
    Return an image of size `frame_shape` in BGRA format (4 channels).
    """

    # load icon as BGRA
    icon = cv2.imread(icon_url, -1)
    # resize
    icon = cv2.resize(icon, (icon_size, icon_size))
    # tint icon
    icon = recolor_BGRA(icon, color)

    # position
    icon_x, icon_y = icon_position
    icon_w, icon_h, _ = icon.shape
    w, h, _ = frame_shape
    overlay = np.zeros((w, h, 4), dtype='uint8')
    overlay[icon_x:icon_x+icon_w, icon_y:icon_y+icon_h, :] = icon

    return overlay


def recolor_BGRA(img, BGRcolor):
    """
    recolor_BGRA(img, BGRcolor)
    Tint img with BGRcolor retaining intensity and alpha
    channel.
    """

    # convert to gray to obtain intensity
    intensity = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # obtain transparency from alpha channel
    transparency = img[:, :, 3]

    # recolor
    recolored_img = np.stack([BGRcolor[0]*intensity,
                              BGRcolor[1]*intensity,
                              BGRcolor[2]*intensity,
                              transparency], 2)
    return recolored_img


def blend_transparent(fore_img, bkg_img):
    """
    blend_transparent(fore_img, bkg_img)
    Blend a foreground image with alpha channel over
    a background. Assumes both images are already in
    BGRA format (4 channels)
    """

    fore_BGR = fore_img[:, :, :3]
    fore_mask = fore_img[:, :, 3]
    bkg_mask = 255 - fore_mask
    back_BGR = bkg_img[:, :, :3]

    # convert masks to 3-channel
    bkg_mask = cv2.cvtColor(bkg_mask, cv2.COLOR_GRAY2BGR)
    fore_mask = cv2.cvtColor(fore_mask, cv2.COLOR_GRAY2BGR)

    bkg = (1/255.0**2) * back_BGR * bkg_mask
    fore = (1/255.0**2) * fore_BGR * fore_mask

    blended = np.uint8(cv2.addWeighted(fore, 255.0, bkg, 255.0, 0.0))
    return blended


if __name__ == "__main__":

    frame = cv2.imread("./assets/icons/test.jpg")
    frame = cv2.resize(frame, (360, 240))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    pos = [frame.shape[0] // 2 - 15, frame.shape[1] // 2 - 15]
    pos2 = [2 * frame.shape[0] // 3 - 15, frame.shape[1] // 3 - 15]

    icon_size = 50

    bat_icon_url = './assets/icons/battery.png'
    bullseye_icon_url = './assets/icons/bullseye.png'
    up_icon_url = './assets/icons/arrow-up-short.png'

    COLOR1 = np.array([0.0, 255.0, 255.0])/255.0  # yellow
    COLOR2 = np.array([255.0, 0.0, 255.0])/255.0  # pink
    COLOR3 = np.array([0.0, 255.0, 0.0])/255.0  # green
    COLOR4 = np.array([255.0, 0.0, 0.0])/255.0  # blue

    ovl_bat = icon_overlay(
        bat_icon_url, 30, [0, 10], frame.shape, COLOR1)
    frame = blend_transparent(ovl_bat, frame)
    cv2.imshow("Battery", frame)

    ovl_arrow = icon_overlay(
        up_icon_url, icon_size, pos2, frame.shape, COLOR2)
    frame = blend_transparent(ovl_arrow, frame)
    cv2.imshow("Arrow", frame)

    ovl_ok = icon_overlay(
        bullseye_icon_url, icon_size, pos, frame.shape, COLOR3)
    frame = blend_transparent(ovl_ok, frame)
    cv2.imshow("Ok", frame)

    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()

    """
    bat_icon_url = './assets/icons/battery.png'
    down_icon_url = './assets/icons/arrow-down-short.png'
    up_icon_url = './assets/icons/arrow-up-short.png'
    left_icon_url = './assets/icons/arrow-left-short.png'
    right_icon_url = './assets/icons/arrow-right-short.png'
    bullseye_icon_url = './assets/icons/bullseye.png'
    ovl_up = icon_overlay(
        up_icon_url, arrow_size, pos, frame.shape, 2)
    ovl_down = icon_overlay(
        down_icon_url, arrow_size, pos, frame.shape, 2)
    ovl_right = icon_overlay(
        right_icon_url, arrow_size, pos, frame.shape, 2)
    ovl_left = icon_overlay(
        left_icon_url, arrow_size, pos, frame.shape, 2)
    ovl_ok = icon_overlay(
        bullseye_icon_url, arrow_size, pos, frame.shape, 1)
    """
