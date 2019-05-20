import serial
import time
import TMCMotorDriver
import TMC5160RegMap

def tmcInit(tmc,current): #set reasonable typical setting to all motors
    tmc.tmcWrite(TMC5160RegMap.regmap["CHOPCONF"],[0x00,0x01,0x00,0xC5])
    tmc.tmcWrite(TMC5160RegMap.regmap["IHOLD_IRUN"],[0x00,0x01,0x1F,current])
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
    tmc.setReg(TMC5160RegMap.regmap["RAMPMODE"],0)

def enumerateTmc(tmcArray): # assign each driver a unique address
    dummy=TMCMotorDriver.TMCstepperController(ser,TMC5160RegMap.regmap,0,0,1,0)
    for i in tmcArray:
        dummy.setAddr(i.dev)
        i.setNAO(1)

def createTmcArray(num,StepPerDegree):
    tmcArray=[]
    GearRatio=[4.25,1.0,(5+2.0/11.0),(46+82.0/125.0),(46+82.0/125.0)]
    maxAngles=[99999,360,360,360,360]
    for i in range(num):
        tmcArray = tmcArray + [TMCMotorDriver.TMCstepperController(ser,TMC5160RegMap.regmap,(255-(i+1)),StepPerDegree,GearRatio[i],maxAngles[i])]
    return tmcArray
def tmcTo(driver,deg):
    driver.moveToDegree(deg)
    driver.waitForStop()

#ser=serial.Serial('/dev/ttyUSB1', 4800, timeout=0.1)
#StepPerDegree=1.8
#tmcArray=createTmcArray(5,StepPerDegree)
#enumerateTmc(tmcArray)
try:

#        tmcInit(i)

    #    tmcInit(tmcArray[4],0x7F)
    #    tmcInit(tmcArray[3],0x7F)
    #    tmcInit(tmcArray[2],0x40)
    #    tmcInit(tmcArray[1],0x40)
    #for i in tmcArray:
    #    i.moveToDegree(0.01)
    #    tmcArray[4].moveToDegree(1)
    #    tmcArray[3].moveToDegree(1)
    #    tmcArray[2].moveToDegree(1)
    #    tmcArray[1].moveToDegree(1)
#    for i in tmcArray:
    #    tmcArray[4].waitForStop()
    #    tmcArray[3].waitForStop()
#    for i in tmcArray:
#        tmcArray[4].moveToDegree(10)
#    for i in tmcArray:
#        tmcArray[4].waitForStop()
#    for i in tmcArray:
#        i.setReg(TMC5160RegMap.regmap["RAMPMODE"],1)
    ser=serial.Serial('/dev/ttyUSB0', 4800, timeout=0.1)
    StepPerDegree=1.8
    tmcArray=createTmcArray(5,StepPerDegree)
    enumerateTmc(tmcArray)
    #for i in tmcArray:
    #tmcInit(tmcArray[3],0x7F)
    #tmcInit(tmcArray[4],0x7F)
    tmcInit(tmcArray[0],128)
    tmcInit(tmcArray[1],128)
    tmcInit(tmcArray[2],128)
    tmcInit(tmcArray[3],128)
    tmcInit(tmcArray[4],128)
    #tmcInit(tmcArray[3],0x7F)
    #tmcArray[3].setReg(TMC5160RegMap.regmap["VMAX"],80000)
    #tmcArray[4].setReg(TMC5160RegMap.regmap["VMAX"],80000)
    tmcArray[0].setReg(TMC5160RegMap.regmap["VMAX"],8000)
    tmcArray[1].setReg(TMC5160RegMap.regmap["VMAX"],40000)
    tmcArray[2].setReg(TMC5160RegMap.regmap["VMAX"],80000)
    tmcArray[3].setReg(TMC5160RegMap.regmap["VMAX"],80000)
    tmcArray[4].setReg(TMC5160RegMap.regmap["VMAX"],80000)
    #tmcInit(tmcArray[2],0x7F)
    #tmcArray[3].setMotionMode(2)
    time.sleep(1)
    #tmcArray[1].moveToDegree(90)
    #tmcArray[1].waitForStop()
    #tmcArray[1].moveToDegree(0)
    #tmcArray[1].waitForStop()
    #tmcArray[1].moveToDegree(1)
    #tmcArray[4].disableDriver()
    #tmcArray[4].moveToDegree(1)
    #tmcArray[3].moveToDegree(10)
    #tmcArray[3].waitForStop()
    #tmcArray[1].homeMotor(2,1000)
    #tmcArray[1].moveToDegree(90)
    #tmcArray[1].waitForStop()
    #tmcArray[1].moveToDegree(0)
    #tmcArray[1].waitForStop()
    #tmcArray[2].homeMotor(2,5000)
    #tmcArray[2].moveToDegree(90)
    #tmcArray[2].waitForStop()
    #tmcArray[2].moveToDegree(0)
    #tmcArray[2].waitForStop()
    #tmcArray[4].homeMotor(2,50000)
    #tmcArray[3].homeMotor(2,50000)
    #tmcArray[3].setMotionMode(2)
    #tmcArray[0].homeMotor(2,5000)
