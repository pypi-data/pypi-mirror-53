#!/usr/bin/env python3

import os
from datetime import datetime

class logger:
    """class is for moving the logging file to as separate folder. it makes logging easy to understand and keeps the logs in one place"""
    def __init__(self,filepath):
        if not filepath:
            raise ValueError('file path required')

        else:
            self.filepath = filepath


    def move(self):
        debpath = os.path.join(self.filepath, 'debug.log')
        if os.path.exists(debpath):
            tmp = datetime.now()
            now = tmp.strftime("%d_%m_%Y_%H_%M_%S")
            val = 'debug.log'
            foo = val.split('.')
            new_file = foo[0] + '_' + "%s"%now + '.' + foo[1]
            newpath = os.path.join(self.filepath, 'logs\\%s'%new_file)
            os.rename(debpath,newpath)
        else:
            pass
