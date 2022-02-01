#!/usr/bin/env python

from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()

# Explore library in:
# ./myvenv/lib/python3.8/site-packages/djitellopy/tello.py

drone.takeoff()

# (L/R, fwd/bk, up/down, anti/clockwise yaw) each in -/+100%
drone.send_rc_control(0, 0, 30, 0)
sleep(2)

drone.send_rc_control(0, 0, 0, 80)
sleep(3)

drone.send_rc_control(0, 0, 0, 0)
sleep(1)

drone.send_rc_control(0, 0, 0, -80)
sleep(3)

drone.send_rc_control(0, 0, 0, 0)
sleep(1)

drone.land()
