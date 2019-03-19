#!/usr/bin/python3

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import serial
import numpy as np
import _thread as thread


def yprUpdater(ser):
	global ypr

	# Read a couple for safety
	for i in range(0, 100):
		ser.readline()

	# Read in some so there will always be a last point
	for i in range(0, 10):
		ypr.append(readYpr(ser))


	while True:
		ypr.append(readYpr(ser))




def readYpr(ser):

	errMatrix = [0, 0, 0]

	ser.flush()
	line = ser.readline()
	line = line.decode("ascii").rstrip()

	if "overflow" in line:
		print("FIFO Overflow!!")
		return errMatrix

	ypr = line.split(",")
	if len(ypr) is not 3:
		print("Recieved invalid data")
		return errMatrix

	return ypr




# Setup
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("Yaw")
ax.set_ylabel("Pitch")
ax.set_zlabel("Roll")
ser = serial.Serial("/dev/serial/by-id/usb-SparkFun_SparkFun_Pro_Micro-if00", 115200, timeout = 1)

#ax.plot()

plt.ion()
plt.show()

# Set up YPR and start the updater thread
ypr = list()
thread.start_new_thread(yprUpdater, (ser, ))
time.sleep(2)


# Get points and plot
while True:

	print(ypr[-1])

	ax.plot([int(ypr[-1][0]), int(ypr[-2][0])],
	        [int(ypr[-1][1]), int(ypr[-2][1])],
	        [int(ypr[-1][2]), int(ypr[-2][2])], c = "r")


	plt.draw()
	plt.pause(0.0001)

	if not ser.isOpen():
		break

ser.close()
