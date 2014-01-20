'''
Created on 2013-12-13

@author: sdz
'''
import os
from PyQt4 import QtCore
import DirectoryManager

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s



def PortWriteToConf(port):
    
    confPort_path = DirectoryManager.CONF_PORT_FILE_PATH
    f = None    
    try:
        f = open(confPort_path, "r")
    except:
#        print "ERROR:Read config file error"
        return None
    
    li = ["port " + port]
    for line in f.readlines():
        print line
        if "port" in str(line):
            continue
        li.append(line)
    f.close()
    f = open(confPort_path, "w")
    for item in li:
        if not str(item).endswith("\n"):
            f.write(item + "\n")
        else:
            f.write(item)
    f.close()
    return True