#coding:utf8
'''
Created on 2014-1-13

@author: sdz
'''

from PyQt4 import QtCore

from UI import mainWindow

from util import File_U
import StartRequest


isdebug = False

class DownloadURL:
    '''
    classdocs
    '''


    def __init__(self, source, destination = None):
        '''
        Constructor
        '''
        
        self.source = File_U._fromUtf8(source)
        
        self.source_info = QtCore.QFileInfo(mainWindow._fromUtf8(source))
        
        self.file_name =  self.source_info.fileName()
        
        self.destination = File_U.getCurrentUpDirPath() + "/temp/" + self.file_name
    
    
    def getDestination(self):
        return self.destination
    
    
#    def sourceIsValid(self):
#        return str(self.file_name).endswith(".7z")
#        
#    def save(self):
#        self.startRequest()
#    
#    def startRequest(self):
#        if isdebug == True:
#            print "self.source, self.destination", self.source, self.destination
#        request = StartRequest.StartRequest(self.source, self.destination)
#        request.run()
    
    

        
        
        
        
if __name__ == "__main__":
    from PyQt4 import QtGui
    import sys
    app = QtGui.QApplication(sys.argv)
    tested = DownloadURL("http://www.uniz.cc/modelview/content/EiffelTower.7z")
    tested.save()
#    print tested.destination
#    print tested.sourceIsValid()
    app.exec_()
        