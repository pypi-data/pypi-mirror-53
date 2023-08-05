#!/usr/bin/env python3

import os
from platform import system
import sys


class getfile:
    """ Getfile class is used to store important files that keeps crypt ninja running. If any of those file are lost or deleted cryptninja will not able to recover the data. """
    #logging.info('loading the getfilename class')
    def __init__(self):
        pass


    def getpath(self):
        #logging.info('calling the getpath function')
        if system() == "Windows":
            #logging.info('checked system is windows. will now join the path')
            actpath = os.path.join(os.path.expanduser('~'),"AppData\\Local\\Programs\\CryptNinja")
            #logging.info('path joined. checking if directory exists')
            if os.path.isdir(actpath):
                logdir = os.path.join(actpath, 'logs')
                if os.path.isdir(logdir):
                    #logging.info('dir exists returning the path') 
                    return actpath
                else:
                    os.mkdir(logdir)
                    #logging.info('dir exists returning the path') 
                    return actpath
            else:
                #logging.info('path not found creating one')
                os.mkdir(actpath)
                logdir = os.path.join(actpath, 'logs')
                os.mkdir(logdir)
                #logging.info('returning the path')
                return actpath
        else:
            #logging.error('not a windows system. exitting')
            sys.exit('%s is not supported by cryptninja'%(system()))
