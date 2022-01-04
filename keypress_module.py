#!/usr/bin/env python

import pygame


def init():
    pygame.init()
    window = pygame.display.set_mode((200, 200))


def is_key_pressed(key_name):
    """ get_key(key_name)
    returns True if key_name is pressed and False otherwise """

    is_pressed = False
    for event in pygame.event.get():
        pass
    key_input = pygame.key.get_pressed()
    my_key = getattr(pygame, 'K_{}'.format(key_name))
    if key_input[my_key]:
        is_pressed = True
    pygame.display.update()
    return is_pressed


if __name__ == '__main__':
    init()
    while True:
        if is_key_pressed('LEFT'):
            print('Left key is pressed')
        if is_key_pressed('RIGHT'):
            print('Right key is pressed')
        if is_key_pressed('UP'):
            print('Up key is pressed')
        if is_key_pressed('DOWN'):
            print('Down key is pressed')
