import pyads
import time

def axisOn(plc, axisNum):
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stControl.bEnable",True, pyads.PLCTYPE_BOOL)
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stConfig.fOverride",100, pyads.PLCTYPE_LREAL)

def axisOff(plc, axisNum):
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stControl.bEnable",False, pyads.PLCTYPE_BOOL)
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stConfig.fOverride",0, pyads.PLCTYPE_LREAL)

def moveAbsolute(plc, axisNum, position, velocity):
    print('Move absolute on Axis {} to position {:.2f} @ velocity {:.2f}'.format(axisNum,position,velocity))
    #print(f"Move absolute on Axis {axisNum} to position {position} @ velocity {velocity}")
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stControl.eCommand",0, pyads.PLCTYPE_INT)
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stConfig.fVelocity",velocity, pyads.PLCTYPE_LREAL)
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stConfig.fPosition",position, pyads.PLCTYPE_LREAL)
    plc.write_by_name(f"GVL.astAxes[{axisNum}].stControl.bExecute",True, pyads.PLCTYPE_BOOL)

def waitForDone(plc, axisNum, timeout=10):
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
        return False
    else:
        print("Done")
        return True

def readAxisPosition(plc, axisNum):
    return plc.read_by_name(f"GVL.astAxes[{axisNum}].stStatus.fActPosition",pyads.PLCTYPE_LREAL)
