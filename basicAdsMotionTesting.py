def moveAbsolute(axisNum,position,velocity):
    print(f"Move absolute on Axis {axisNum} to position {position} @ velocity {velocity}")
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stControl.eCommand",0, pyads.PLCTYPE_INT)
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stConfig.fVelocity",velocity, pyads.PLCTYPE_LREAL)
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stConfig.fPosition",position, pyads.PLCTYPE_LREAL)
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stControl.bExecute",True, pyads.PLCTYPE_BOOL)

def axisOn(axisNum):
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stControl.bEnable",True, pyads.PLCTYPE_BOOL)
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stConfig.fOverride",100, pyads.PLCTYPE_LREAL)

def axisOff(axisNum):
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stControl.bEnable",False, pyads.PLCTYPE_BOOL)
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stConfig.fOverride",0, pyads.PLCTYPE_LREAL)

def waitForDone(axisNum, timeout=10):
    timeLimit = time.time()+timeout
    boolTimeoutError = False;
    while(True):
        if(plc.read_by_name(f"GVL.astAxes[{axisNum}].stStatus.bBusy", pyads.PLCTYPE_BOOL)):
            break
        if time.time()>timeLimit:
            boolTimeoutError = True
            break
    while(True):
        if(plc.read_by_name(f"GVL.astAxes[{axisNum}].stStatus.bDone", pyads.PLCTYPE_BOOL)):
            break
        if time.time()>timeLimit:
            boolTimeoutError = True
            break   
    if boolTimeoutError:
        print("Timeout error")
    else:
        print("Done")

import pyads
import time
# add remote route
plc = pyads.Connection('5.65.74.200.1.1',852) #852 is the port of the PLC, first value is AMS net ID
plc.open()
axisOn(1)
moveAbsolute(1,2,2)
waitForDone(1)
time.sleep(0.5)
moveAbsolute(1,0,2)
waitForDone(1)
plc.close()

