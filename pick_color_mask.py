#!/usr/bin/env python

import cv2
import numpy as np

from djitellopy import tello


def empty(args):
    pass


def reduce_frame(img, desired_shape):
    scale_percent = min(
        desired_shape[0]/img.shape[0], desired_shape[1]/img.shape[1])
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized_img


def pick_color_mask(video_source="WEBCAM", frame_size=-1,
                    lower_init=[0, 0, 0],
                    upper_init=[179, 255, 255]):
    """ pick_color_mask(*video_source, *lower_init, *upper_init, *frame_size)
        Select interactively HSV thresholds to mask image by color.
        Returns lower_threshold, upper_threshold to use with cv2.inRange()
        Optional arguments:
        - video_source: "WEBCAM", "DRONE" or "STATIC". Default "WEBCAM"
        - frame_size: desired (width, height) to process smaller images.
          Default -1 to process full frame size of video feed
        - lower_init, upper_init: starting value of thresholds

        """

    frame = get_frame(video_source)
    if frame_size == -1:
        frame_width, frame_height, _ = frame.shape
        frame_size = (frame_width, frame_height)
    else:
        frame = reduce_frame(frame, frame_size)
        frame_width, frame_height, _ = frame.shape

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
        frame = get_frame(video_source)

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


def get_frame(video_source):
    global drone, video_stream, IMAGE_PATH

    if video_source == "DRONE":
        frame = drone.get_frame_read().frame
        frame = cv2.flip(frame, 0)  # flip vertically to avoid mirror effect

    elif video_source == "WEBCAM":
        _, frame = video_stream.read()

    elif video_source == "STATIC":
        frame = cv2.imread(IMAGE_PATH)

    else:
        print(f"Video Source: {video_source} not recognized.")

    return frame


if __name__ == "__main__":

    # Create video stream before calling
    # (Choose one)

    """
    # A) use static img
    video_source = "STATIC"
    IMAGE_PATH = './assets/data/IMG_7733_xs.PNG'
    """

    # B) use video from integrated webcam
    video_source = "WEBCAM"
    video_stream = cv2.VideoCapture(0)

    """
    # C) use drone video stream
    video_source = "DRONE"
    drone = tello.Tello()
    drone.connect()
    drone.streamon()
    """

    # Call pick_color_mask without initial values
    lower_threshold, upper_threshold = pick_color_mask(video_source)

    print("lower limits:", lower_threshold)
    print("upper limits:", upper_threshold)

    # Alternative: call pick_color_mask with initial values
    lower_threshold, upper_threshold = pick_color_mask(video_source,
                                                       (320, 240),
                                                       lower_threshold,
                                                       upper_threshold)
    print("lower limits:", lower_threshold)
    print("upper limits:", upper_threshold)

    # Release video stream after call
    if video_source == "WEBCAM":
        video_stream.release()
    elif video_source == "DRONE":
        drone.streamoff()

    cv2.destroyAllWindows()
