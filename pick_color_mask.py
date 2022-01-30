#!/usr/bin/env python

import cv2
import numpy as np

global isframe
isframe = True


def empty(args):
    pass


def pick_color_mask(video_stream,
                    lower_init=[0, 0, 0],
                    upper_init=[179, 255, 255], ):
    """ pick_color_mask(video_stream, *lower_init, *upper_init)
        Select interactively HSV thresholds to mask image by color.
        Returns lower_threshold, upper_threshold to use with cv2.inRange()
        Optional arguments: starting value of thresholds"""

    frame_width = int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # MH if single frame:
    if isframe:
        frame = cv2.imread('./assets/data/IMG_7732_xs.PNG')
        frame_width = 480
        frame_height = 360
        frame = cv2.resize(frame, (frame_width, frame_height))

    print("width:", frame_width)
    print("height:", frame_height)
    cv2.namedWindow("Color Mask", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Color Mask", 3*frame_width+60, frame_height+200)
    cv2.createTrackbar("HUE min", "Color Mask", lower_init[0], 179, empty)
    cv2.createTrackbar("HUE Max", "Color Mask", upper_init[0], 179, empty)
    cv2.createTrackbar("SAT min", "Color Mask", lower_init[1], 255, empty)
    cv2.createTrackbar("SAT Max", "Color Mask", upper_init[1], 255, empty)
    cv2.createTrackbar("VAL min", "Color Mask", lower_init[2], 255, empty)
    cv2.createTrackbar("VAL Max", "Color Mask", upper_init[2], 255, empty)

    print("Select threshold values. Type 'q' to quit")

    while True:
        if isframe:
            pass
        else:
            _, frame = video_stream.read()

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h_min = cv2.getTrackbarPos("HUE min", "Color Mask")
        h_max = cv2.getTrackbarPos("HUE Max", "Color Mask")
        s_min = cv2.getTrackbarPos("SAT min", "Color Mask")
        s_max = cv2.getTrackbarPos("SAT Max", "Color Mask")
        v_min = cv2.getTrackbarPos("VAL min", "Color Mask")
        v_max = cv2.getTrackbarPos("VAL Max", "Color Mask")

        lower_threshold = np.array([h_min, s_min, v_min])
        upper_threshold = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(frame_hsv, lower_threshold, upper_threshold)
        frame_masked = cv2.bitwise_and(frame, frame, mask=mask)
        show_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        horiz_stack = np.hstack([frame, show_mask, frame_masked])

        cv2.imshow("Color Mask", horiz_stack)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()

    return lower_threshold, upper_threshold


if __name__ == "__main__":

    # Create video stream before calling

    # use video from webcam
    video_stream = cv2.VideoCapture(0)

    # reduce size (optional)
    width = 320
    height = 240
    video_stream.set(3, width)
    video_stream.set(4, height)

    # Call pick_color_mask without initial values
    lower_threshold, upper_threshold = pick_color_mask(video_stream)

    print("lower limits:", lower_threshold)
    print("upper limits:", upper_threshold)

    # Alternative: call pick_color_mask with initial values
    lower_threshold, upper_threshold = pick_color_mask(video_stream,
                                                       lower_threshold,
                                                       upper_threshold)
    print("lower limits:", lower_threshold)
    print("upper limits:", upper_threshold)

    # Release video stream after calling
    video_stream.release()
