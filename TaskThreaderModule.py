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

    
def loop(data):
    try:
        r = range(0, len(data))
        for x in r:
            print "Initializing process " + str(x)
            locals()['loop%s' % x] = Thread(target=data[x])
        print "Initializing finished."

        for x in r:
            print "Running process " + str(x)
            locals()['loop%s' % x].start()

        print "Preparing to wait for functions." 
        for x in r:
            locals()['loop%s' % x].join()

        print "Success!!"
        return True
    except:
        PrintException()
