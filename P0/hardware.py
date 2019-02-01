from texttable import Texttable
from flavor import Flavor

import logging

class Hardware:

    def __init__(self):
        self.numOfMachines = ''
        self.hwDataDict = {}
		# Key: hw_name/server name
		# Value: list of flavours allocated 
        self.allocatedHardware = {}

    def config (self, fileName):
        hwDataTempDict = {}
        with open(fileName) as f:
            for line in f:
                data = line.split()
                hwData = HardwareData()

                if(len(data)>1):
                    if(len(data)==5 and self.isValid(data)):
                        hwData.name = data[0]
                        hwData.ip = data[1]
                        hwData.mem = data[2]
                        hwData.numDisks = data[3]
                        hwData.numVCpus = data[4]
                        hwDataTempDict[data[0]] = hwData

                    else:
                        print ("Skipping file ...")
                        logging.error('Data not proper, config not complete, Skipping file ...')
                        return
                else:
                    self.numOfMachines = data[0]
        #self.hwDataList.extend(hwDataTempList)
        #self.hwDataDict = {**hwDataTempDict,**self.hwDataDict} this is order dependent, use update
        self.hwDataDict.update(hwDataTempDict)
        logging.info('SUCCESS')

    def isValid(self,data):
        if((not data[2].isdigit()) or (not data[3].isdigit()) or  (not data[4].isdigit())):
            return False
        else:
            return True

    def show(self):
        tempDataList = []
        tempDataList.append(['Name', 'IP', 'MEM', 'Num-Disks' , 'Num-vcpus'])
        for name, hwData in self.hwDataDict.items():
                tempList = []
                tempList.append(hwData.name)
                tempList.append(hwData.ip)
                tempList.append(hwData.mem)
                tempList.append(hwData.numDisks)
                tempList.append(hwData.numVCpus) 
                tempDataList.append(tempList)
                
        T = Texttable()
        T.add_rows(tempDataList)
        print (T.draw()) 
        logging.info('SUCCESS')

    def getHardwareDataSize(self):
        return len(self.hwDataDict)

    def getHardwareInfo(self, hwName):
        for name, hardware in self.hwDataDict.items():
            if hardware.name == hwName:
                return hardware
        return None

    def showAvailableHardware(self):
        tempDataList = []
        tempDataList.append(['Name', 'IP', 'MEM', 'Num-Disks' , 'Num-vcpus'])
        if len(self.hwDataDict) == 0:
            print('\n Please configure the hardware \n')
        for name, hwData in self.hwDataDict.items():
            tempList = []
            if hwData.name not in self.allocatedHardware:
                tempList.append(hwData.name)
                tempList.append(hwData.ip)
                tempList.append(hwData.mem)
                tempList.append(hwData.numDisks)
                tempList.append(hwData.numVCpus) 
            else :
                totalAllocated = FlavorData()
                totalAllocated.mem = 0
                totalAllocated.numDisks = 0
                totalAllocated.numVCpus = 0
                for obj in self.allocatedHardware[hwData.name]:
                    totalAllocated.mem += obj.mem
                    totalAllocated.numDisks += obj.numDisks
                    totalAllocated.numVCpus += obj.numVCpus
                tempList.append(hwData.name)
                tempList.append(hwData.ip)
                tempList.append(hwData.mem - totalAllocated.mem)
                tempList.append(hwData.numDisks - totalAllocated.numDisks)
                tempList.append(hwData.numVCpus - totalAllocated.numVCpus) 
            tempDataList.append(tempList)
        T = Texttable()
        T.add_rows(tempDataList)
        print (T.draw()) 
        logging.info('SUCCESS')

class HardwareData:
        def __init__(self):
            self.name = ""
            self.ip = ""
            self.mem = ''
            self.numDisks = ''
            self.numVCpus = ''
