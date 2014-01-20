'''
Created on 2014-1-13

@author: sdz
'''

#import threadng

from UI import mainWindow

import PyQt4

from PyQt4 import QtNetwork
from PyQt4 import QtCore

from PyQt4 import QtGui

from util import File_U


import time


isdebug = False


class StartRequest:
    '''
    classdocs
    '''
    


    def __init__(self, url, tofile = None):
        
        
        self.url = QtCore.QUrl(url)
        
        self.tofile_path = mainWindow._fromUtf8(tofile)
        
        self.tofile_info = QtCore.QFileInfo(self.tofile_path)
        
        self.tofile_basename = self.tofile_info.baseName()
        
        self.tofile = QtCore.QFile(mainWindow._fromUtf8(tofile))
        
        self.initFile()
        
        self.isSuccess = False
        
#        self.main.setNetworkAccessible(QtNetwork.QNetworkAccessManager().Accessible)
        
    def initFile(self):
        self.touch_()
        self.tofile.open(QtCore.QIODevice.WriteOnly)
        
    def touch_(self):
        if self.tofile.exists():
            self.tofile.remove()

               
    def creatRequest(self):
        req = QtNetwork.QNetworkRequest(self.url)  
        req.setRawHeader("User-agent", "Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20100101 Firefox/12.0")
        return req
#    @staticmethod 
   
    def run(self):
        
#        if self.isSuccess == False:
        
        self.main = QtNetwork.QNetworkAccessManager()
        if isdebug:
            print "networkAccessible", self.main.networkAccessible()
        self.content = self.main.get(QtNetwork.QNetworkRequest(self.creatRequest())) #type(content) is QNetworkReply
        if isdebug:
            print "BufferSize", self.content.readBufferSize()
        self.content.setReadBufferSize(4096)
        if isdebug:
            print "BufferSize", self.content.readBufferSize()
            print "error", self.content.error()
            
#        print "is running", self.content.readBufferSize()
        
        QtCore.QObject.connect(self.content, QtCore.SIGNAL(mainWindow._fromUtf8("readyRead()")), self.httpReadyRead)
        QtCore.QObject.connect(self.content, QtCore.SIGNAL(mainWindow._fromUtf8("finished()")), self.httpFinished)
#        print self.content.downloadProgress
        self.content.downloadProgress.connect(self.updateDataReadProgress)
#        QtCore.QObject.connect(self.content, QtCore.SIGNAL(mainWindow._fromUtf8("downloadProgress(int,int)")), self.updateDataReadProgress)
            
        
                               
    def httpFinished(self):
            
        
        if self.isSuccess == False:
            del self.content
            self.run()
        else:
            self.tofile.flush()
            self.tofile.close()     
        
        if isdebug:
            print "httpFinished"
        
    
    def httpReadyRead(self):
        
        self.isSuccess = True
        self.tofile.write(self.content.readAll())
        
        
    
    @PyQt4.QtCore.pyqtSlot(int,int)    
    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.observer:
            self.observer.setMaximum(totalBytes)
            self.observer.setValue(bytesRead)
            
        if isdebug:
            print bytesRead, totalBytes
    
    def setObserver(self, progressBar):
        self.observer = progressBar   
        
    
    



if __name__ == "__main__":
    import sys
    import PyQt4
    app = QtGui.QApplication(sys.argv)
    tested = StartRequest(r"http://www.uniz.cc/modelview/content/EiffelTower.7z", "../temp/test.7z")
    
    tested.run()
    
    app.exec_()
        
        
        
        
        
        
        
        
        
        
    
        
        
        
        
        
        
        