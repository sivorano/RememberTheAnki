#!/usr/bin/env python3

import sys

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
import RememberTheAnki
import RememberTheAnki as rta


def test_HandleInput():
    assert(RememberTheAnki.HandleInput([]) == 0)
    assert(RememberTheAnki.HandleInput(["ThisShouldGive0"]) == 0)

def test_MainLoop():
    rta.HandleInput(["startup"])
    rta.WriteToDaemon(rta.MESSAGE_TYPES["deamon close"])
    time.sleep(3)

def test_WriterAndReader():
    textToWrite = "Hej med\n dig"
    RememberTheAnki.WriteToDaemon(textToWrite)
    out1 = RememberTheAnki.ReadLineFromFile(RememberTheAnki.SUB_INPUT_FILE)
    out2 = RememberTheAnki.ReadLineFromFile(RememberTheAnki.SUB_INPUT_FILE)
    assert(out1 == "Hej med")
    assert(out2 == " dig")
    errorVal = False
    try:
        RememberTheAnki.ReadLineFromFile(RememberTheAnki.SUB_INPUT_FILE)
    except:
        errorVal = True
    assert(errorVal == True)

    
