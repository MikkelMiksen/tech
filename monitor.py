import serial
from distance_parser import DistCalc
from calculate_volume import VolCalc
import pygame 

s = serial.Serial(port="/dev/cu.usbmodem0010577862563", baudrate=115200)
d_calc = DistCalc()
v_calc = VolCalc(zero_distance=5.0)

pygame.mixer.init()
pygame.mixer.music.load("i_hate_sweden.mp3")
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(loops=-1)

with open("output.txt", "a") as f:
    while True:
        serial_line = s.readline()

        distance = d_calc.calculate_distance(serial_line)

        volume = v_calc.calculate_volume(distance)

        print("distance: ", distance, " vol: ", volume)

        pygame.mixer.music.set_volume(volume)


