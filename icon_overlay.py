#!/usr/bin/env python

import cv2
import numpy as np


def icon_overlay(frame, icon, icon_pos=(0, 0), color=False, icon_size=False):
    """
    `frame = icon_overlay(frame, icon, icon_pos=(x,y), color, icon_size=(h,w))`
    assume `icon` is BGRA format (4 channels)
    if provided, resize it to `icon_size` and recolor it to `color`
    and place it in position `icon_pos` (defaults to (0,0))
    in a transparent overlay of size `frame.shape`.
    Return blend of this overlay with `frame` in BGRA format (4 channels).
    """

    # assume icon is BGRA
    # resize
    if icon_size is False:
        pass
    else:
        icon = cv2.resize(icon, (icon_size[1], icon_size[0]))

    # tint icon
    if color is False:
        pass
    else:
        color = 1/255.0*np.asarray([color[0], color[1], color[2]])
        icon = recolor_BGRA(icon, color)

    # position
    icon_x, icon_y = icon_pos
    icon_h, icon_w, _ = icon.shape
    h, w, _ = frame.shape
    overlay = np.zeros((h, w, 4), dtype='uint8')
    overlay[icon_x:icon_x+icon_h, icon_y:icon_y+icon_w, :] = icon

    frame = blend_transparent(overlay, frame)

    return frame


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
    a background. Assumes foreground image is already
    in BGRA format (4 channels)
    """

    # get BGR channels from fore and bkg images
    fore_BGR = fore_img[:, :, :3]
    back_BGR = bkg_img[:, :, :3]

    # prepare both masks based on alpha channel of fore_img
    fore_mask = fore_img[:, :, 3]
    bkg_mask = 255 - fore_mask

    # convert masks to 3-channel
    fore_mask = cv2.cvtColor(fore_mask, cv2.COLOR_GRAY2BGR)
    bkg_mask = cv2.cvtColor(bkg_mask.astype('uint8'), cv2.COLOR_GRAY2BGR)

    # mask
    bkg = (1/255.0**2) * back_BGR * bkg_mask
    fore = (1/255.0**2) * fore_BGR * fore_mask

    # blend
    blended = np.uint8(cv2.addWeighted(fore, 255.0, bkg, 255.0, 0.0))
    return blended


if __name__ == "__main__":

    frame = cv2.imread("./assets/icons/test.jpg")
    frame = cv2.resize(frame, (360, 240))
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    icon_size = (60, 200)
    centre_pos = [(frame.shape[0] - icon_size[0]) // 2,
                  (frame.shape[1] - icon_size[1]) // 2]

    COLOR1 = np.array([255.0, 0.0, 255.0])  # pink
    COLOR2 = np.array([0.0, 255.0, 255.0])  # yellow
    COLOR3 = np.array([0.0, 255.0, 0.0])  # green
    COLOR4 = np.array([255.0, 0.0, 0.0])  # blue

    # load icons in BGRA format (4 channel)
    bat_icon = cv2.imread('./assets/icons/battery.png', -1)
    arrow_icon = cv2.imread('./assets/icons/arrow-up-short.png', -1)
    ok_icon = cv2.imread('./assets/icons/bullseye.png', -1)

    frame = icon_overlay(frame, arrow_icon, (0, 200), COLOR3, (30, 30))
    cv2.imshow("Arrow", frame)

    frame = icon_overlay(frame, ok_icon, centre_pos, COLOR4, icon_size)
    cv2.imshow("Ok", frame)

    frame = icon_overlay(frame, bat_icon, (frame.shape[0]-bat_icon.shape[0],
                                           frame.shape[1]-bat_icon.shape[1]),
                         COLOR2)
    cv2.imshow("Battery", frame)

    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        cv2.destroyAllWindows()

        """ other icons
        bat_icon_url = './assets/icons/battery.png'
        down_icon_url = './assets/icons/arrow-down-short.png'
        up_icon_url = './assets/icons/arrow-up-short.png'
        left_icon_url = './assets/icons/arrow-left-short.png'
        right_icon_url = './assets/icons/arrow-right-short.png'
        bullseye_icon_url = './assets/icons/bullseye.png'
        """
