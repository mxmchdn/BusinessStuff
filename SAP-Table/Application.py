#!/usr/bin/python

#Author: maxime.chardon, Stage EPITA SPE





#------------------------------------INSTALLATION AND IMPORT PART-----------------------------------

import subprocess

# Process to test import or install and import
def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
        print(package + ' is already installed')
    except ImportError:
        import pip
        install(package)
        print(package + ' is install')
    finally:
        globals()[package] = importlib.import_module(package)

def install(name):
    subprocess.call(['pip', 'install', '--trusted-host', 'files.pythonhosted.org', '--trusted-host', 'pypi.org', '--trusted-host', 'pypi.python.org', name, '-vvv'])

# Modules to install
install_and_import('requests') # Get part (retire from net)
install_and_import('xlwt') # Exel part (save)
install_and_import('PyQt5') # GUI part

import sys, os
# For excel
from xlwt import Workbook
import requests
from Rappatriement_Longueur import *
# for GUI
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

#------------------------------------INSTALLATION AND IMPORT PART-----------------------------------





#---------------------------------------------GUI PART----------------------------------------------

# Argument 1: the path for scan a directory <str>
Directory_Path = ''
# Argument 2: the splitter in filename <str>
Name_Splitter = ''
# Argument 3: the position of the name in filename <int>
Name_Position = 3
# Argument 4: the splitter in the file <str>
File_Splitter = ''
# Argument 5: if you want unicode (True = *2, False = *1) <bool>
Is_Unicode = False
# Argument 6: the type (extension) of file to scan (.txt or .csv) <str>
File_Type = ''
# Argument 7: the default value if length equal to zero <int>
Default_Value = 10

#---------------------------------------------GUI PART----------------------------------------------





#---------------------------------------------GUI PART----------------------------------------------

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 640
        self.top = 480
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.list = []
        self.getDirectory()
        self.getNameSplitter()
        self.getIntPosition()
        self.getFileSplitter()
        self.getIsUnicode()
        self.getFileType()
        self.getDefaultValue()

        file = open("tmp", "w")
        for elt in self.list:
            file.write(str(elt) + '\n')
        file.close()
        self.show()

    def getDirectory(self):
        path = QFileDialog.getExistingDirectory(self, 'Select the directory')
        if path != '':
            self.list.append(path)
        else:
            raise Exception('You stop the program, cause: you cancel the selection of a directory!')

    def getNameSplitter(self):
        splitter, isOK = QInputDialog.getText(self, "What is your name splitter?", "Name splitter:")
        if isOK and splitter != '':
            if splitter[0] > '0' and splitter[0] <'9':
                 splitter = ord(int(splitter))
            self.list.append(splitter)
        else:
            raise Exception('You stop the program, cause: you cancel the selection of the name splitter!')

    def getIntPosition(self):
        x, isOK = QInputDialog.getInt(self, "What the name position?", "Name position:")
        if isOK:
            self.list.append(x)
        else:
            raise Exception('You stop the program, cause: you cancel the selection of the name position!')

    def getFileSplitter(self):
        splitter, isOK = QInputDialog.getText(self, "What is your file splitter?", "File splitter (int / char / copy-paste):")
        if isOK and splitter != '':
            if splitter[0] > '0' and splitter[0] <'9':
                splitter = chr(int(splitter))
            self.list.append(splitter)
        else:
            raise Exception('You stop the program, cause: you cancel the selection of the file splitter!')

    def getIsUnicode(self):
        items = ('True', 'False')
        item, isOK = QInputDialog.getItem(self, "Choose if you want to use Unicode","Unicode:", items, 0, False)
        if isOK and item:
            self.list.append(item)
        else:
            raise Exception('You stop the program, cause: you cancel the selection of unicode descision!')

    def getFileType(self):
        ext, isOK = QInputDialog.getText(self, "What is your file type?", "File type:")
        if isOK and ext != '':
            self.list.append(ext)
        else:
            raise Exception('You stop the program, cause: you cancel the selection of the file type!')

    def getDefaultValue(self):
        x, isOK = QInputDialog.getInt(self, 'What is your default length?', "Default legth:")
        if isOK and x:
            self.list.append(x)
        else:
            raise Exception('You stop the program, cause: you cancel the selection of the default length!')

    def __repr__(self):
        return self.list

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
#---------------------------------------------GUI PART----------------------------------------------





#---------------------------------------Application PART--------------------------------------------

# Extract all data
file = open("tmp", "r")
lines = file.readlines()
Directory_Path = lines[0][0 : len(lines[0]) - 1]
Name_Splitter = lines[1][0 : len(lines[1]) - 1]
Name_Position = int(lines[2])
File_Splitter = lines[3][0 : len(lines[3]) - 1]
Is_Unicode = bool(lines[4])
File_Type = lines[5][0 : len(lines[5]) - 1]
if File_Type[0] != '.':
    File_Type = '.' + File_Type
Default_Value = int(lines[6])
file.close()
os.remove("tmp")

# Extract from file
List_Name = Scan_directory(Directory_Path, Name_Splitter, Name_Position, File_Type)
Fields_List_extract = Fields_Len_Extraction(List_Name, File_Splitter)

# Extract from web
GET_requests(List_Name)
Fields_List_GET = Fields_Len_HTML_Extractions(List_Name)

# Analyse and Save
Result = MergeTwoList(Fields_List_extract, Fields_List_GET)
SaveAll(Result, Is_Unicode, Default_Value, File_Type)
