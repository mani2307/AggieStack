from texttable import Texttable
import logging


class Server:
    def __init__(self):
        self.serverDataDict = {}

    def config(self, svName, imgName, flName, mcName):
        svData = ServerData()
        svData.name = svName
        svData.imgName = imgName
        svData.flName = flName
        svData.mcName = mcName
        self.serverDataDict[svName] = svData
        logging.info('SUCCESS')

    def isValid(self, data):
        return True

    def showServer(self):
        tempDataList = []
        tempDataList.append(['Name', 'Image Name', 'Flavor Name'])
        for name, svData in self.serverDataDict.items():
            tempList = []
            tempList.append(svData.name)
            tempList.append(svData.imgName)
            tempList.append(svData.flName)
            tempDataList.append(tempList)

        T = Texttable()
        T.add_rows(tempDataList)
        print(T.draw())
        logging.info('SUCCESS')

    def showInstance(self):
        tempDataList = []
        tempDataList.append(['Name', 'Machine Name'])
        for name, svData in self.serverDataDict.items():
            tempList = []
            tempList.append(svData.name)
            tempList.append(svData.mcName)
            tempDataList.append(tempList)
        T = Texttable()
        T.add_rows(tempDataList)
        print(T.draw())
        logging.info('SUCCESS')

    def getServerDataSize(self):
        return len(self.flDataDict)


class ServerData:
    def __init__(self):
        self.name = ""
        self.imgName = ''
        self.flName = ''
        self.mcName = ''