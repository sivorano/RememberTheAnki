#!/usr/bin/env python3

import sys
from anki import Collection
from shutil import copyfile,rmtree
from anki.utils import intTime
import time
import os,glob
import fileinput
import logging
#import threading
import multiprocessing 
import time
from contextlib import closing
import subprocess

import hashlib

BUFFER_SIZE = 1024

#The files from which the deamon will take its input and write its output
SUB_INPUT_FILE = "RememberTheAnkiFiles/Input"
SUB_OUTPUT_FILΕ = "RememberTheAnkiFiles/Output"
MESSAGE_TYPES = {"deamon close" :
                 """DEAMON EXIT
                 """,
                 "deamon closing" : "MESSAGE:DEAMON EXITING\n",
                 "deamon ping" : "DEAMON PING:\n",
                 "deamon pingback" : "DEAMON PINGBACK\n"}
LOCAL_COPY = "RTA_COL_COPY.anki2"
LOCAL_COPY_ROOT = "RTA_COL_COPY"
TEST_DECKNAMES = ["日本語::My true immersion deck"]


def StartCheckerDaemon(args):
    """
    Starts the background Deamon, which will do the actual work.
    """
    subprocess.Popen([sys.executable,
                      args[0],
                      "internal-startup"]#,
                     #stdin = open(SUB_INPUT_FILE,"r"),
                     #stdout = open(SUB_OUTPUT_FILΕ,"w")
    )
    
def CloseCheckerDaemon():
    """
    Closes the background daemon.
    """
    WriteToDaemon(MESSAGE_TYPES["deamon close"])


#FIXME: We want to implement better multiprocessing features using .join
def DeamonMainLoop():
    """
    Runs the main loop of the deamon checker process.    
    """
    import datetime
    #from dateutil.relativedelta import relativedelta
    START_TIME = datetime.datetime.now()
    CheckerProcess = multiprocessing.Process(target = FileCheckerLoop,args = (START_TIME,"",3600))
    CheckerProcess.daemon = True #Then it closes if this process closes.
    CheckerProcess.start()
    WriteFromDaemon("Checker started")
    
    sys.exit()
    while True:
        #logging.debug('DEAMON LOOP: reading')
        line = sys.stdin.readline().rstrip()
        #logging.debug('DEAMON LOOP: read')
        if line == MESSAGE_TYPES["deamon close"]:
            print(MESSAGE_TYPES["deamon closing"],flush = True)
            sys.exit()
            print("ERROR: Loop didn't close",flush = True)
        else:
            print("ERROR: unidentified input")
        #DeamonHandleInput(line)
        
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
        #time.sleep(3)
        print("Internal-startup worked")
        # logging.basicConfig(level=logging.DEBUG,filename = "RememberTheAnkiFiles/Log")
        # logging.debug('This will get logged')

        # logging.info("Internal-startup initialized")
        print("This is a test")
        WriteFromDaemon("This went well")
        
        with open(SUB_INPUT_FILE,"r") as my_stdin:
            ()

            #DeamonMainLoop()
        #Start the main loop
        
        logging.error("Implement Daemon")
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
    

if __name__ == "__main__":
    # We start by finding the input arguments

    InputArgs = RecieveStdInInput()
    #print(InputArgs)
    reactionCode = HandleInput(InputArgs)

    if reactionCode == 0:
        print("An error occured.")
    sys.exit()


    
