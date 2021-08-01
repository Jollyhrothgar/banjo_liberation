from . import encode
import pygame
import numpy


def play(data, rate=44100):
    ''' Send audio array to pygame for playback
    '''
    pygame.mixer.init(rate, -16, 1, 1024)
    sound = pygame.sndarray.make_sound(encode.as_int16(data))
    length = sound.get_length()
    sound.play()
    pygame.time.wait(int(length * 1000))
    pygame.mixer.quit()
