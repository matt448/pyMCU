#!/usr/bin/python

import pymcu           # Import the pymcu module
import time            # Import time module for sleep functions


########################################
# Functions
########################################

#Blank the lcd screen by printing spaces
def blanklcd():
    mb.lcd(1,'                              ')
    mb.lcd(2,'                              ')
    mb.lcd(3,'                              ')
    mb.lcd(4,'                              ')

#Read value from DS18B20 temperature sensor
#Need to pass digital pin number, lcd line and flag for F or C units

def readtemp(pin,lcdline,ForC):
    mb.owWrite(pin,1,0x33)
    ReadVal = mb.owRead(7,0,8)
    mb.owWrite(7,1,0xCC)
    mb.owWrite(7,0,0x44)
    mb.owWrite(7,1,0xCC)
    mb.owWrite(7,0,0xBE)
    ReadVal = mb.owRead(7,0,12)
    HexVal1 = hex(ReadVal[1])
    HexVal2 = hex(ReadVal[0])
    HexVal1 = HexVal1[2:4]
    HexVal2 = HexVal2[2:4]
    HexVal = '0x'+HexVal1+HexVal2
    DecVal = int(HexVal, 0)
    TempC = (DecVal * 0.0625)
    TempF = ((TempC*9)/5)+32
    TempFR = round(TempF, 1)
    TempCR = round(TempC, 1)
    if ForC:
        mb.lcd(lcdline,'Temp: ' + str(TempFR) + chr(int(223)) + 'F   ')
	return TempFR
    else:
        mb.lcd(lcdline,'Temp: ' + str(TempCR) + chr(int(223)) + 'C   ')
	return TempCR
    

########################################
# Main Program
########################################


fileout = "/tmp/temperature.out"

mb = pymcu.mcuModule() # Initialize mb (My Board) with mcuModule Class Object - Find first available pymcu hardware module.
print mb
mb.lcd()               # Initialize the LCD
mb.pinLow(1)
mb.pinLow(2)
mb.mcuInfo()

time.sleep(1)          # Wait for LCD to Initialize

blanklcd()
time.sleep(0.07)

##########12345678901234567890
mb.lcd(1,'  ----------------  ')
mb.lcd(2,'   Garage Monitor   ')
mb.lcd(3,'  ----------------  ')
time.sleep(2)

blanklcd()
time.sleep(0.07)

counter = 1
outcntr = 1
maxcount = 90000

print 'Running sensor application....'
print
print 'Press Ctrl-C to stop'

#while counter <= maxcount:
while(1): 
    mb.pinHigh(1)

    mb.lcd(1,time.strftime("%m/%d/%Y  %I:%M %p"))
    #Read button state from pin D13
    #and print status to lcd
    #buttonstate = mb.digitalRead(13)
    #strbuttonstate = str(buttonstate)
    #mb.lcd(2,'  button: ' + strbuttonstate)

    #Need to pass digital pin number and lcd line
    tempout = readtemp(7,4,1)

    #Check state of door switch
    mb.digitalState(12, 'input')
    if mb.digitalRead(12):
        mb.lcd(3,'DOOR CLOSED')
        mb.pinLow(2)
    else:
        mb.lcd(3,'DOOR OPEN  ')
        mb.pinHigh(2)
        
    #Read values for light sensor on pin A3
    A3volts = mb.analogRead(3)
    ##print str(A3volts)
    mb.lcd(2,'Light Level: ' + str(A3volts) + '    ')
    A3realvolts = ((A3volts)/1024.0)*5
    A3realvolts = round(A3realvolts, 4)
    
    #print 'Loop ' + str(counter) + ' of ' + str(maxcount)
    time.sleep(0.5)
    mb.pinLow(1)
    counter=counter+1
    outcntr=outcntr+1
    #print 'TEMP: ' + str(tempout)
    if outcntr == 30:
	FILE = open(fileout,"w")
	FILE.write(str(tempout))
	FILE.close()
	outcntr=0
	

#blanklcd()
mb.lcd(4,'END PROGRAM        ')
mb.pinLow(1)
mb.pinHigh(2)
time.sleep(1)
mb.pinLow(2)
mb.close()

