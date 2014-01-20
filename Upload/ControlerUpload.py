'''
Created on 2014-1-16

@author: sdz
'''
from util import File_U
from PyQt4 import QtCore

#from Printer import PrinterFactory
#
#from Manager import DirectoryManager
#
#from Agent import Agent

#import time

#import threading

class ControlerUpload(QtCore.QThread, QtCore.QObject):
    
    
#    finishDecompress = QtCore.pyqtSignal()
    


    def __init__(self, zipfilename, parent = None):
        '''
        Constructor
        '''
        super(ControlerUpload, self).__init__(parent)
        
        self.zipfilename = File_U._fromUtf8(zipfilename) # has extention name
        
        
#        wareHouse = DirectoryManager.getModelPath(File_U.excludeExtentionName(zipfilename))
#        self.agent = Agent.Agent()
#       
#        self.printer = PrinterFactory.PrinterFactory(wareHouse).getPrinter()
        
        
    def run(self):
        
        
        
        self.unpackThread = File_U.DeCompress7z(File_U.getCurrentUpDirPath() + "/temp/" + self.zipfilename, observer = self.observer)
#        self.unpackThread.correctFinished.connect(self.uploadStart) 
        self.unpackThread.unpack7zCommand()
#        unpackThread
#        time.sleep(200)

    def setObserver(self, observer):
        self.observer = observer

    def uploadStart(self):
        
        pass
        
#        print "wareHouse", wareHouse
        
        
#        self.printer.start()
#        import time
#        print "ssssssssssssssstop"
#        time.sleep(100)        
#        self.agent.noticeToReceiver(self.printer.searchPortSignal, self.searchPortAction)
#        self.agent.noticeToReceiver(self.printer.writeCom.uploadProcessSingal, self.uploadProcessAction)
#        
#        self.printer.wait()

    def searchPortAction(self, info):
        
        self.parent().ui.textEdit.append(info)    
        
    def uploadProcessAction(self, pro, maxv):
        
        self.parent().ui.progressBar.setMaximum(int(maxv))
        self.parent().ui.progressBar.setValue(int(pro))

        

#class DecompressThread(File_U.DeCompress7z, QtCore.QThread):
#        
#    
#    def __init__(self, filepath, outpath = None, observer = None):
#        
#        super(DecompressThread, self).__init__(filepath, outpath, observer)
#        self.exitStatus = -1 
#        
##        self.initDecompressThreadConnect()
#        
#    def run(self):
#        
#        self.unpack7zCommand()
        
    
#    def initDecompressThreadConnect(self):
#        
#        self.correctFinished.connect(self.correctFinishedAction)
    
#    def correctFinishedAction(self):
#        self.exitStatus = 1     #correct finished
        
    
    
        