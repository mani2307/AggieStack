 # Implemention of AggieStack CLI
 Aggistack CLI reads the command from the standard input and generates the expected output in the standard output. Command for running the code is as follows:

    cd P0
    python3 aggiestack.py 
 
 After running this command, you will get a list of valid commands which you can execute on the terminal:
 
       ========== Aggiestack I Valid commands: ==========

      1) aggiestack config --hardware hdwr-config.txt
      2) aggiestack config --images image-config.txt
      3) aggiestack config --flavors flavor-config.txt
      4) aggiestack show hardware
      5) aggiestack show images
      6) aggiestack show flavors
      7) aggiestack show all
      8) aggiestack admin show hardware
      9) aggiestack admin can_host [machine name] [flavor]
      aggieshell>

After this, you can execute commands as given below:

  **1) Configure the hardware**
  
      aggieshell>aggiestack config --hardware hdwr-config.txt
      aggieshell>aggiestack show hardware
      
      +--------+-------------+-----+-----------+-----------+
      |  Name  |     IP      | MEM | Num-Disks | Num-vcpus |
      +========+=============+=====+===========+===========+
      | m1     | 128.0.0.1   | 16  | 8         | 4         |
      +--------+-------------+-----+-----------+-----------+
      | m2     | 128.0.0.2   | 16  | 32        | 4         |
      +--------+-------------+-----+-----------+-----------+
      | m3     | 128.0.0.3   | 16  | 16        | 4         |
      +--------+-------------+-----+-----------+-----------+
      | m4     | 128.0.0.4   | 16  | 8         | 4         |
      +--------+-------------+-----+-----------+-----------+
      | k1     | 128.1.1.0.  | 32  | 32        | 8         |
      +--------+-------------+-----+-----------+-----------+
      | k2     | 128.1.0.2.  | 32  | 32        | 8         |
      +--------+-------------+-----+-----------+-----------+
      | k3     | 128.1.3.0.  | 32  | 32        | 8         |
      +--------+-------------+-----+-----------+-----------+
      | calvin | 128.129.4.4 | 8   | 16        | 1         |
      +--------+-------------+-----+-----------+-----------+
      | hobbes | 1.1.1.1     | 16  | 64        | 16        |
      +--------+-------------+-----+-----------+-----------+
      | dora   | 1.1.1.2     | 64  | 256       | 16        |
      +--------+-------------+-----+-----------+-----------+
      aggieshell>

  **2) Configure the flavors**
  
      aggieshell> aggiestack config --flavors flavor-config.txt
      aggieshell>aggiestack show flavors
      
      +--------+-----------+-----------+-----------+
      |  Name  | RAM-in-GB | Num-Disks | Num-vcpus |
      +========+===========+===========+===========+
      | small  | 1         | 1         | 1         |
      +--------+-----------+-----------+-----------+
      | medium | 8         | 2         | 4         |
      +--------+-----------+-----------+-----------+
      | large  | 16        | 2         | 4         |
      +--------+-----------+-----------+-----------+
      | xlarge | 32        | 4         | 8         |
      +--------+-----------+-----------+-----------+
      aggieshell>
   
   **Similarly, we can configure the images as well.**
   **3) Display all data**
   
       aggieshell>aggiestack show all
       
      +--------+-------------+-----+-----------+-----------+
      |  Name  |     IP      | MEM | Num-Disks | Num-vcpus |
      +========+=============+=====+===========+===========+
      | m1     | 128.0.0.1   | 16  | 8         | 4         |
      +--------+-------------+-----+-----------+-----------+
      | m2     | 128.0.0.2   | 16  | 32        | 4         |
      +--------+-------------+-----+-----------+-----------+
      | m3     | 128.0.0.3   | 16  | 16        | 4         |
      +--------+-------------+-----+-----------+-----------+
      | m4     | 128.0.0.4   | 16  | 8         | 4         |
      +--------+-------------+-----+-----------+-----------+
      | k1     | 128.1.1.0.  | 32  | 32        | 8         |
      +--------+-------------+-----+-----------+-----------+
      | k2     | 128.1.0.2.  | 32  | 32        | 8         |
      +--------+-------------+-----+-----------+-----------+
      | k3     | 128.1.3.0.  | 32  | 32        | 8         |
      +--------+-------------+-----+-----------+-----------+
      | calvin | 128.129.4.4 | 8   | 16        | 1         |
      +--------+-------------+-----+-----------+-----------+
      | hobbes | 1.1.1.1     | 16  | 64        | 16        |
      +--------+-------------+-----+-----------+-----------+
      | dora   | 1.1.1.2     | 64  | 256       | 16        |
      +--------+-------------+-----+-----------+-----------+
      
      +--------+-----------+-----------+-----------+
      |  Name  | RAM-in-GB | Num-Disks | Num-vcpus |
      +========+===========+===========+===========+
      | small  | 1         | 1         | 1         |
      +--------+-----------+-----------+-----------+
      | medium | 8         | 2         | 4         |
      +--------+-----------+-----------+-----------+
      | large  | 16        | 2         | 4         |
      +--------+-----------+-----------+-----------+
      | xlarge | 32        | 4         | 8         |
      +--------+-----------+-----------+-----------+
      
       No images data found
      aggieshell>
  **4) One can also execute admin commands as follow:**
  
      aggieshell>aggiestack admin show hardware
      +--------+-------------+-----+-----------+-----------+
      |  Name  |     IP      | MEM | Num-Disks | Num-vcpus |
      +========+=============+=====+===========+===========+
      | m1     | 128.0.0.1   | 16  | 8         | 4         |
      +--------+-------------+-----+-----------+-----------+
      | m2     | 128.0.0.2   | 16  | 32        | 4         |
      +--------+-------------+-----+-----------+-----------+
      | m3     | 128.0.0.3   | 16  | 16        | 4         |
      +--------+-------------+-----+-----------+-----------+
      | m4     | 128.0.0.4   | 16  | 8         | 4         |
      +--------+-------------+-----+-----------+-----------+
      | k1     | 128.1.1.0.  | 32  | 32        | 8         |
      +--------+-------------+-----+-----------+-----------+
      | k2     | 128.1.0.2.  | 32  | 32        | 8         |
      +--------+-------------+-----+-----------+-----------+
      | k3     | 128.1.3.0.  | 32  | 32        | 8         |
      +--------+-------------+-----+-----------+-----------+
      | calvin | 128.129.4.4 | 8   | 16        | 1         |
      +--------+-------------+-----+-----------+-----------+
      | hobbes | 1.1.1.1     | 16  | 64        | 16        |
      +--------+-------------+-----+-----------+-----------+
      | dora   | 1.1.1.2     | 64  | 256       | 16        |
      +--------+-------------+-----+-----------+-----------+
      aggieshell>aggiestack admin can_host m1 small
      Yes

      aggieshell>aggiestack admin can_host m1 xlarge
      No

      aggieshell>  
  **5) Once you are done with all configuration, you can quit using quit command**
  
      aggieshell>quit
      C:\Users\spans\Documents\Github\678-18-c\P0>

**Once the program is closed, we need to reconfigure harware, images, and flavors.**
**We also have handled negative testcases and an appropriate message will be displayed on the terminal.**

# Requirements:
**1) Texttable**

      Installation command: pip3 install texttable

# Reference
1) https://stackoverflow.com/questions/36423259/how-to-use-pretty-table-in-python-to-print-out-data-from-multiple-lists
2) https://docs.python.org/2/library/logging.html
3) https://stackoverflow.com/questions/577234/python-extend-for-a-dictionary
