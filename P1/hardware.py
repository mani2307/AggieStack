from texttable import Texttable
from flavor import FlavorData

import logging


class Hardware:

    def __init__(self):
        self.numOfMachines = ''
        self.hwDataDict = {}
        self.noOfRacks = ''
        self.rackDataDict = {}
        # Key: hw_name/server name
        # Value: list of flavours allocated
        self.allocatedHardware = {}

    def config(self, fileName):
        hwDataTempDict = {}
        with open(fileName) as f:
            rackOrMachine=0
            for line in f:
                data = line.split()
                hwData = HardwareData()
                rackData = RackData()

                if (len(data) > 1) and rackOrMachine == 2:
                    if (len(data) == 6 and self.isValid(data)):
                        hwData.name = data[0]
                        hwData.rack = data[1]
                        hwData.ip = data[2]
                        hwData.mem = int(data[3])
                        hwData.numDisks = int(data[4])
                        hwData.numVCpus = int(data[5])
                        hwDataTempDict[data[0]] = hwData

                    else:
                        print("Skipping file ...")
                        logging.error('Data not proper, config not complete, Skipping file ...')
                        return
                elif (len(data) == 1) and rackOrMachine == 1:
                    self.numOfMachines = int(data[0])
                    rackOrMachine = 2
                elif (len(data) == 1) and rackOrMachine == 0:
                    self.noOfRacks = int(data[0])
                    rackOrMachine = 1
                elif (len(data) > 1) and rackOrMachine == 1:
                    rackData.name = data[0]
                    rackData.capacity = int(data[1])
                    self.rackDataDict[data[0]] = rackData


        # self.hwDataList.extend(hwDataTempList)
        # self.hwDataDict = {**hwDataTempDict,**self.hwDataDict} this is order dependent, use update
        self.hwDataDict.update(hwDataTempDict)
        logging.info('SUCCESS')

    def isValid(self, data):
        if ((not data[3].isdigit()) or (not data[4].isdigit()) or (not data[5].isdigit())):
            return False
        else:
            return True

    def show(self):
        tempDataList = []
        tempDataList.append(['Name', 'Rack','IP', 'MEM', 'Num-Disks', 'Num-vcpus'])
        for name, hwData in self.hwDataDict.items():
            tempList = []
            tempList.append(hwData.name)
            tempList.append(hwData.rack)
            tempList.append(hwData.ip)
            tempList.append(hwData.mem)
            tempList.append(hwData.numDisks)
            tempList.append(hwData.numVCpus)
            tempDataList.append(tempList)

        T = Texttable()
        T.add_rows(tempDataList)
        print(T.draw())
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
        tempDataList.append(['Name', 'IP', 'Rack', 'MEM', 'Num-Disks', 'Num-vcpus'])
        if len(self.hwDataDict) == 0:
            print('\n Please configure the hardware \n')
        for name, hwData in self.hwDataDict.items():
            tempList = []
            if hwData.name not in self.allocatedHardware:
                tempList.append(hwData.name)
                tempList.append(hwData.ip)
                tempList.append(hwData.rack)
                tempList.append(hwData.mem)
                tempList.append(hwData.numDisks)
                tempList.append(hwData.numVCpus)
            else:
                totalAllocated = FlavorData()
                totalAllocated.mem = 0
                totalAllocated.numDisks = 0
                totalAllocated.numVCpus = 0
                obj = self.allocatedHardware.get(hwData.name, HardwareData)
                totalAllocated.mem += obj.mem
                totalAllocated.numDisks += obj.numDisks
                totalAllocated.numVCpus += obj.numVCpus
                tempList.append(hwData.name)
                tempList.append(hwData.ip)
                tempList.append(hwData.rack)
                tempList.append(hwData.mem - totalAllocated.mem)
                tempList.append(hwData.numDisks - totalAllocated.numDisks)
                tempList.append(hwData.numVCpus - totalAllocated.numVCpus)
            tempDataList.append(tempList)
        T = Texttable()
        T.add_rows(tempDataList)
        print(T.draw())
        logging.info('SUCCESS')


class HardwareData:
    def __init__(self):
        self.name = ""
        self.rack = ""
        self.ip = ""
        self.mem = 0
        self.numDisks = 0
        self.numVCpus = 0

class RackData:
    def __init__(self):
        self.name = ""
        self.capacity = 0
        self.stored_images = []