import pyads
import time

class testClass:
    def __init__(self,plc,axisNum):
        self.plc = plc
        self.axisNum = axisNum

    def axisOn(self):
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.bEnable",True, pyads.PLCTYPE_BOOL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stConfig.fOverride",100, pyads.PLCTYPE_LREAL)

    def axisOff(self):
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.bEnable",False, pyads.PLCTYPE_BOOL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stConfig.fOverride",0, pyads.PLCTYPE_LREAL)

    def moveAbsolute(self, position, velocity):
        print('Move absolute on Axis {} to position {:.2f} @ velocity {:.2f}'.format(self.axisNum,position,velocity))
        #print(f"Move absolute on Axis {axisNum} to position {position} @ velocity {velocity}")
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.eCommand",0, pyads.PLCTYPE_INT)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stConfig.fVelocity",velocity, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stConfig.fPosition",position, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.bExecute",True, pyads.PLCTYPE_BOOL)

    def waitForDone(self, timeout=10):
        timeLimit = time.time()+timeout
        boolTimeoutError = False;
        while(True):
            if(self.plc.read_by_name(f"GVL.astAxes[{self.axisNum}].stStatus.bBusy", pyads.PLCTYPE_BOOL)):
                break
            if time.time()>timeLimit:
                boolTimeoutError = True
                break
        while(True):
            if(self.plc.read_by_name(f"GVL.astAxes[{self.axisNum}].stStatus.bDone", pyads.PLCTYPE_BOOL)):
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

    def readAxisPosition(self):
        return self.plc.read_by_name(f"GVL.astAxes[{self.axisNum}].stStatus.fActPosition",pyads.PLCTYPE_LREAL)
