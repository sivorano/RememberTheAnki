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

BUFFER_SIZE = 1024

#The files from which the deamon will take its input and write its output
SUB_INPUT_FILΕ = "RememberTheAnkiFiles/Input"
SUB_OUTPUT_FILΕ = "RememberTheAnkiFiles/Output"


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


def StartCheckerDaemon(args):
    """
    Stats the background Deamon, which will handle 
    """
    subprocess.Popen([sys.executable,
                      args[0],
                      "internal-startup"],
                     stdin = open(SUB_INPUT_FILΕ,"r"),
                     stdout = open(SUB_OUTPUT_FILΕ,"w"))
    

def HandleInput(args):
    if len(args) <= 1:
        print ("ERROR: Program needs atleast 1 argument, eg startup")
        return 0
    elif args[1] == "startup":
        print("Runing startup")
        StartCheckerDaemon(args)
        return 1
    elif args[1] == "internal-startup":
        time.sleep(10)
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
    

if __name__ == "__main__":
    # We start by finding the input arguments

    InputArgs = RecieveStdInInput()
    print(InputArgs)
    reactionCode = HandleInput(InputArgs)

    if reactionCode == 0:
        sys.exit()
    sys.exit()



# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     time.sleep(2)
#     logging.info("Thread %s: finishing", name)

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")

#     logging.info("Main    : before creating thread")
#     x = threading.Thread(target=thread_function, args=(1,))
#     logging.info("Main    : before running thread")
#     x.start()
#     logging.info("Main    : wait for the thread to finish")
#     x.join()
#     logging.info("Main    : all done")


