
AMS_NET_ID = '5.65.74.200.1.1'
PLC_PORT = 852

def absolutePositionTest(targetPosition,velocity,threshold,timeout=10):
    axis1.moveAbsolute(targetPosition,velocity)
    if axis1.waitForDone(timeout) == False:
        print("Timeout on absolute move")
        return False
    actualPosition = axis1.readAxisPosition()
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
plc = pyads.Connection(AMS_NET_ID, PLC_PORT) #Setup PLC connection
plc.open() #Open PLC connection
axis1 = mf.testClass(plc,1) #Setup testclass with current PLC
axis1.axisOn()
#need to actually wait for the axis to turn on, it's a bit slow
time.sleep(1)

positionTargetsList = [2,0,1,2,1,2,0,3,0]

for i in positionTargetsList:
    absolutePositionTest(i,2,0.005)
    time.sleep(1)

axis1.axisOff()

plc.close()

