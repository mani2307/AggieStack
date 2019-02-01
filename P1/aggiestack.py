from stackdata import StackData	

import sys
import logging
import os.path

def printAvailableCommands():
    print ("========== Aggiestack II Valid commands: ==========\n")
    print ("1) aggiestack config --hardware hdwr-config.txt")
    print ("2) aggiestack config --images image-config.txt")
    print ("3) aggiestack config --flavors flavor-config.txt")
    print ("4) aggiestack show hardware")
    print ("5) aggiestack show images")
    print ("6) aggiestack show flavors")
    print ("7) aggiestack show all")
    print ("8) aggiestack admin show hardware")
    print ("9) aggiestack admin can_host [machine name] [flavor]")
    print ("10) aggiestack server create --image IMAGE --flavor FLAVOR_NAME INSTANCE_NAME")
    print ("11) aggiestack server list")
    print ("12) aggiestack admin show instances")
    print ("13) aggiestack server delete ins1")
    print ("14) aggiestack admin evacuate RACK_NAME")
    print ("15) aggiestack admin remove MACHINE")
    print ("16) aggiestack admin add –-mem MEM --disk NUM_DISKS --vcpus VCPUs --ip IP --rack RACK_NAME MACHINE")
    print ("17) aggiestack admin show imagecaches RACK_NAME")

def validateCommand(inputCommand):
    if inputCommand=='':
        logging.error('FAILURE')
        return False

    validInputs= {"quit", "aggiestack config --hardware", "aggiestack config --images", "aggiestack config --flavors",
                  "aggiestack show hardware", "aggiestack show images", "aggiestack show flavors", "aggiestack show all", 
                  "aggiestack admin show hardware", "aggiestack admin can_host", "aggiestack server list", "aggiestack admin show instances", 
                  "aggiestack admin evacuate", "aggiestack admin remove", "aggiestack admin add", "aggiestack server create", "aggiestack admin show imagecaches",
                  "aggiestack server delete"}

    fullCommand=' '.join(inputCommand)

    if "config" in fullCommand:
        fileName=inputCommand[-1].strip()
        inputCommand= inputCommand[:-1]
        if ".txt" not in fileName:
            print ('Please enter valid file name\n')
            logging.error('FAILURE')
            return False
        if os.path.isfile(fileName) == False:
            print('File does not exist \n')
            logging.error('FAILURE')
            return False
        fullCommand=' '.join(inputCommand)
    # TODO: Validation of admin commands 'can_host'
    # validate that flavor exists and hardware exists
    if "can_host" in fullCommand:
        inputCommand = inputCommand[:-2]
        fullCommand=' '.join(inputCommand)
    if "evacuate" in fullCommand:
        inputCommand = inputCommand[:-1]
        fullCommand=' '.join(inputCommand)
    if "remove" in fullCommand:
        inputCommand = inputCommand[:-1]
        fullCommand=' '.join(inputCommand)
    if "delete" in fullCommand:
        inputCommand = inputCommand[:-1]
        fullCommand=' '.join(inputCommand)
    if "add" in fullCommand:
        inputCommand = inputCommand[0:3]
        fullCommand=' '.join(inputCommand)
    if "create" in fullCommand:
        inputCommand = inputCommand[0:3]
        fullCommand = ' '.join(inputCommand)
    if "imagecaches" in fullCommand:
        inputCommand = inputCommand[:-1]
        fullCommand=' '.join(inputCommand)
    if fullCommand not in validInputs:
        logging.error('FAILURE')
        return False

    return True

def validateAddMachine(inputText):
    if inputText == '':
        logging.error('Invalid Add command')
        return False

    if (len(inputText) != 14):
        print('Incomplete command')
        logging.error('Incomplete command')
        return False
    
    if ((not inputText[4].isdigit()) or (not inputText[6].isdigit()) or (not inputText[8].isdigit())):
        print("Invalid entry")
        logging.error("Invalid entry")
        return False

    if ((inputText[3] != '--mem' and inputText[3] != '-mem') or (inputText[5] != '--disk' and inputText[5] != '-disk') or (inputText[7] != '--vcpus' 
    and inputText[7] != '-vcpus') or (inputText[9] != '--ip' and inputText[9] != '-ip') or (inputText[11] != '--rack' and inputText[11] != '-rack')):
        print(inputText)
        print("Incorrect arguments for config")
        logging.error("Incorrect arguments for config")
        return False

    return True

def validateServerCreate(inputText):
    if inputText == '':
        logging.error('Invalid create command')
        return False

    if (len(inputText) != 8):
        print("Incomplete command")
        logging.error("Incomplete command")
        return False

    if ((inputText[3] != "--image") or (inputText[5] != "--flavor")):
        print(inputText)
        print("Incorrect arguments for config")
        logging.error("Incorrect arguments for config")
        return False

    return True

def main():
    printAvailableCommands()
    logging.basicConfig(filename='aggiestack.log', format='%(asctime)s %(levelname)-8s %(message)s',level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Starting Logging ...')

    stackData = StackData()

    while True:
        user_input = input("aggieshell>")
        logging.info(user_input)
        inputText = user_input.split()
        if user_input == '':
            continue
        if validateCommand(inputText):
            if inputText[0] == "quit":
                logging.info('SUCCESS')
                logging.info('Validation Finished ...')
                break;
        
            if inputText[1] == "config":
            # aggiestack config --hardware hdwr-config.txt    
                if inputText[2] == "--hardware": 
                    stackData.config("hardware",inputText[3])
                elif inputText[2] == "--flavors": 
                    stackData.config("flavor",inputText[3])
                elif inputText[2] == "--images":
                    stackData.config("image",inputText[3])

            if inputText[2] == "create":
                if validateServerCreate(inputText):
                    stackData.createInstance(inputText[7], inputText[4], inputText[6])

            if len(inputText) == 3 and inputText[1] == "server" and inputText[2] == "list":
                stackData.show("server list")

            if len(inputText) == 4 and inputText[1] == "admin" and inputText[3] == "instances":
                stackData.show("server instance")

            if len(inputText) == 4 and inputText[1] == "server" and inputText[2] == "delete":
                stackData.deleteInstance(inputText[3])

            # type aggiestack show hardware
            elif inputText[1] == "show": 
                if inputText[2] == "hardware": 
                    stackData.show("hardware")
                elif inputText[2] == "flavors": 
                    stackData.show("flavor")
                elif inputText[2] =="images":
                    stackData.show("images")
                elif inputText[2] == "all": 
                    stackData.showAll()

            elif inputText[1] == "admin":
                if inputText[2] == "show" and inputText[3] == "hardware":
                    stackData.adminShowAvailableHardware()
                elif inputText[2] == "show" and inputText[3] == "imagecaches":
                    stackData.adminShowCachedImagesOnRack(inputText[4])
                elif inputText[2] == "can_host":
                    status = stackData.canHost(inputText[3], inputText[4])
                    if status == True:
                        print("Yes\n")
                    else:
                        print("No\n")
                elif inputText[2] == "remove":
                    stackData.remove(inputText[3])
                elif inputText[2] == "add":
                    if validateAddMachine(inputText):
                        stackData.addMachine(inputText[4], inputText[6], inputText[8], inputText[10], inputText[12], inputText[13])
                elif inputText[2] == "evacuate":
                    stackData.evacuateRack(inputText[3])
                logging.info('SUCCESS')
        else:
            print('Incorrect Command\n')
            printAvailableCommands()

if __name__ == "__main__":
    main()
