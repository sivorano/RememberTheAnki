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

#Constants


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

def WriteFromDaemon(ToWrite, brute = True):
    """
    Writes ToWrite from the Deamon to StdOut.
    """
    if brute:
        with open(SUB_OUTPUT_FILΕ,"w") as daemonOut:
            daemonOut.write(ToWrite)
    else:
        print(ToWrite,flush = True)
    return 1


def ReadLineFromFile(InFile):
    """
    Reads one line from the demons, and removes this line
    """
    with open(InFile,"r") as deamonIn:
        lines = deamonIn.readlines()
    with open(InFile, 'w') as deamonIn:
        if len(lines) > 0:
            deamonIn.writelines(lines[1:])
            return lines[0].rstrip()
        else:
            deamonIn.writelines([""])
    raise Exception("No lines to read")

def ReadLineFromDaemon(ToWrite,Trytime = 10):
    """
    """
    Read = ""
    ReadSomething = False
    def readThreadFun():
        """
        Tries to read from stdin.
        """
        temp = sys.stdin.readline()
        Read = temp
        ReadSomething = True
    
    readProcess = multiprocessing.Process(target = readThreadFun)
    readProcess.start()
    time.sleep(Trytime)
    readProcess.terminate()
    return (Read,ReadSomething)

    

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


def hashCalculator(filename):
    """
    Calculates the sha 256 hash of a file.
    Taken from https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html
    """
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
    # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        digest = sha256_hash.hexdigest()
    return digest


def ReadCollectionCounts(path,deckNames):
    col = Collection(path)
    deckIds = {}
    for key, value in col.decks.decks.items():
        if value["name"] in deckNames:
            #print(value)
            deckIds[value["name"]] = value["id"]

    stat = col.stats()
    counts = 0
    for name,deckId in deckIds.items():
        cardsRes = stat.col.db.all(
            """
            SELECT :today,due,* FROM cards 
            WHERE due < :today 
            AND did = :id
            AND reps != 0
            """ % (), today = stat.col.sched.today, id = deckId)
        #stat.col.db.all(""" PRAGMA table_info(cards);""")
    counts = len(cardsRes) + counts
    return counts



def CheckFiles(fileToCheck,deckNames,memory = {}):
    """
    comment
    """
    hashOfCol = hashCalculator(fileToCheck)
    if hashOfCol in memory:
        return (memory[hashOfCol],memory)
    else:
        #We remove any exess files
        if os.path.exists(LOCAL_COPY_ROOT + ".media"):
            rmtree(LOCAL_COPY_ROOT + ".media")
        for filename in glob.glob(LOCAL_COPY_ROOT + '*') :
            os.remove(filename)

        #We create a local copy
        copyfile(fileToCheck,LOCAL_COPY)
        
        counts = ReadCollectionCounts(LOCAL_COPY,deckNames)
        memory[hashOfCol] = counts
        return (counts,memory)

def CloseWIFI():
    print("please implement close wifi")
    
def FileCheckerLoop(StartTime,fileToCheck,deckNames,limit = 0,SleepTime = 3600):

    memory = {}
    counts,nmemory = CheckFiles(fileToCheck)
    memory = nmemory
    if counts > limit:
        CloseWIFI()
    
    while True:
        time.sleep(SleepTime)

        counts, nmemory  = CheckFiles(LOCAL_COPY,deckNames,memory)
        memory = nmemory
        if counts > limit:
            CloseWIFI()



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



