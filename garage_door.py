#****************************************************************************************
# Script:        garage_door.py
# Author:        Jim Adams
# Date:          March 21, 2014
# Version:       1.1
# Language:      Python 3
# Target:        GeekiPi (Raspberry Pi)
#
# History
# =======================================================================================
# Version:       1.1
# Date:          March 26, 2014
# Author:        Jim Adams
#
# Added improved user interface including support for numeric or alpha choices for
# selecting which door to open or close.
# Also added prompt to ask the user if any open door should be closed when the
# user chooses to exit the application.
# Added better formatted messages.
# ---------------------------------------------------------------------------------------
# Version:       1.0
# Date:          March 21, 2014
# Author:        Jim Adams
#
# Original version of the application.
#****************************************************************************************

import time
import pifacedigitalio
import sys
import os

# set the static messages we will want to display to the user
test_message = "*** Garage Door is set to TEST mode ***"
welcome_message = "* Adams' Garage Door application *"
goodbye_message = "The Garage Door application is ending.\nGoodbye."
option_message = "Select one of the options below"
door_one_warning_message = ">>> WARNING: Garage Door 1 is OPEN! <<<"
door_two_warning_message = ">>> WARNING: Garage Door 2 is OPEN! <<<"

# initialize the i/o board
pfd = pifacedigitalio.PiFaceDigital()

# define the door class which will encapsulate our garage door functions
class Door:
	door_number = 0
	door_open = False

	def __init__(self, door_number, door_open):
		self.door_number = door_number
		self.door_open = door_open
			
	def status(self):
		print("Garage Door {:d} is currently".format(self.door_number), "{:s}.".format("Open" if self.door_open else "Closed"))

	def close(self):
		if self.door_open == True:
			if not mode_test:
				pfd.leds[self.door_number-1].turn_on()
				time.sleep(0.5)
				pfd.leds[self.door_number-1].turn_off()
			else:
				print("Test Mode: Simulating Door Action...")
			self.door_open = not self.door_open

	def open(self):
		if self.door_open == False:
			if not mode_test:
				pfd.leds[self.door_number-1].turn_on()
				time.sleep(0.5)
				pfd.leds[self.door_number-1].turn_off()
			else:
				print("Test Mode: Simulating Door Action...")
			self.door_open = not self.door_open

	def toggle(self):
		if not mode_test:
			pfd.leds[self.door_number-1].turn_on()
			time.sleep(0.25)
			pfd.leds[self.door_number-1].turn_off()
		else:
			print("Test Mode: Simulating Door Action...")
		self.door_open = not self.door_open

# clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

# check to see if we are in test mode. If we are then
# we will not actually open/close the garage doors
mode_test = False
argument_count = len(sys.argv)
if argument_count > 1:
	if sys.argv[1].upper() == 'TEST':
		print("\n" + ("*" * len(test_message)) + "\n" + test_message + "\n" + ("*" * len(test_message)))
		mode_test = True

# display the welcome message
print("\n" + ("*" * len(welcome_message)) + "\n" + welcome_message + "\n" + ("*" * len(welcome_message)) + "\n")

# initialize the door(s)
door_one = Door(1, False)
door_two = Door(2, False)
door_one.status()
door_two.status()

# now all there is to do is wait for the user to tell us what to do
while True:
	# display user instructions
	print("\n" + option_message + "\n" + ("-" * len(option_message)))

	action = input("1(A) = Open/Close Main Garage Door\n2(B) = Open/Close Second Garage Door\nX = Exit\n")
	if action.upper() == "1" or action.upper() == "A":
		print("")
		door_one.toggle()
		door_one.status()
		door_two.status()
		print("")
	elif action.upper() == "2" or action.upper() == "B":
		print("")
		door_two.toggle()
		door_one.status()
		door_two.status()
		print("")
	elif action.upper() == "X":
		break
	else:
		print("Not a valid selection!")
		time.sleep(2)
		print("")

# before we shut down, let's check to make sure the garage doors are closed
if door_one.door_open:
	print("\n" + ("*" * len(door_one_warning_message)) + "\n" + door_one_warning_message + "\n" + ("*" * len(door_one_warning_message)) + "\n")
	action = input("Shall I close Garage Door 1 for you? ")
	if action[:1].upper() == 'Y':
		door_one.close()
		door_one.status()
	else:
		print("Okay, we will leave Garage Door 1 open.")

if door_two.door_open:
	print("\n" + ("*" * len(door_two_warning_message)) + "\n" + door_two_warning_message + "\n" + ("*" * len(door_two_warning_message)) + "\n")
	action = input("Shall I close Garage Door 2 for you? ")
	if action[:1].upper() == 'Y':
		door_two.close()
		door_two.status()
	else:
		print("Okay, we will leave Garage Door 2 open.")

# okay, we are shutting down so time to clean up
pfd.output_port.all_off()
pfd.deinit_board()

# print the goodbye message
#print("\n" + ("*" * len(goodbye_message)) + "\n" + goodbye_message + "\n" + ("*" * len(goodbye_message)) + "\n")
print("\n" + goodbye_message + "\n")
