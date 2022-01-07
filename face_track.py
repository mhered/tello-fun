#!/usr/bin/env python

import cv2
from djitellopy import tello
from surveyor import process_frame
import time


def find_face(frame):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(frame_gray, 1.2, 8)

    faces_centres = []
    faces_areas = []

    for (x, y, width, height) in faces:
        # rectangle
        cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 0, 255), 2)
        centre_x = x + width // 2  # // operator division(floor) e.g. 9//2=4
        centre_y = y + height // 2
        area = width * height
        faces_centres.append((centre_x, centre_y))
        faces_areas.append(area)
        print(len(faces_areas))
    if len(faces_areas) != 0:
        i = faces_areas.index(max(faces_areas))
        # centre of largest
        cv2.circle(frame, (centre_x, centre_y), 5, (0, 255, 0), cv2.FILLED)
        return frame, [faces_centres[i], faces_areas[i]]
    else:
        return frame, [[0, 0], 0]


def track_face(drone, face_data, frame_size, pid, p_error):

    # (L/R, bk/fwd, up/down, clock/counterclock-wise yaw) each in -/+100%
    left_right = 0
    bk_fwd = 0
    down_up = 0
    c_cc_yaw = 0
    speed = 25

    height, width = frame_size
    face_x, face_y = face_data[0]
    # face_area = face_data[1]
    # print(f"(w,h):{frame_size}, (face_x,face_y):{face_data[0]}")

    # up-down
    if face_y > 3*height//5:
        print(f"Face in y:{face_y} > {3*height//5}")
        print("move down v")
        down_up = -speed
    elif face_y != 0 and face_y < 2*height//5:
        print(f"Face in y:{face_y} < {2*height//5}")
        print("move up ^")
        down_up = speed
    else:
        print("stay put")

    # left-right
    if face_x > 3*width//5:
        print(f"Face in x:{face_x} > {3*width//5}")
        print("rotate clockwise >")
        c_cc_yaw = speed
    elif face_x != 0 and face_x < 2*width//5:
        print(f"Face in x:{face_x} < {2*width//5}")
        print("rotate counterclockwise <")
        c_cc_yaw = -speed
    else:
        print("stay put")

    return [left_right, bk_fwd, down_up, c_cc_yaw]


if __name__ == "__main__":

    source = "TELLO"

    # initializations
    if source == "TELLO":
        # tello drone
        drone = tello.Tello()
        drone.connect()
        # start streaming
        drone.streamon()
        frame = drone.get_frame_read().frame
        frame = process_frame(frame, drone)
        cv2.imshow("Live Image", frame)
        time.sleep(5)
        drone.takeoff()
        drone.send_rc_control(0, 0, 25, 0)
        time.sleep(4)
        drone.send_rc_control(0, 0, 0, 0)

    elif source == "WEBCAM":
        # start streaming from webcam
        video_stream = cv2.VideoCapture(0)

    # main loop
    while True:
        if source == "TELLO":
            # get frame from drone
            frame = drone.get_frame_read().frame
            frame = process_frame(frame, drone)
        elif source == "WEBCAM":
            # get frame from webcam
            _, frame = video_stream.read()
        else:
            break

        frame, face_data = find_face(frame)
        commands = track_face(0, face_data, frame.shape[:2], 0, 0)
        if source == "TELLO":
            drone.send_rc_control(
                commands[0],
                commands[1],
                commands[2],
                commands[3])

        cv2.imshow("Live Image", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            drone.land
            break
    drone.streamoff()
    drone.end()
    cv2.destroyAllWindows()
