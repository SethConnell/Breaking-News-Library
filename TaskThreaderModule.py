from threading import *
import os
import time

# The 'data' argument needs to be a list with functions.
def runTasks(data):
    if type(data) is list and len(data) > 0:
        loop(data)
        return True
    else:
        return False

# Loops through data list, runs functions, then starts "finished()" when complete.
def loop(data, finished):
    try:
        r = range(0, len(data))
        for x in r:
            # Initializes processes.
            locals()['loop%s' % x] = Thread(target=data[x])

        for x in r:
            # Starts processes.
            locals()['loop%s' % x].start()

        # Waits for functions to complete. 
        for x in r:
            locals()['loop%s' % x].join()

        finished()
    except:
        PrintException()
