import serial
import calculate_distance

s = serial.Serial(port="/dev/cu.usbmodem0010577862563", baudrate=115200)

while True:
    cs_distances = s.readline()
    dist = calculate_distance.calculate_distance(str(cs_distances))
    print(dist)
