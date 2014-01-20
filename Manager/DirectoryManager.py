#coding:utf8
'''
Created on 2014-1-17

@author: sdz
'''

from util import File_U

import os

debug = False

CWD = File_U._fromUtf8(os.getcwd())

MAINPATH = File_U.getUpDirPath(CWD)

CONF_PORT_FILE_PATH = MAINPATH + "/sys/confPort.txt"


def getModelPath(modelName):
    
    return MAINPATH + "/temp/" + modelName
    

if debug:
    
    #test getModelPath
    print getModelPath("阿斯达山大")
    print "CONF_PORT_FILE_PATH", CONF_PORT_FILE_PATH