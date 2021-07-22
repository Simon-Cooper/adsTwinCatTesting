AMS_NET_ID = '5.79.68.132.1.1'  #User needs to update this to match AMS NET ID of controller
PLC_PORT = 852  #Default port number for our collaboration code
AXIS_ID = 1

import pyads
import time
import plcMotionFunctions as mf
from testScripts import *
from os import system, name

system('cls') #clears the terminal window4
plc = pyads.Connection(AMS_NET_ID, PLC_PORT) #Creates the PLC connection object#

while True:
    try:
        plc.open() #Start connection to the PLC
        break
    except ValueError:
        print("Error opening PLC connection")
        break

#<Here would probably want to execute scripts in a test folder>
testAxis = mf.testClass(plc,AXIS_ID)
testAxis.axisOn()

if testAxis.waitForOn() == False:
    plc.close()
    print("Axis failed to enable. Press enter key to exit")
    input()
    system.exit()


#pointMoves(testAxis,20)
testAxis.moveToHighLimit(10)
time.sleep(1)
testAxis.moveToLowLimit(10)
time.sleep(1)
testAxis.moveToLowLimit(-20)
plc.close()
