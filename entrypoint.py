#!/usr/bin/env python3

# This script launch two types of threads :
# The first scan a directory with filename like job:[0-9]*:process, extract the number in the filename,
# ass it in a queue and delete the file
# The second retrieve a number from the previous queue, execute a batch script with the number as argument.
# If the script does not return 0, it try 3 times.

import sys
import glob, os
import re
from subprocess import Popen, PIPE
import argparse, sys

import queue
import threading
import time

# script is the script to run
# folder is the folder whre files are found
script = "./script.sh"
folder = os.environ['JOB_LAUNCHER_DIRECTORY']


#flag to stop script
exitFlag = 0

#processing number queue
queueLock = threading.Lock()
workQueue = queue.Queue(1000)

# Thread to look in folder, extract in folder files looking file job:[0-9]*:process and put in into queue
class look_for_numbers(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("Start thread " + str(self.threadID))
        while not exitFlag:
            for filename in glob.glob(folder + "/job:[0-9]*:process"):
                filename_match = re.search('job:([0-9]*):process', filename, re.IGNORECASE)
                if filename_match:
                    print("[" + str(self.threadID) + "]New file found : " + filename_match.group(0))
                    os.remove(filename)
                    queueLock.acquire()
                    workQueue.put(filename_match.group(1))
                    queueLock.release()
            time.sleep(5)

# Thread to take a number from queue and run script with it
# If script fails try 3 more time
class exec_script(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("Start thread " + str(self.threadID))
        while not exitFlag:
          queueLock.acquire()
          if not workQueue.empty():
             number = workQueue.get()
             queueLock.release()
             p = Popen([script,number], stdin=PIPE, stdout=PIPE, stderr=PIPE)
             output, err = p.communicate(b"input data that is passed to subprocess' stdin")
             rc =  p.returncode
             if rc != 0:
                 print("[" + str(self.threadID) + "] [WARN] Number " +  number +" unprocessed")
                 for i in range(3):
                     p = Popen([script,number], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                     output, err = p.communicate(b"input data that is passed to subprocess' stdin")
                     rc =  p.returncode
                     if(rc==0):
                         print("[" + str(self.threadID) + "] Number " +  number +" processed")
                         break
                 print("[" + str(self.threadID) + "] [ERR] Number " +  number +" unprocessed")
             else:
                 print("[" + str(self.threadID) + "] Number " +  number +" processed")
          else:
             queueLock.release()
             time.sleep(10)


# Run script
# Start one thread + 3

print('Starting')

thread_look_for_numbers = look_for_numbers(1, "Look for numbers")
thread_exec_script1 = exec_script(2, "Exec script 1")
thread_exec_script2 = exec_script(3, "Exec script 2")
thread_exec_script3 = exec_script(4, "Exec script 3")

thread_look_for_numbers.start()
thread_exec_script1.start()
thread_exec_script2.start()
thread_exec_script3.start()

thread_look_for_numbers.join()
thread_exec_script1.join()
thread_exec_script2.join()
thread_exec_script3.join()


print('Ending')
