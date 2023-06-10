import os
import shutil

# Clear screen
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def checkFileExsit(file):
    return os.path.isfile(file)

def checkPath(path):
    return os.path.isdir(path)

def createFolder(path):
    os.makedirs(path)

def removeFolder(path):
    shutil.rmtree(path)
