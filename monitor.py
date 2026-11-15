import serial
from distance_parser import DistCalc
from calculate_volume import VolCalc
import pygame 

s = serial.Serial(port="/dev/cu.usbmodem0010577862563", baudrate=115200)
d_calc = DistCalc()
a_vol_calc = VolCalc(zero_distance=8.0) # AMBIENT VOLUME CALCULATOR
s_vol_calc = VolCalc(zero_distance=4.0) # SOUND VOLUME CALCULATOR

pygame.mixer.init()
pygame.mixer.music.load("sounds/ambient.mp3")
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(loops=-1)

sound = pygame.mixer.Sound("sounds/guide.mp3")

sound_playing = False

with open("output.txt", "a") as f:
    while True:
        serial_line = s.readline()

        distance = d_calc.calculate_distance(serial_line)

        if distance != None:
            if distance < 3 and not sound_playing:
                s_volume = s_vol_calc.calculate_volume(distance)
                sound.play()
                sound.set_volume(s_volume)
                sound_playing = True

            if distance > 4.5 and sound_playing:
                sound.stop()
                sound_playing = False

        a_volume = a_vol_calc.calculate_volume(distance)

        print("distance: ", distance, " vol: ", a_volume)

        pygame.mixer.music.set_volume(a_volume)


