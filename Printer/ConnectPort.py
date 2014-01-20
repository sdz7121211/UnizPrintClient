#coding:utf8
'''
Created on 2013-12-12

@author: sdz
'''
import serial
import time
from PyQt4 import QtCore

from util import File_U

global init_port
init_port = "com2"

global rate
rate = 115200


class ConnectPort(QtCore.QObject):
    
    tryOpenPort = QtCore.pyqtSignal(str)
    
    canOpenPrinterPort = QtCore.pyqtSignal(str)
    
    canNotOpenPrinterPort = QtCore.pyqtSignal(str)
    
    global init_port
    global rate

    def __init__(self, port = init_port, rate = rate):
        '''
        Constructor
        '''
        super(ConnectPort, self).__init__()
        self.prt = None
        if ConnectPort.canOpen(port, rate):
            self.prt = Port(port, rate).open()
        else:
            return None
    
    
    def isUniz(self):     
        
        if self.prt:
            time.sleep(0.1)
            u = self.prt.read(1)
    
            if u == "U":
                self.prt.close() 
                return True
            
            self.prt.close()    
            return False
    
    def getUnizPort(self):
        for i in range(1,256):
            time.sleep(0.4)
            po = "com" + str(i)
            self.tryOpenPort.emit(File_U._fromUtf8("正在扫描打印机端口" + po))
            ok = ConnectPort(po)
            if ok.prt:
                if ok.isUniz():
                    ok.closePort()
                    return po
                ok.closePort()            
        return None
    
    def closePort(self):
        if self.prt:
            self.prt.close()
            
            
            
    
    @staticmethod
    def canOpen(port, rate = rate):
        ser = None
        try:
            ser = serial.Serial(port, rate)
        except:
            return False
        
        ser.close()
        return True
    
class Port():
    
    def __init__(self, port, rate):
        
        self.port = port
        self.rate = rate
        
    def open(self):
        
        try:
            ser = serial.Serial(self.port, self.rate, timeout = 0.1)
            return ser
        except:
            return False



            
#    d = time.time()
#    print d-s
#    print li
if __name__ == "__main__":
    
    def accept(content):
        print content
    tested = ConnectPort()
    tested.tryOpenPort.connect(accept)
    print tested.getUnizPort()
    
            
