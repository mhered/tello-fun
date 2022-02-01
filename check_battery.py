#!/usr/bin/env python

from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()

# Explore library in:
# ./myvenv/lib/python3.8/site-packages/djitellopy/tello.py

print(drone.get_battery())
