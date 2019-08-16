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
import platform
import hashlib

#Constants


BUFFER_SIZE = 1024

#The files from which the deamon will take its input and write its output
LOCAL_COPY = "RTA_COL_COPY.anki2"
LOCAL_COPY_ROOT = "RTA_COL_COPY"
#TEST_DECKNAMES = ["日本語::My true immersion deck"]
TEST_DECKNAMES = "日本語"
TEST_FILETOCHECK = "/home/anders/.local/share/Anki2/User 1/collection.anki2"
WINDOWS_CLOSE_WIFI_COMMAND = "netsh interface set interface Wi-Fi disable"
WINDOWS_OPEN_WIFI_COMMAND = "netsh interface set interface Wi-Fi enable"



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


def ReadCollectionCounts(path,deckName):
    col = Collection(path)
    deckIds = {}
    for key, value in col.decks.decks.items():
        #print("Deck id -> " + value["name"])
        if value["name"] == deckName or value["name"].startswith(deckName): #::
            deckIds[value["name"]] = value["id"]
            print(value["name"])
    for value in deckIds.values():
        ()        
	#print(value)
    stat = col.stats()
    counts = 0
    cardsRes = []
    for name,deckId in deckIds.items():
        cardsRes = stat.col.db.all(
            """
            SELECT :today,due,* FROM cards 
            WHERE due < :today 
            AND did = :id
            AND reps != 0
            AND queue >= 0
            """ % (), today = stat.col.sched.today, id = deckId)
        #stat.col.db.all(""" PRAGMA table_info(cards);""")
        print("%s - %s" % (len(cardsRes),name))
        counts = len(cardsRes) + counts
    return counts



def CheckFiles(fileToCheck,deckNames,memory = {}):
    """
    comment
    """
    hashOfCol = hashCalculator(fileToCheck)
    if hashOfCol in memory:
        print("Hash was in memory")
        return (memory[hashOfCol],memory)
    else:
        #We remove any exess files
        print("Hash was not in memory")

        if os.path.exists(LOCAL_COPY_ROOT + ".media"):
            rmtree(LOCAL_COPY_ROOT + ".media")
        for filename in glob.glob(LOCAL_COPY_ROOT + '*') :
            os.remove(filename)

        #We create a local copy
        copyfile(fileToCheck,LOCAL_COPY)
        
        counts = ReadCollectionCounts(LOCAL_COPY,deckNames)
        memory[hashOfCol] = counts
        return (counts,memory)

def IsOnWIFI():
    ()

def CloseWIFI():

    if platform.system() == "Linux":
        print("LINUX: turning wifi off")
        os.system("/usr/bin/dbus-launch --exit-with-session /usr/bin/nmcli network off")
        #print("please implement wifi checker for linux")
    else:
        print("WINDOWS: turning wifi off")
        os.system(WINDOWS_CLOSE_WIFI_COMMAND)

def EnableWIFI():
    if platform.system() == "Linux":
        print("LINUX: turning wifi on")
        os.system("/usr/bin/dbus-launch --exit-with-session /usr/bin/nmcli network on")
        #print("please implement wifi checker for linux")
    else:
        print("WINDOWS: turning wifi on")
        os.system(WINDOWS_OPEN_WIFI_COMMAND)
        
def FileCheckerLoop(fileToCheck,deckNames,limit = 0,SleepTime = 3600):

    memory = {}
    counts,nmemory = CheckFiles(fileToCheck,deckNames,memory)
    memory = nmemory
    if counts > limit:
        CloseWIFI()
    else:
        EnableWIFI()
    
    while True:
        time.sleep(SleepTime)

        counts, nmemory  = CheckFiles(fileToCheck,deckNames,memory)
        memory = nmemory
        if counts > limit:
            print("counts: %s" % counts)
            CloseWIFI()
        else:
            EnableWIFI()



FileCheckerLoop(fileToCheck = TEST_FILETOCHECK, deckNames = TEST_DECKNAMES,limit = 0 ,SleepTime = 600)
#ReadCollectionCounts(TEST_FILETOCHECK,TEST_DECKNAMES)
