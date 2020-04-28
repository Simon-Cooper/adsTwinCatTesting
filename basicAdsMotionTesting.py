
def absolutePositionTest(plc,axisNum,targetPosition,velocity,threshold,timeout=10):
    mf.moveAbsolute(plc,axisNum,targetPosition,velocity)
    if mf.waitForDone(plc,axisNum,timeout) == False:
        print("Timeout on absolute move")
        return False
    actualPosition = mf.readAxisPosition(plc,axisNum)
    posDeviation = abs(targetPosition - actualPosition)
    print('Target position: {:.3f}'.format(targetPosition))
    print('Position reached: {:.3f}'.format(actualPosition))
    print('Position deviation: {:.3f}'.format(posDeviation))
    
    if posDeviation>threshold:
        print('Test failed')
        print('\n********************\n')
        return False
    else:
        print('Test passed')
        print('\n********************\n')
        
    


import pyads
import time
import plcMotionFunctions as mf
from os import system, name
# add remote route
system('cls')
plc = pyads.Connection('5.65.74.200.1.1',852) #852 is the port of the PLC, first value is AMS net ID
plc.open()
mf.axisOn(plc, 1)
#need to actually wait for the axis to turn on, it's a bit slow
time.sleep(1)

positionTargetsList = [2,0,1,2,1,2,0,3,0]

for i in positionTargetsList:
    absolutePositionTest(plc,1,i,2,0.005)
    time.sleep(1)

mf.axisOff(plc, 1)

plc.close()

