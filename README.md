

Today I got a super present: the Tello drone. The Boost combo kit includes one drone, some spares, three batteries and a charger. The packaging is compact and effective, more functional than luxurious.  The drone itself is beautifully finished, sporting a vision positioning system and onboard camera capable of 5Mpixel shots and 720p live video streaming, as well as neat safety features such as propeller guards and a rubber landing gear. Flight time is 13'

I plugged the batteries to top them up. It took about 20' to see the solid green light, and I used this time to visit the [official Tello website](https://www.ryzerobotics.com/) and download the documentation and watch the [videos](https://www.ryzerobotics.com/tello/videos):

* [Quick Start guide](https://dl-cdn.ryzerobotics.com/downloads/Tello/20180212/Tello+Quick+Start+Guide_V1.2+multi.pdf)
* [User Manual](https://dl-cdn.ryzerobotics.com/downloads/Tello/20180404/Tello_User_Manual_V1.2_EN.pdf)
* [Scratch README](https://terra-1-g.djicdn.com/2d4dce68897a46b19fc717f3576b7c6a/Tello 编程相关/For Tello/Scratch 0320 修改/Tello Scratch README 0320.pdf)
* [Tello SDK](https://terra-1-g.djicdn.com/2d4dce68897a46b19fc717f3576b7c6a/Tello 编程相关/For Tello/Tello SDK Documentation EN_1.3_1122.pdf)

I installed the iOS app in my iphone. User reviews were a mixed bag but it was nice to see that after 3 years it keeps receiving updates.

Press the button on the side to switch on, wait a few seconds for the LED to go flashing orange. The instructions are easy to follow: you need to connect your mobile to the Tello Wifi network and the first time activate 

First try the drone instead of hovering in place it slowly drifted until it bumped onto a book shelf... 

Pretty active community in https://tellopilots.com/ and http://protello.com/ seems related to insufficient lighting.

Official support for Scratch but I have seen unofficial python [TelloPy library](https://github.com/hanyazou/TelloPy) and a [ROS driver](http://wiki.ros.org/tello_driver) etc.

Also python modules in this repo: [Tello-Python](https://github.com/dji-sdk/Tello-Python)

And the one from [DJITelloPy](https://github.com/damiafuentes/DJITelloPy) by damiafuentes, used in [this video by Murtaza](https://www.youtube.com/watch?v=LmEcyQnfpDA&t=1282s) which started it all...

[A 2018 review of the Tello by Half Chrome (best beginner drone under 100$](https://www.youtube.com/watch?v=hpwrYP1_txY)

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

## `check-battery.py` - First connection 

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

## `basic-moves.py` - Moving around

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



## `key-controls.py` - Controlling the drone with the computer keyboard

We will use the [Pygame](https://www.pygame.org/news) library:

```bash
(myvenv)$ pip install pygame
```

`keypress_module.py` - implements `init()` and `is_key_pressed()` functions using `pygame`library

`key-controls.py` - includes statement  `import keypress_module.py as kp` to use functions defined in the module.

Tested OK

Note: Why this code does not work well with `ESC` key for landing?

## `surveyor.py`- stream FPV, control the drone to move around and take pictures

Combine `camera.py` and `key-controls.py`

Add display of timestamp and battery level to streaming window

Add option to take a picture and store with unique name in `./assets/images/`

**Note: destination folder must exist beforehand otherwise the `cv2.imwrite` fails to save without giving any warning** 

**Note: Why original version did not work?** Had to make a few changes to  `key-controls.py`

**Note: Why this code does not work well with `SPACE` key for taking pictures?**



Usage: 

1.  Connect computer to the drone Wifi `TELLO_EFD008`, 
2.  Launch `$ python ./surveyor.py` 
3.  Wait for streaming window to show live image
4. Click on pygame window so it gets focus and can listen to keystrokes
5. Press `RETURN` to take off 
6. Press `p`to take a picture, store with unique name in `./assets/images/`
7. Press arrow keys to move the drone: `LEFT` `RIGHT`, forward (with `UP`) and backwards (with `DOWN`)
8. Press `w` to climb and `s` to descend 
9. Press `a` to rotate counterclockwise and `d` to rotate clockwise
10. Press `q` to land
11. `CTRL-c` to stop the program

## `face_track.py` - drone detects and tracks face with altitude and yaw

Did not work downloading `haarcascade_frontalface_default.xml` from opencv github: https://github.com/opencv/opencv/tree/master/data/haarcascades. 

Also could not find opencv:

```bash
(myvenv) mhered@mhered-laptop:~/tello$ which opencv
(myvenv) mhered@mhered-laptop:~/tello$ whereis opencv
opencv:
(myvenv) mhered@mhered-laptop:~/tello$ opencv --v
Command 'opencv' not found
```

however it was pulled by djitellopy, and I can detect it in python:

```python
>>>import cv2
>>> print(cv2.__version__)
4.5.5
>>> print(cv2.data.haarcascades)
/home/mhered/tello/myvenv/lib/python3.8/site-packages/cv2/data/
```

## `icon_overlay.py` - helper function to overlay icons on the live stream 

Used in `frame_process()` to show the battery icon
