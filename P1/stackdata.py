from hardware import Hardware, HardwareData, RackData
from flavor import Flavor
from image import Image
from server import Server
from texttable import Texttable
import logging

class StackData:

    def __init__(self):
        self.hwData = Hardware()
        self.flData = Flavor()
        self.imgData = Image()
        self.serverData = Server()

    def config(self, configuration, fileName):
        if configuration == "hardware":
            self.hwData.config(fileName);
        elif configuration == "flavor":
            self.flData.config(fileName);
        elif configuration == "image":
            self.imgData.config(fileName);

    def show(self, configuration):
        if configuration == "hardware":
            self.hwData.show();
        elif configuration == "flavor":
            self.flData.show();
        elif configuration == "images":
            self.imgData.show();
        elif configuration == "server list":
            self.serverData.showServer()
        elif configuration == "server instance":
            self.serverData.showInstance()

    def showAll(self):
        if self.hwData.getHardwareDataSize() != 0:
            self.hwData.show();
        else:
            print('\n No hardware data found\n')
        if self.flData.getFlavorsDataSize() != 0:
            self.flData.show();
        else:
            print('\n No flavors data found\n')
        if self.imgData.getImageDataSize() != 0:
            self.imgData.show();
        else:
            print('\n No images data found\n')
        logging.info('SUCCESS')

    def deleteInstance(self, name):
        if name in self.serverData.serverDataDict:
            server = self.serverData.serverDataDict[name]
            flavor = self.flData.getFlavorInfo(server.flName)
            allocated = self.hwData.allocatedHardware[server.mcName]
            allocated.mem = allocated.mem - flavor.mem
            allocated.numVCpus = allocated.numVCpus - flavor.numVCpus
            allocated.numDisks = allocated.numDisks - flavor.numDisks
            if allocated.mem > 0:
                self.hwData.allocatedHardware[name] = allocated
            else:
                self.hwData.allocatedHardware.pop(server.mcName, None)

            self.serverData.serverDataDict.pop(name, None)
        else:
            print("ERROR!! Instance Not Found..")

    def validateImageAndFlavor(self,imageName, flavorName):
        if((imageName in self.imgData.imageDict.keys()) and (flavorName in self.flData.flDataDict.keys())):
            return True
        else:
            return False

    def createInstance(self, serverName, imageName, flavorName):
        if(self.validateImageAndFlavor(imageName, flavorName)):
            mcName = self.getMachine(flavorName, imageName)
            if len(mcName) > 0:
                print(mcName)
                self.serverData.config(serverName, imageName, flavorName, mcName)
                logging.info('SUCCESS')
            else:
                logging.error("No available hardware found")
        else:
            print("ERROR! Image name or file name not found")

    def getMachine(self, flavorName, imageName):
        #aggiestack server create --image linux-ubuntu-16 --flavor small ins1
        flavor = self.flData.getFlavorInfo(flavorName)
		
        availableMachines = []
		
		# Find available machines
        for name, hwData in self.hwData.hwDataDict.items():
            availMem = hwData.mem
            availNoDisks = hwData.numDisks
            availVcpus = hwData.numVCpus
            if name in self.hwData.allocatedHardware:
                allocated = self.hwData.allocatedHardware[name]
                availMem = availMem - allocated.mem
                availNoDisks = availNoDisks - allocated.numDisks
                availVcpus = availVcpus - allocated.numVCpus
            if availMem >= flavor.mem and availNoDisks >= flavor.numDisks and availVcpus >= flavor.numVCpus:
                availableMachines.append(name)

        # Find the machine whose rack has the image
        for name in availableMachines:
            rackName = self.hwData.hwDataDict[name].rack
            storedImagesList = self.hwData.rackDataDict[rackName].stored_images
            if imageName in storedImagesList:
                print ("Image already found")
                allocated = self.hwData.allocatedHardware.get(name, HardwareData())
                allocated.name = name
                allocated.mem = allocated.mem + flavor.mem
                allocated.numDisks = allocated.numDisks + flavor.numDisks
                allocated.numVCpus = allocated.numVCpus + flavor.numVCpus
                self.hwData.allocatedHardware[name] = allocated				
                return name				

        # Find any rack where this image can be inserted
        for name in availableMachines:
            rackName = self.hwData.hwDataDict[name].rack
            rackStorage = self.hwData.rackDataDict[rackName].capacity            
            if rackStorage >= int(self.imgData.imageDict[imageName].noOfAvailable):
                # Copy image to rack storage
                self.hwData.rackDataDict[rackName].stored_images.append(imageName)
                self.hwData.rackDataDict[rackName].capacity -= int(self.imgData.imageDict[imageName].noOfAvailable)
                print ("Image added to rack storage")
                # Return Machine name by updating the parameters
                allocated = self.hwData.allocatedHardware.get(name, HardwareData())
                allocated.name = name
                allocated.mem = allocated.mem + flavor.mem
                allocated.numDisks = allocated.numDisks + flavor.numDisks
                allocated.numVCpus = allocated.numVCpus + flavor.numVCpus
                self.hwData.allocatedHardware[name] = allocated				
                return name

        if len(availableMachines) == 0:
            return ''
        else:
            # Simply add an instance to any machine
            name = availableMachines[0]
            allocated = self.hwData.allocatedHardware.get(name, HardwareData())
            allocated.name = name
            allocated.mem = allocated.mem + flavor.mem
            allocated.numDisks = allocated.numDisks + flavor.numDisks
            allocated.numVCpus = allocated.numVCpus + flavor.numVCpus
            self.hwData.allocatedHardware[name] = allocated
            return name
		
    def adminShowAvailableHardware(self):
        self.hwData.showAvailableHardware()

    def canHost(self, hardwareName, flavorName):
        hardware = self.hwData.getHardwareInfo(hardwareName)
        flavor = self.flData.getFlavorInfo(flavorName)
        if hardware is None or flavor is None:
            print("\n Please verify hardware name and flavor name")
            logging.error('FAILURE')
            return False
        if hardware.mem >= flavor.mem and hardware.numDisks >= flavor.numDisks and hardware.numVCpus >= flavor.numVCpus:
            return True
        else:
            return False

    def remove(self, machineName):
        #removes the machine from the available list
        #first remove all the linked instances
        tempInst = []
        for name, svData in self.serverData.serverDataDict.items():
            if (svData.mcName == machineName):
                tempInst.append(svData.name)

        # for name in tempInst:
        #         self.deleteInstance(name)

        if (len(tempInst) > 0):
            logging.error("Can not remove. Migrate the running instance from this machine")
            print("Can not remove. Migrate the running instance from this machine")
            return

        try:
            del self.hwData.hwDataDict[machineName]
            self.hwData.numOfMachines -= 1
            logging.info ("Machine removed")
        except KeyError as ex:
            logging.error("This machine does not exist")

    def addMachine(self, mem, disk, vcpu, ip, r_name, m_name):
        hwData = HardwareData()
        if(r_name not in self.hwData.rackDataDict.keys()):
            print("This rack does not exist, can not add machine")
            logging.error("This rack does not exist, can not add machine")
            return

        hwData.name = m_name
        hwData.rack = r_name
        hwData.ip = ip
        hwData.mem = mem
        hwData.numDisks = disk
        hwData.numVCpus = vcpu
        self.hwData.hwDataDict[m_name] = hwData

    def findRack(self, rackName):
        for name, rackData in self.hwData.rackDataDict.items():
            if(rackData.name!= rackName):
                subsRack = rackData.name
                self.hwData.rackDataDict.pop(rackName)
                return subsRack
                
    def evacuateRack(self, rackName):
        if(rackName in self.hwData.rackDataDict.keys()):
            substituteRack = self.findRack(rackName)
            if(substituteRack == None):
                print("Rack Not evacuated, No other rack found")
            else:
                for name, hwData in self.hwData.hwDataDict.items():
                    if(hwData.rack == rackName):
                        hwData.rack = substituteRack
                        self.hwData.hwDataDict[name] = hwData
        else:
            print(" Error!! RackName Not Found ")

    def adminShowCachedImagesOnRack(self, rackName):
        if rackName in self.hwData.rackDataDict:
            storedImagesList = self.hwData.rackDataDict[rackName].stored_images
            data = [["List of Images"]]
            for image in storedImagesList:
                data.append([image])
            rackStorage = self.hwData.rackDataDict[rackName].capacity
            T = Texttable()
            T.add_rows(data)
            print(T.draw())
            print("The amount of storage available in the given rack is ", rackStorage)
        else:
            print("Please enter valid rack-name")