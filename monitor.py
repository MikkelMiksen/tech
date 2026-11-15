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
s_volume=0
sound_playing = False

with open("output.txt", "a") as f:
    while True:
        serial_line = s.readline()

        distance = d_calc.calculate_distance(serial_line)
        a_volume = a_vol_calc.calculate_volume(distance)

        if distance != None:
            if distance < 3 and not sound_playing:
                sound.play()
                sound_playing = True
            if sound_playing: 
                s_volume = s_vol_calc.calculate_volume(distance)
                sound.set_volume(s_volume)
            if distance > 4.5 and sound_playing:
                sound.stop()
                sound_playing = False


        print("distance: ", distance, " a_vol: ", a_volume, " s_vol: ", s_volume)


        pygame.mixer.music.set_volume(a_volume)


