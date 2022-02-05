# Tello fun

Today I got a super present: the Tello drone. The Boost combo kit includes one drone, some spares, three batteries and a charger. The packaging is compact and effective, more functional than luxurious. The drone itself is beautifully finished, sporting a vision positioning system and onboard camera capable of 5 Mpixel shots and 720p live video streaming, as well as neat safety features such as propeller guards and a rubber landing gear. Flight time is about 13'.

I plugged the batteries to top them up. It took about 20' to see the solid green light, and I used this time to visit the [official Tello website](https://www.ryzerobotics.com/), watch some of the quickstart [videos](https://www.ryzerobotics.com/tello/videos) and download the documentation:

* [Quick Start guide](https://dl-cdn.ryzerobotics.com/downloads/Tello/20180212/Tello+Quick+Start+Guide_V1.2+multi.pdf)
* [User Manual](https://dl-cdn.ryzerobotics.com/downloads/Tello/20180404/Tello_User_Manual_V1.2_EN.pdf)
* [Scratch README](https://terra-1-g.djicdn.com/2d4dce68897a46b19fc717f3576b7c6a/Tello 编程相关/For Tello/Scratch 0320 修改/Tello Scratch README 0320.pdf)
* [Tello SDK](https://terra-1-g.djicdn.com/2d4dce68897a46b19fc717f3576b7c6a/Tello 编程相关/For Tello/Tello SDK Documentation EN_1.3_1122.pdf)

## Why the Tello?

* [A 2018 review of the Tello by Half Chrome (best beginner drone under 100$](https://www.youtube.com/watch?v=hpwrYP1_txY)

* [Top 5 Best Programmable Drones In 2022: Make You Own Move](https://www.propelrc.com/best-programmable-drones/)

* [Tello Drone in 2021 | Still Good?](): stability and image quality (not video)

* [Top 5 accessories for Tello](https://www.youtube.com/watch?v=zOXkIOieFw8): get a wifi repeater (check setup videos for [TP Link N300 Wifi range extender]() or [Xiaomi Mi repeater](https://www.youtube.com/watch?v=gxOUK3c0bIE)) to improve video quality for 10€!

## iOS app

I installed the iOS app in my iphone. User reviews were a mixed bag but it was nice to see that after 3 years it keeps receiving updates.

Press the button on the side to switch on, wait a few seconds for the LED to go flashing orange. The instructions are easy to follow: you need to connect your mobile to the Tello Wifi network and the first time activate (??) ...not sure what I was about to say... 

First try the drone instead of hovering in place it slowly drifted until it bumped onto a book shelf... 

I searched the pretty active community in https://tellopilots.com/ and http://protello.com/ and learned this is probably related to insufficient lighting.

## Programming the Tello

Thats where the real fun is. Official support is for Scratch but I there are plenty of community-developed alterantives: the iOS app [TelloFpv](https://apps.apple.com/us/app/tellofpv/id1545864950) a [ROS driver](http://wiki.ros.org/tello_driver), and unofficial python libraries such as [TelloPy library](https://github.com/hanyazou/TelloPy) , [Tello-Python](https://github.com/dji-sdk/Tello-Python) or [DJITelloPy](https://github.com/damiafuentes/DJITelloPy) by damiafuentes, used in [this video tutorial about drone programming by Murtaza](https://www.youtube.com/watch?v=LmEcyQnfpDA&t=1282s).

## Installations

First, it is good practice to [create a virtual environment](https://linuxize.com/post/how-to-create-python-virtual-environments-on-ubuntu-18-04/):

```
$ cd tello 
$ python3 -m venv myvenv
$ source myvenv/bin/activate
```

Note: within the virtual environment, you can use the command `pip` instead of `pip3` and `python` instead of `python3`

Install the DJITelloPy library (pulls also numpy & opencv):

```
(myvenv)$ pip install djitellopy
```

## `check_battery.py` - First connection 

```python
#!/usr/bin/env python

from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()

# Explore library in:
# ./myvenv/lib/python3.8/site-packages/djitellopy/tello.py

print(drone.get_battery())
```

Switch on the Tello, connect the computer Wifi to Tello and run 

Note if you get an error `Exception: Did not receive a state packet from the Tello` disable the ubuntu firewall:

```
$ sudo ufw status
$ sudo ufw disable
```

## `basic_moves.py` - Moving around

```python
#!/usr/bin/env python

from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()

# Explore library in:
# ./myvenv/lib/python3.8/site-packages/djitellopy/tello.py

drone.takeoff()

# (L/R, fwd/bk, up/down, anti/clockwise yaw) each in -/+100%
drone.send_rc_control(0, 30, 0, 0)
sleep(2)

drone.send_rc_control(0, 0, 30, 0)
sleep(2)

drone.send_rc_control(0, 0, 0, 0)
sleep(1)

drone.send_rc_control(0, 0, -30, 0)
sleep(2)

drone.send_rc_control(0, -30, 0, 0)
sleep(2)

drone.send_rc_control(0, 0, 0, 0)
sleep(1)

drone.land()
```

## `camera.py` - Streaming frames



## `key_controls.py` - Controlling the drone with the computer keyboard

We will use the [Pygame](https://www.pygame.org/news) library:

```bash
(myvenv)$ pip install pygame
```

`keypress_module.py` - implements `init()` and `is_key_pressed()` functions using `pygame`library

`key_controls.py` - includes statement  `import keypress_module.py as kp` to use functions defined in the module.

Tested OK

Note: Why this code does not work well with `ESC` key for landing?

## `surveyor.py`- stream FPV, control the drone to move around and take pictures

Combine `camera.py`, `key_controls.py` and `icon_overlay.py`

Add display of timestamp and battery level to streaming window

Add option to take a picture and store with unique name in `./assets/images/`

**Note: destination folder must exist beforehand otherwise the `cv2.imwrite` fails to save without giving any warning** 

**Note: Why original version did not work?** Had to make a few changes to  `key_controls.py`

**Note: Why this code does not work well with `SPACE` key for taking pictures?**

Usage: 

1. Connect computer to the drone Wifi `TELLO_EFD008`, 

2. Launch `$ python ./surveyor.py` 

3. Wait for streaming window to show live image

4. Click on pygame window so it gets focus and can listen to keystrokes

5. Press `RETURN` to take off 

6. Press `p`to take a picture, store with unique name in `./assets/images/`

7. Press arrow keys to move the drone: `LEFT` `RIGHT`, forward (with `UP`) and backwards (with `DOWN`)

8. Press `w` to climb and `s` to descend 

9. Press `a` to rotate counterclockwise and `d` to rotate clockwise

10. Press `q` to land

11. `CTRL-c` to stop the program

Includes `process_frame()`to resize and superimpose battery icon with status and a timestamp in the camera feed

## `face_track.py` - drone detects and tracks face with altitude and yaw

Inspired loosely on project 3 of [Murtaza's Drone Programming With Python video](https://www.youtube.com/watch?v=LmEcyQnfpDA&t=1282s) but implemented simple bang-bang control instead of PID, and chose to yaw and control height instead of distance to target to avoid having the drone moving around the room. Idea from selfie air stick project: [repo](https://github.com/geaxgx/tello-openpose/blob/master/README.md) and [video](https://www.youtube.com/watch?v=RHRQoaqQIgo) and this [thread](https://tellopilots.com/threads/applying-computer-vision-techniques-to-tello.3804/).

Downloading `haarcascade_frontalface_default.xml` from opencv github: https://github.com/opencv/opencv/tree/master/data/haarcascades did not work.

Also I could not find `opencv` from command line:

```bash
(myvenv) mhered@mhered-laptop:~/tello$ which opencv
(myvenv) mhered@mhered-laptop:~/tello$ whereis opencv
opencv:
(myvenv) mhered@mhered-laptop:~/tello$ opencv --v
Command 'opencv' not found
```

However it was pulled by `djitellopy`, and is detected in python:

```python
>>>import cv2
>>> print(cv2.__version__)
4.5.5
>>> print(cv2.data.haarcascades)
/home/mhered/tello/myvenv/lib/python3.8/site-packages/cv2/data/
```

## `icon_overlay.py` - helper function to overlay icons on the live stream 

Used in `frame_process()` to show the battery icon
After trying unsuccessfully two approaches ([this one yields jagged edges](https://theailearner.com/tag/cv2-addweighted/ ) and [this one multiplies intensities in the two images rather than covering the background with the overlay](https://www.youtube.com/watch?v=dCSZvP5IAqc), I finally settled for [this approach](https://stackoverflow.com/questions/36921496/how-to-join-png-with-alpha-transparency-in-a-frame-in-realtime/37198079#37198079)

Note: I failed to automate the conversion of `svg` images to `png` preserving the alpha channel. Either it is not proprly installed or not accessible from the virtual environment (myvenv)  **Check!!**. 

After some frustration I just repeated the conversion of `svg` icons to `png`using GIMP:

Open -> Set density to 90pix/cm, size to 100x100 pix. 

Color-> Invert

File -> Export -> Select File Type (by Extension) -> PNG image -> Export -> Export

## `line_follower.py`

Based on project 4 of  [Murtaza's Drone Programming With Python video](https://www.youtube.com/watch?v=LmEcyQnfpDA&t=1282s) 

Rotation:

| LH sensor | Center sensor | RH sensor | Action |
| - | - | - | - |
| 0 | 1 | 0 | move fwd |
| 1 | 1 | 0 | slight turn left |
| 1 | 0 | 0 | strong turn left |
| 0 | 1 | 1 | slight turn right |
| 0 | 0 | 1 | strong turn right |
| 0 | 0 | 0 | stop |
| 1 | 0 | 1 | stop |
| 1 | 1 | 1 | stop |

Translation: PID to keep line centered in the image


## `utils.py` - auxiliary functions

- `countdown()` - speak a countdown
- `process_frame()` - show an overlay with a timestamps and battery status
- `reduce_frame()` - resize. Obsolete, to be eliminated

## TO DO

- [x] fix `icon_overlay.py` 
- [ ] do `line_follower.py`
- [ ] review and program `tello-openpose`: https://github.com/geaxgx/tello-openpose/blob/master/README.md
- [ ] refactor to use ROS driver
- [ ] check out how to access raw video in this thread http://tellopilots.com/threads/tello-whats-possible.88/post-1021
