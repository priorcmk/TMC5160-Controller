import time

class TMCstepperController:

    """TMCstepper Unit"""
    def __init__(self, ser,regmap, device, StepPerDegree, GearRatio):
        self.ser=ser
        self.reg=regmap
        self.dev=device
        self.StepPerDegree=StepPerDegree
        self.GearRatio=GearRatio

    def crc_calc(self,data):         # from TMC5160 datasheet
        crc=0
        for i in range(len(data)-1):
            current = data[i];
            for j in range(8):
                if((crc >> 7) ^ (current & 0x01)):
                    crc = ((crc << 1) ^ 0x07) & 0xFF;
                else:
                    crc = (crc << 1) & 0xFF;
                current = current >> 1;
        data[-1]=crc
        return data

    def tmcWrite(self,addr,data): #raw write
        addr = addr | 0x80
        data = [0x05,self.dev,addr] + data + [0x00]
        data=self.crc_calc(data)
        for i in data:
            #print(hex(i))
            self.ser.write(i.to_bytes(1,'big'))

    def tmcRead(self,addr): # raw read
        data=[0x05,self.dev,addr,0x00]
        data=self.crc_calc(data)
        for i in data:
            #print(hex(i))
            self.ser.write(i.to_bytes(1,'big'))
    #    data=self.ser.read(100)
    #    time.sleep(0.05) # does not catch up to incoming data without delay TODO find another way to read this

        while True:
            ser1=self.ser.inWaiting()
            time.sleep(0.02)
            ser2=self.ser.inWaiting()
            if(ser2==ser1):
                break

        data=self.ser.read(self.ser.inWaiting())
    #    print(data)
        data=data[-5:-1]
        return data

    def setReg(self, addr, data): # write a register (32 bit)
        if(type(addr)==type("ABC")):
            addr=self.reg[addr]
        data=self.byteToInt(data.to_bytes(4,'big'))
        self.tmcWrite(addr,data)

    def readReg(self,addr): # read a register (32 bit)
        if(type(addr)==type("ABC") and (addr in self.reg)):
            addr=self.reg[addr]
        data=self.tmcRead(addr)
        return self.byteToInt(data)

    def byteToInt(self,data):
        intData=[]
        for i in range(len(data)):
            intData= intData + [data[i]]
        return intData
    def arrayToInt(self,array): # four 8 bit element only
        return ((array[0] & 0xFF) << 24) | ((array[1] & 0xFF) << 16) | ((array[2] & 0xFF) << 8) | ((array[3] & 0xFF))

    def intToArray(self,num): # 32 bit yo 4 8 bit only
        return [((num & 0xFF000000) >> 24) , ((num & 0xFF0000) >> 16) , ((num & 0xFF00) >> 8) , ((num & 0xFF))]

    def setAddr(self,addr): # set slave address
        self.setReg(self.reg["SLAVECONF"], addr | 0xF00)
        #self.dev=addr

    def setNAO(self,bool): # set Next address line, ACTIVE low
        if(bool):
            self.setReg(self.reg["IOIN"],0)
        else:
            self.setReg(self.reg["IOIN"],1)


    def moveToDegree(self,deg): # starts a fixed number of degree rotation
        steps=round((deg/(self.StepPerDegree/256)*self.GearRatio))
        self.setReg(self.reg["XTARGET"],steps)

    def waitForStop(self): # polls
        timeStart=time.time()
        x=1
        while (x != 0):
            x=self.arrayToInt(self.readReg(self.reg["VACTUAL"]))
            #print(x)
            if(time.time()-timeStart > 10):
                print("The motor timed out while moving")
                return 0
        if(self.readReg(self.reg["XACTUAL"]) != self.readReg(self.reg["XTARGET"])):
            if((self.readReg("IOIN")[3] & 0x01) == 0):
                self.setReg("XTARGET",0)
                self.setReg("XACTUAL",0)
                print ("Homed")
                return 1
            print("Motion Error, did not move correctly")
            print(self.readReg(self.reg["XACTUAL"]))
            print(self.readReg(self.reg["XTARGET"]))
            return 0
        return 1
    def disableDriver(self):
        self.setReg(self.reg["CHOPCONF"],0x10410150)
