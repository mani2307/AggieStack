from hardware import Hardware
from flavor import Flavor
from image import Image

import logging

class StackData:

    def __init__(self):
        self.hwData = Hardware()
        self.flData = Flavor()
        self.imgData = Image()

    def config (self, configuration, fileName):
        if (configuration == "hardware"):
            self.hwData.config(fileName);
        elif (configuration == "flavor"):
            self.flData.config(fileName);
        elif (configuration == "image"):
        	self.imgData.config(fileName);

    def show (self, configuration):
        if (configuration == "hardware"):
            self.hwData.show();
        elif (configuration == "flavor"):
            self.flData.show();
        elif (configuration == "images"):
        	self.imgData.show();

    def showAll (self):
        if self.hwData.getHardwareDataSize()!=0:
            self.hwData.show();
        else:
            print('\n No hardware data found\n')
        if self.flData.getFlavorsDataSize()!=0:
            self.flData.show();
        else:
            print('\n No flavors data found\n')
        if self.imgData.getImageDataSize()!=0:
            self.imgData.show();
        else:
            print('\n No images data found\n')
        logging.info('SUCCESS')

    def adminShowAvailableHardware(self):
        self.hwData.showAvailableHardware()
		
    def canHost(self, hardwareName, flavorName):
        hardware = self.hwData.getHardwareInfo(hardwareName)
        flavor = self.flData.getFlavorInfo(flavorName)
        if hardware==None or flavor==None:
            print("\n Please verify hardware name and flavor name")
            logging.error('FAILURE')
            return False
        if hardware.mem >= flavor.mem and hardware.numDisks >= flavor.numDisks and hardware.numVCpus >= flavor.numVCpus:
            return True
        else:
            return False
