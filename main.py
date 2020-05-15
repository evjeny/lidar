import serial
import time

import numpy as np
import matplotlib.pyplot as plt


com = "/dev/ttyUSB1"
serial = serial.Serial(com, 9600)

num_states = 180
vert_lines = 1
mrx = np.zeros((vert_lines, num_states))

while True:
    command = input("enter command: ")

    if command.lower() == "help":
        print(" help -- print help")
        print(" exit -- exit the app")
        print(" setvert [vert_lines] -- set size of veritcal dimension")
        print(" scan [vert_begin] [vert_end] -- scan vertical lines")
        print(" defaultpos -- set default position of scanner")
        print(" show -- show the scanned picture")
    elif command.lower() == "exit":
        break
    elif command.lower().startswith("setvert"):
        parts = command.lower().split(" ")
        if len(parts) != 2:
            print("invalid syntax, must be `setvert [vert_lines]`")
        else:
            vert_lines = int(parts[1])
            mrx = np.zeros((vert_lines, num_states))
    elif command.lower().startswith("scan"):
        parts = command.lower().split(" ")
        begin = 0
        end = 0
        if len(parts) == 2:
            begin = int(parts[1])
            end = begin + 1
        elif len(parts) == 3:
            begin = int(parts[1])
            end = int(parts[2]) + 1
        else:
            print("invalid syntax, must be `scan [vert_deg]`")
            continue
            
        for i in range(begin, end):
            serial.write(b's')
            result_line = serial.readline().decode().strip()
            values = [int(value) for value in result_line.split(",")]

            mrx[i] = np.array(values)
    elif command.lower() == "defaultpos":
        serial.write(b'e')
    elif command.lower() == "show":
        plt.imshow(mrx, cmap="hot")
        plt.show()

