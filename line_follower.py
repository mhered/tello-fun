#!/usr/bin/env python

import cv2
import numpy as np

from djitellopy import tello
from pick_color_mask import pick_color_mask, get_frame
from utils import countdown, process_frame, reduce_frame

# parameters
THRESHOLD = .80  # % of detection in area to set to 1
TRANS_GAIN = .33  # translation gain, the higher the more sensitive
SENSORS = 3  # number of areas for track sensing
ROTA_VALS = [-25, -15, 0, 15, 25]  # rotation gain, match with SENSORS
FWD_SPEED = 15  # default fwd speed
video_source = "WEBCAM"

# Functions definition


def thresholding(frame, lower_threshold, upper_threshold):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv, lower_threshold, upper_threshold)
    return mask


def get_lateral_offset(mask, frame, decorate_frame=True):
    GREEN = (0.0, 255.0, 0.0)
    PINK = (255.0, 0.0, 255.0)
    RED = (0.0, 0.0, 255.0)

    cx = 0.0
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        largest_area_detected = max(contours, key=cv2.contourArea)
        x_r, y_r, w_r, h_r = cv2.boundingRect(largest_area_detected)
        cx = x_r + w_r//2
        cy = y_r + h_r//2
        if decorate_frame:
            # draw boundary of track detected
            cv2.drawContours(frame, largest_area_detected, -1, PINK, 3)
            # draw centroid
            cv2.circle(frame, (cx, cy), 5, GREEN, cv2.FILLED)
            # draw bounding rectangle
            # cv2.rectangle(frame, (x_r, y_r), (x_r+w_r, y_r+h_r), RED, 2)
            h, w, c = frame.shape
            # draw arrow
            cv2.arrowedLine(frame, (w//2, h//2, ), (cx, h//2,), GREEN, 1)
    print("Offset:", w//2-cx)
    return cx, frame


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
        # display a window per area
        # cv2.imshow(win_title, area)
    print("Sensors:", sens_out)
    return sens_out


def compute_commands(sens_out, cx):
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
    elif sens_out == [0, 1, 1]:
        yaw = ROTA_VALS[3]
    elif sens_out == [0, 0, 1]:
        yaw = ROTA_VALS[4]
    elif sens_out == [1, 1, 1]:
        yaw = 0
    else:
        yaw = 0
        fwd_speed = 0

    print(f"Command: ({left_right}, {fwd_speed}, 0, {yaw})")

    return left_right, fwd_speed, 0, yaw


if __name__ == "__main__":

    # Initialization of variables

    # reduced size of images for processing
    frame_width = 360
    frame_height = 240

    # video_source = "STATIC" for testing on still photos
    # video_source = "WEBCAM" for testing on stream from video source
    # video_source = "DRONE" for testing on Tello drone

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
        # print(f"Battery: {drone.get_battery()}%")
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

    # HSV values test sheet
    lower_threshold = [115,  70,   0]
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

        # resize preserving aspect ratio
        frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
        # frame = reduce_frame(frame, (frame_width, frame_height))

        mask = thresholding(frame, lower_threshold, upper_threshold)
        cx, frame = get_lateral_offset(mask, frame)  # for translation
        sens_out = get_sensor_output(mask, SENSORS)  # for rotation
        left_right, fwd_speed, up_down, yaw = compute_commands(sens_out, cx)

        text_bat = "NA"
        if video_source == "DRONE":
            drone.send_rc_control(left_right, fwd_speed, up_down, yaw)
            text_bat = drone.get_battery()
        # show images
        frame = process_frame(frame, text_bat)
        cv2.imshow("Output", frame)
        # cv2.imshow("Mask", mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if video_source == "DRONE":
        drone.land
        drone.streamoff()
        drone.end()
    cv2.destroyAllWindows()
