#!/usr/bin/env python3

import sys
import socket
from anki import Collection
from shutil import copyfile,rmtree
from anki.utils import intTime
import time
import os,glob
import fileinput
import logging
import threading
import time
import socket
from contextlib import closing
import subprocess

#Constants


BUFFER_SIZE = 1024

#The files from which the deamon will take its input and write its output
SUB_INPUT_FILE = "RememberTheAnkiFiles/Input"
SUB_OUTPUT_FILΕ = "RememberTheAnkiFiles/Output"


#Maybe remove
def findFreePort():
    """
    returns an usnused port, see 
    https://stackoverflow.com/questions/1365265/on-localhost-how-do-i-pick-a-free-port-number
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('localhost', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]



def RecieveStdInInput():
    """
    Check if there is input from StdIn. Returns this input as an list.
    """
    args = []
    return sys.argv

def WriteToDaemon(ToWrite):
    """
    Writes ToWrite to the Deamons input file.
    """
    deamonIn = open(SUB_INPUT_FILE,"w")
    deamonIn.write(ToWrite)
    deamonIn.close()
    return 1

def ReadLinesFromDaemon():
    """
    Reads one line from the demons, and removes this line
    """
    with open(SUB_OUTPUT_FILΕ,"r") as deamonIn:
        lines = deamonIn.readlines()
    with open(SUB_OUTPUT_FILΕ, 'w') as demonIn:
        if len(lines) > 0:
            demonIn.writelines(lines[1:])
        else:
            demonIn.writelines([""])
        #FIXME: Should handle removing the line
    return lines[0]


def PingDaemon():
    """
    """
    ()

def StartCheckerDaemon(args):
    """
    Starts the background Deamon, which will do the actual work.
    """
    subprocess.Popen([sys.executable,
                      args[0],
                      "internal-startup"],
                     stdin = open(SUB_INPUT_FILΕ,"r"),
                     stdout = open(SUB_OUTPUT_FILΕ,"w"))
    
def CloseCheckerDaemon():
    """
    Closes the background daemon.
    """
    #Send to 
    ()


    
def HandleInput(args):
    """
    Handles the input, depending on 
    """
    if len(args) <= 1:
        print ("ERROR: Program needs atleast 1 argument, eg startup")
        return 0
    elif args[1] == "startup":
        print("Runing startup")
        StartCheckerDaemon(args)
        return 1
    elif args[1] == "internal-startup":
        time.sleep(10)
        #Start the main loop
        print("Internal-startup initialized")
        return 1
    elif args[1] == "close":
        return 1
    elif args[1] == "recheck":
        return 1
    elif args[1] == "isruning":
        return 1
    elif args[1] == "repeat":
        return 1
    else:
        print("Invalid input")
        return 0
    

# if __name__ == "__main__":
#     # We start by finding the input arguments

#     InputArgs = RecieveStdInInput()
#     print(InputArgs)
#     reactionCode = HandleInput(InputArgs)

#     if reactionCode == 0:
#         sys.exit()
#     sys.exit()



