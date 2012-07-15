#!/usr/bin/python
#
# Written by Matthew McMillan
# matthew.mcmillan at gmail dot com
#
# This code reads a temperature value from
# a DS18B20 sensor using a pyMCU board. It only
# reads from a single sensor.
#
import pymcu           # Import the pymcu module

#Function to read value from DS18B20 temperature sensor
#Need to pass digital pin number, lcd line and flag for F or C units
#
# 0x33	READ ROM. Read single device address.
# 0xCC	SKIP ROM. Address all devices on the bus
# 0x44  CONVERT T. Initiate temperature conversion
# 0xBE  READ SCRATCHPAD. Initiate read temp stored in the scratchpad.

def readtemp(pin,ForC):
    mb.owWrite(pin,1,0x33)
    ReadVal = mb.owRead(pin,0,8)
    mb.owWrite(pin,1,0xCC)
    mb.owWrite(pin,0,0x44)
    mb.owWrite(pin,1,0xCC)
    mb.owWrite(pin,0,0xBE)
    ReadVal = mb.owRead(pin,0,12)
    HexVal1 = hex(ReadVal[1])
    HexVal2 = hex(ReadVal[0])
    HexVal1 = HexVal1[2:4]
    HexVal2 = HexVal2[2:4]
    HexVal = '0x'+HexVal1+HexVal2
    DecVal = int(HexVal, 0)
    TempC = (DecVal * 0.0625)
    if ForC:
    	TempF = ((TempC*9)/5)+32
    	TempFR = round(TempF, 1)
        return TempFR
    else:
	TempCR = round(TempC, 1)
        return TempCR

################
# Main program
################

# Initialize mb (My Board) with mcuModule Class Object
mb = pymcu.mcuModule() 

#Need to pass digital pin number and ForC
tempout = readtemp(7,1)

print 'Temp: ' + str(tempout)
