from stackdata import StackData	

import sys
import logging
import os.path

def printAvailableCommands():
    print ("========== Aggiestack I Valid commands: ==========\n")
    print ("1) aggiestack config --hardware hdwr-config.txt")
    print ("2) aggiestack config --images image-config.txt")
    print ("3) aggiestack config --flavors flavor-config.txt")
    print ("4) aggiestack show hardware")
    print ("5) aggiestack show images")
    print ("6) aggiestack show flavors")
    print ("7) aggiestack show all")
    print ("8) aggiestack admin show hardware")
    print ("9) aggiestack admin can_host [machine name] [flavor]")

def validateCommand(inputCommand):
    if inputCommand=='':
        logging.error('FAILURE')
        return False

    validInputs=set(["quit",
        "aggiestack config --hardware",
        "aggiestack config --images",
        "aggiestack config --flavors",
        "aggiestack show hardware",
        "aggiestack show images",
        "aggiestack show flavors",
        "aggiestack show all",
        "aggiestack admin show hardware",
        "aggiestack admin can_host"])

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
    if fullCommand not in validInputs:
        logging.error('FAILURE')
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
                elif inputText[2] == "can_host":
                    status = stackData.canHost(inputText[3], inputText[4])
                    if status == True:
                        print("Yes\n")
                    else:
                        print("No\n")
                logging.info('SUCCESS')
        else:
            print('Incorrect Command\n')
            printAvailableCommands()

if __name__ == "__main__":
    main()