#    tmcArray[4].moveToDegree(1)
#    tmcArray[4].waitForStop()
#    tmcArray[4].moveToDegree(0)
#    tmcArray[4].waitForStop()
#    time.sleep(1)
#    tmcArray[3].moveToDegree(80)
    #tmcArray[3].waitForStop()
    deg1=40
    tmcTo(tmcArray[0],deg1)
    tmcTo(tmcArray[4],deg1)
    tmcTo(tmcArray[3],deg1)
    tmcTo(tmcArray[2],deg1)
    tmcTo(tmcArray[1],deg1)
    time.sleep(1)
    deg1=0
    tmcTo(tmcArray[0],deg1)
    tmcTo(tmcArray[4],deg1)
    tmcTo(tmcArray[3],deg1)
    tmcTo(tmcArray[2],deg1)
    tmcTo(tmcArray[1],deg1)
    time.sleep(1)
    #tmcArray[0].moveToDegree(20)
    #tmcArray[0].waitForStop()
    #tmcArray[0].moveToDegree(0)
    #tmcArray[0].waitForStop()
    #tmcArray[4].moveToDegree(20)
    #tmcArray[4].waitForStop()
    #tmcArray[4].moveToDegree(0)
    #tmcArray[4].waitForStop()
    #tmcArray[3].moveToDegree(20)
    #tmcArray[3].waitForStop()
    #tmcArray[3].moveToDegree(0)
    #tmcArray[2].waitForStop()
    #tmcArray[2].moveToDegree(20)
    #tmcArray[2].waitForStop()
    #tmcArray[3].moveToDegree(0)
    #tmcArray[2].waitForStop()
    #tmcArray[1].moveToDegree(20)
    #tmcArray[1].waitForStop()
    #tmcArray[3].moveToDegree(0)
    #tmcArray[1].waitForStop()
    #tmcArray[0].homeMotor(2,80000)
    #tmcArray[3].moveToDegree(0)
    #tmcArray[3].waitForStop()
    #tmcArray[3].moveToDegree(10)
    #tmcArray[3].waitForStop()
    #tmcArray[2].moveToDegree(10)
    #tmcArray[2].waitForStop()
    #tmcArray[1].moveToDegree(10)
    #tmcArray[1].waitForStop()
    #tmcArray[0].moveToDegree(10)
    #tmcArray[0].waitForStop()
    #tmcArray[0].moveToDegree(0)
    #tmcArray[0].waitForStop()
    #tmcArray[3].moveToDegree(45)
    #tmcArray[3].waitForStop()
    #tmcArray[3].moveToDegree(0)
    #tmcArray[3].waitForStop()
    #tmcArray[3].disableDriver()
    #tmcArray[2].moveToDegree(5)
    #tmcArray[2].waitForStop()
    #tmcArray[2].homeMotor(2,20000)
    #tmcArray[2].moveToDegree(45)
    #tmcArray[2].waitForStop()
    #tmcArray[2].moveToDegree(0)
    #for i in tmcArray:
    #    i.disableDriver()
except Exception as exp:
    for i in tmcArray:
    #    i.disableDriver()
         i.setReg(TMC5160RegMap.regmap["VMAX"],0)
    print("Failed")
    print(exp)
#tmcArray[2].setReg(TMC5160RegMap.regmap["GCONF"],0x0D)
#tmcArray[2].setReg(TMC5160RegMap.regmap["SW_MODE"],0x1FE)
#tmcArray[2].moveToDegree(9999)
#tmcArray[2].waitForStop()
#tmcArray[2].moveToDegree(0)
#tmcArray[2].waitForStop()
#tmcArray[2].disableDriver()
