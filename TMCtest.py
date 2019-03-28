import serial
import time
import TMCMotorDriver
import TMC5160RegMap

def tmcInit(tmc): #set reasonable typical setting to all motors
    tmc.tmcWrite(TMC5160RegMap.regmap["CHOPCONF"],[0x00,0x01,0x00,0xC5])
    tmc.tmcWrite(TMC5160RegMap.regmap["IHOLD_IRUN"],[0x00,0x01,0x14,0x05])
    tmc.setReg(TMC5160RegMap.regmap["AMAX"],5000)
    tmc.setReg(TMC5160RegMap.regmap["VMAX"],80000)

    tmc.setReg(TMC5160RegMap.regmap["XACTUAL"],0)
    tmc.setReg(TMC5160RegMap.regmap["VSTART"],1000)
    tmc.setReg(TMC5160RegMap.regmap["A1"],1000)
    tmc.setReg(TMC5160RegMap.regmap["DMAX"],1000)
    tmc.setReg(TMC5160RegMap.regmap["V1"],1000)
    tmc.setReg(TMC5160RegMap.regmap["D1"],2000)
    tmc.setReg(TMC5160RegMap.regmap["VSTOP"],10)
    tmc.setReg(TMC5160RegMap.regmap["GCONF"],0x0D)
    tmc.setReg(TMC5160RegMap.regmap["SW_MODE"],0x1FE)

def enumerateTmc(tmcArray): # assign each driver a unique address
    dummy=TMCMotorDriver.TMCstepperController(ser,TMC5160RegMap.regmap,0,0,1)
    for i in tmcArray:
        dummy.setAddr(i.dev)
        i.setNAO(1)

def createTmcArray(num,StepPerDegree):
    tmcArray=[]
    GearRatio=[1.0,(5+2.0/11.0),4.25,(46+82.0/125.0),(46+82.0/125.0)]
    for i in range(num):
        tmcArray = tmcArray + [TMCMotorDriver.TMCstepperController(ser,TMC5160RegMap.regmap,(255-(i+1)),StepPerDegree,GearRatio[i])]
    return tmcArray


ser=serial.Serial('/dev/ttyUSB0', 4800, timeout=0.1)
StepPerDegree=1.8
tmcArray=createTmcArray(5,StepPerDegree)
enumerateTmc(tmcArray)
for i in tmcArray:
    tmcInit(i)
for i in tmcArray:
    i.moveToDegree(90)
for i in tmcArray:
    i.waitForStop()
for i in tmcArray:
    i.disableDriver()
#tmcArray[2].setReg(TMC5160RegMap.regmap["GCONF"],0x0D)
#tmcArray[2].setReg(TMC5160RegMap.regmap["SW_MODE"],0x1FE)
#tmcArray[2].moveToDegree(9999)
#tmcArray[2].waitForStop()
#tmcArray[2].moveToDegree(0)
#tmcArray[2].waitForStop()
#tmcArray[2].disableDriver()
