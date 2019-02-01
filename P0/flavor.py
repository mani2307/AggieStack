from texttable import Texttable
import logging


class Flavor:
    def __init__(self):
        self.noOfFlavors=''
        self.flDataDict={}

    def config (self, fileName):
        flDataTempDict = {}
        with open(fileName) as f:
            for line in f:
                data = line.split()
                flData = FlavorData()
                if(len(data)>1):
                    if(len(data)==4 and self.isValid(data)):
                        flData.name = data[0]
                        flData.mem = data[1]
                        flData.numDisks = data[2]
                        flData.numVCpus = data[3]
                        flDataTempDict[data[0]]=flData
                    else:
                        #logging.error('Data Missing')
                        print("data invalid, skipping file")
                        logging.error('Data not proper, config not complete, Skipping file ...')
                        return
                else:
                    self.noOfFlavors = data[0]
        self.flDataDict.update(flDataTempDict)
        logging.info('SUCCESS')

    
    def isValid(self,data):
        return True

    def show(self):
        tempDataList = []
        tempDataList.append(['Name', 'RAM-in-GB', 'Num-Disks' , 'Num-vcpus'])
        for name, flData in self.flDataDict.items():
                tempList = []
                tempList.append(flData.name)
                tempList.append(flData.mem)
                tempList.append(flData.numDisks)
                tempList.append(flData.numVCpus) 
                tempDataList.append(tempList)
                
        T = Texttable()
        T.add_rows(tempDataList)
        print (T.draw()) 
        logging.info('SUCCESS')
		
    def getFlavorInfo(self, flName):
        for name, flavor in self.flDataList.items():
            if flavor.name == flName:
                return flavor
        return None

    def getFlavorsDataSize(self):
        return len(self.flDataDict)

class FlavorData:
    def __init__(self):
        self.name = ""
        self.mem = ''
        self.numDisks = ''
        self.numVCpus = ''