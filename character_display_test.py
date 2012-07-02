#!/usr/bin/python

# This script loops through all ASCII character codes
# and displays them on the LCD screen. It is currently
# configured for a 20x4 screen.
# I created this to look for which characters my LCD
# can display other than the basic A-Z and 0-9.

import pymcu           # Import the pymcu module
import time            # Import time module for sleep functions


def blanklcd():
    mb.lcd(1,'                              ')   # Blank the display
    mb.lcd(2,'                              ')
    mb.lcd(3,'                              ')
    mb.lcd(4,'                              ')

    
    
mb = pymcu.mcuModule() # Initialize mb (My Board) with mcuModule Class Object - Find first available pymcu hardware module.
print mb
mb.lcd()               # Initialize the LCD
mb.pinLow(1)
mb.pinLow(2)
mb.mcuInfo()

time.sleep(1)          # Wait for LCD to Initialize

blanklcd()
time.sleep(0.07)

mb.lcd(1,'  ---- pyMCU -----')
mb.lcd(3,'Character Display ')
time.sleep(2)

blanklcd()
time.sleep(0.07)

counter = 1
maxcount = 254

while counter <= maxcount:
    #dispchr = raw_input("Enter Character: ")
    mb.lcd(1,'Character No: ' + str(counter))
    mb.lcd(3,'      ' + chr(int(counter)) + chr(int(counter)) + chr(int(counter)))
    time.sleep(1)
    counter=counter+1


mb.lcd(4,'END PROGRAM        ')
mb.pinLow(1)
mb.pinHigh(2)
time.sleep(1)
mb.pinLow(2)
mb.close()
