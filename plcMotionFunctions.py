MOVE_ABSOLUTE = 0
MOVE_RELATIVE = 1
JOG = 2
MOVE_VELOCITY = 3
MOVE_MODULO = 4
HOME = 10


import pyads
import time

class testClass:
    def __init__(self,plc,axisNum):
        self.plc = plc
        self.axisNum = axisNum

    def axisOn(self):
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.bEnable",True, pyads.PLCTYPE_BOOL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stConfig.fOverride",100, pyads.PLCTYPE_LREAL)

    def waitForOn(self, timeout=10):
        timeLimit = time.time()+timeout
        boolTimeoutError = False;
        while(True):
            if(self.checkAxisOn()):
                break
            if time.time()>timeLimit:
                boolTimeoutError = True
                break
        if boolTimeoutError:
            print("Timeout: Axis " +axisNum+ " not enabled")
            return False
        else:
            print('Axis {} Enabled'.format(self.axisNum))
            return True

    def checkAxisOn(self):
        return self.plc.read_by_name(f"GVL.astAxes[{self.axisNum}].stStatus.bEnabled",pyads.PLCTYPE_BOOL)

    def axisOff(self):
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.bEnable",False, pyads.PLCTYPE_BOOL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stConfig.fOverride",0, pyads.PLCTYPE_LREAL)

    def moveAbsolute(self, position, velocity):
        print('Move absolute on Axis {} to position {:.2f} @ velocity {:.2f}'.format(self.axisNum,position,velocity))
        #print(f"Move absolute on Axis {axisNum} to position {position} @ velocity {velocity}")
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.eCommand",MOVE_ABSOLUTE, pyads.PLCTYPE_INT)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.fVelocity",velocity, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.fPosition",position, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.bExecute",True, pyads.PLCTYPE_BOOL)

    def moveRelative(self, position, velocity):
        print('Relative position move on {}: {:.2f} @ velocity {:.2f}'.format(self.axisNum, position, velocity))
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.eCommand",MOVE_RELATIVE, pyads.PLCTYPE_INT)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.fVelocity",velocity, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.fPosition",position, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.bExecute",True, pyads.PLCTYPE_BOOL)

    def moveVelocity(self, velocity):
        print('Continuos velocity move on Axis {} @ velocity {:.2f}'.format(self.axisNum, velocity))
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.eCommand",MOVE_VELOCITY, pyads.PLCTYPE_INT)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.fVelocity",velocity, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name(f"GVL.astAxes[{self.axisNum}].stControl.bExecute",True, pyads.PLCTYPE_BOOL)

    def moveToHighLimit(self, velocity,timeout=30):
        timeLimit = time.time()+timeout
        boolTimeoutError = False;
        if velocity<0:
            print("Incorrect velocity for fwd movement")
            return False
        self.moveVelocity(velocity)
        while(True):
            if(self.plc.read_by_name(f"GVL.astAxes[{self.axisNum}].stStatus.bFwEnabled", pyads.PLCTYPE_BOOL))==False:
                print("Forward limit reached")
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

    def moveToLowLimit(self, velocity,timeout=30):
        timeLimit = time.time()+timeout
        boolTimeoutError = False;
        if velocity>0:
            print("Incorrect velocity for bwd movement")
            return False
        self.moveVelocity(velocity)
        while(True):
            if(self.plc.read_by_name(f"GVL.astAxes[{self.axisNum}].stStatus.bBwEnabled", pyads.PLCTYPE_BOOL))==False:
                print("Backward limit reached")
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
