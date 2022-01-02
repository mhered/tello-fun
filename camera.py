#!/usr/bin/env python

from djitellopy import tello
import cv2

drone = tello.Tello()
drone.connect()

# Explore library in:
# ./myvenv/lib/python3.8/site-packages/djitellopy/tello.py

print(drone.get_battery())

drone.streamon()

while True:
    # get frame
    frame = drone.get_frame_read().frame
    # resize
    frame_xs = cv2.resize(frame, (360, 240))
    # mirror for display
    frame_xs_flipped = cv2.flip(frame_xs, 1)

    # show images
    cv2.imshow("Frame", frame_xs_flipped)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
drone.streamoff()
cv2.destroyAllWindows()
