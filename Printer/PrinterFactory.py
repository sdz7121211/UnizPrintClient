#coding:utf8

'''
Created on 2014-1-17

@author: sdz
'''

import time
import os
from PyQt4 import QtCore
import thread
from PyQt4 import Qt
import PyQt4

import Image
from util import File_U
from Manager import DirectoryManager
from Manager import PortConfiguration

from Agent import Agent

import ConnectPort

from Factory import Singleton

import Queue


class PrinterFactory(Singleton.Singleton, QtCore.QObject): #单件
    

    def __init__(self, filepath):
        
        self.filepath = filepath
        
        pass
    
    def getPrinter(self, parent = None):
        
        return Printer(self.filepath, parent)
           
    
class Printer(QtCore.QThread, QtCore.QObject):
    
    QUEUEMAXSIZE = 10  
    SLEEPTIME = 5
    
#    uploadStartSingal = QtCore.pyqtSignal(int)
    searchPortSignal = QtCore.pyqtSignal(str)
    closePrinterSignal = QtCore.pyqtSignal()
    
    def __init__(self, filepath, parent = None):
        
        super(Printer, self).__init__()
        self.qu = Queue.Queue(maxsize = self.QUEUEMAXSIZE)
        self.com_dr = 'com2'
        self.BANDRATE = 115200
        
        self.parent_ = parent
        
        if self.parent_:
            self.setParent(parent)
            
        self.agent = Agent.Agent()
#        self.printerConnect = None
        self.dorectory = filepath
        self.end_flag = True
        
        self.writeCom = ThreadWriteCOM(self.qu, None)
        
        self.stopFlag = False
        
        
        
    def stop(self):
        self.writeCom.stop()
        self.stopFlag = True
        
        
    def run(self):
        self.initCom()
        printerConnect = ConnectPort.ConnectPort(self.com_dr, self.BANDRATE)
        if printerConnect.isUniz():
            self.ser = ConnectPort.Port(self.com_dr, self.BANDRATE).open()
            self.writeCom.setPort(self.ser)
            self.printModel(self.dorectory)
        else:
            printerConnect = ConnectPort.ConnectPort()
            printerConnect.tryOpenPort.connect(self.tryOpenPortAction, 1)
            printerPort = printerConnect.getUnizPort()
            if printerPort:
                PortConfiguration.PortWriteToConf(printerPort)
                
#                print "printerPort", printerPort
                self.ser = ConnectPort.Port(printerPort, 115200).open()
                if self.ser:
                    self.writeCom.setPort(self.ser)
#                    print "self.ser", self.dorectory
                    self.printModel(self.dorectory)
                    
    @PyQt4.QtCore.pyqtSlot(str)             
    def tryOpenPortAction(self, processContent):
        
        self.searchPortSignal.emit(processContent)
        
    def initCom(self):
        f = QtCore.QFile()
        f.setFileName(DirectoryManager.CONF_PORT_FILE_PATH)
        if f.exists():
            if f.open(QtCore.QIODevice.ReadOnly):
                i = 0
                for item in file(DirectoryManager.CONF_PORT_FILE_PATH).readlines():
                    try:
                        if i == 0:
                            self.com_dr = str(item).split()[1]
                        if i == 1:
                            self.BANDRATE = int(str(item).split()[1])
                        i += 1
                    except:
                            pass
                        
        print "initCom", self.com_dr, self.BANDRATE
        
       


    def printModel(self, dorectory):
        
    
    
        modelName = str(dorectory).split("/")[-1]
        idx_location = dorectory + "/" + modelName + ".idx"
        
    
        # ==================================== 索引文件  =================================
    
        idx = open(idx_location,'r')
        head = idx.readline()
        if '*** NVP Index file ***' in head:
            prefix     = idx.readline().split()
            ext        = idx.readline().split()
            num_start  = idx.readline().split()        
            num_end    = idx.readline().split()
            base_start = idx.readline().split()
            dirname    = os.path.dirname(idx_location)
            prefixname = prefix[1]
            extname    = ext[1]
            ini_startname  = num_start[1]
            endname    = num_end[1]
            base_startname = base_start[1]
            Model_Start = int(ini_startname)
            Model_End   = int(endname)
            ini_base_start = int(base_startname)
        idx.close()
        # ==================================== 索引读取 完毕 =================================
#        print "Model_Start", int(ini_startname)
#        print "Model_End", int(endname)
        time.sleep(1)
        time.sleep(1)
        time.sleep(1)
        self.ser.write('s')                               
        time.sleep(0.8)

        self.writeCom.setMaxProcess((Model_End + 1) - 2000)
        
        self.writeCom.setParent(self)
        self.writeCom.start()
        if self.writeCom.isRunning():
            self.writeCom.setPriority(QtCore.QThread.HighestPriority)
        
        OK_stemp = []
        
        for photo_count in range(Model_Start, Model_End + 1 ):  #分层循环
            
            del OK_stemp[:]
    
            if_start_fill = False
            image_st = dorectory + "\\" + modelName + str(photo_count)+'.png'
            
            processing_image = Image.open(image_st)         #文件位置
            black_image = processing_image.convert("1")
            
            s = black_image.getdata()
            i = 0
            for re_line in range(0, black_image.size[1]): # 行
            
                if i%2 == 0:
                    re_row = 0 
                    while re_row < black_image.size[0]: # 列
                        if (s[re_line * black_image.size[0] + re_row] == 255): # 起始边界
                            
                            if if_start_fill == False:
                                if_start_fill = True
                                start_str_hex = self._hex_16_bit(re_line)
                                OK_stemp.append(start_str_hex)
                                                   
                            x1 = re_row
                            while (s[re_line * black_image.size[0] + re_row] == 255 ): # 结束边界
                                re_row += 1
                                if re_row == black_image.size[0]:
                                    break
                                
                            x2 = re_row - 1                        
                            
                                
                            str_hex = self._HEX_Result(x1, x2)
                            if self.qu.qsize() == self.QUEUEMAXSIZE:
                                time.sleep(self.SLEEPTIME)
                            OK_stemp.append(str_hex)
                            re_row += 1 
                        else:
                            re_row += 1
                            
                          
                if i%2 == 1:
                    re_row = black_image.size[0] - 1
                    while re_row >= 0: # 列
                        if (s[re_line * black_image.size[0] + re_row] == 255): # 起始边界    
                                         
                            if if_start_fill == False:
                                if_start_fill = True
                                start_str_hex = self._hex_16_bit(re_line)
                                OK_stemp.append(start_str_hex)
                                                                                    
                            x1 = re_row
                            while (s[re_line * black_image.size[0] + re_row] == 255 ): # 结束边界
                                re_row -= 1
                                if re_row == -1:                            
                                    break
                                
                            x2 = re_row + 1   
                                                 
                            str_hex = self._HEX_Result(x1, x2)
                            if self.qu.qsize() == self.QUEUEMAXSIZE:
                                if self.stopFlag:
                                    return
                                time.sleep(self.SLEEPTIME) 
                            OK_stemp.append(str_hex)                       
                            re_row -= 1 
                        else:
                            re_row -= 1                
                i += 1
                if if_start_fill == True:
                    OK_stemp.append('555555')            
    
            OK_stemp.append('666666')
            self.cut_last(OK_stemp)
    
            for item in OK_stemp:
                
                self.qu.put(item, 1)                
                    
        self.qu.put("777777", 1)   



    def cut_last(self, ls):
    
        i = 0
    
        ls.reverse()
        if len(ls) > 1:
            for item in ls[1:]:
                if item != "555555":
                    pass
                    break
                i += 1            
            del ls[1:i]
        ls.reverse()
        
        time.sleep(10)
        
       
        
    def _HEX_Result(self, x1,x2): # 24  bit
    
        hex_x1 = ''
        hex_x2 = ''
        for i in range (0,3 - len(hex(x1)[2:])):
            hex_x1 += '0'
        for i in range (0,3 - len(hex(x2)[2:])):
            hex_x2 += '0'
        hex_result = hex_x1 + hex(x1)[2:] + hex_x2 + hex(x2)[2:]
    
        return  hex_result
        
    def _hex_16_bit(self, num): # 16 bit    
        
        if num >= 16:  
            head = hex(int(num)>>8)[2:]
            tail = hex(num)[-2:]
            sss = head + tail
            for i in range(0, 4 - len(sss)):
                sss = "0" + sss
            return sss
        else:
            sss = hex(num)[2:]
            for i in range(0, 4 - len(hex(num)[2:])):
                sss = "0" + sss
            return sss
        
class ThreadWriteCOM(QtCore.QThread, QtCore.QObject):     
    
    uploadProcessSingal = QtCore.pyqtSignal(int,int)
    
    finished = QtCore.pyqtSignal()
    
    def __init__(self, queue, ser):
        super(ThreadWriteCOM, self).__init__()
        
        self.qu = queue
        self.ser = ser
        
        self.stopFlag = False
        
    def setPort(self, port):
        self.ser = port
        
    def setMaxProcess(self, maxv):
        self.maxv = maxv
        
    def stop(self):
        self.stopFlag = True
        
    def run(self):
        process = 0
        while not self.stopFlag:      
            processing_hex = self.qu.get(1)
            if processing_hex != "777777":
#                print "not777777", processing_hex
                if processing_hex == "666666":
                    process += 1                   
                    self.uploadProcessSingal.emit(process, self.maxv)
                    time.sleep(10)
                self._send_cmd(processing_hex)
            else:
                self.stopFlag = True
                
            self.ser.close()
            
            if not self.stopFlag:
            
                self.finished.emit()
                
                
                
       
    def _send_cmd(self, processing_hex):
    
#        print "_send_cmd"
        flag = False   
        rev = self.ser.read(1)  
    
        while rev == "U":
            flag = True    
            rev = self.ser.read(1)
        if flag == True:
            rev = self.ser.read(1)
          
        if rev == 's':
#            print "memory is full"
            print self.ser.read(1) # b
            print self.ser.read(1) # o
            
        self.ser.write(processing_hex.decode("hex"))
        
        
def searchPortSignalAccept(content):
    print "aaaaaaaaaaaaaaaaaaaaa", content

if __name__ == "__main__":
    
    from PyQt4 import QtGui
    import sys
    
    app = QtGui.QApplication(sys.argv)

    printer = PrinterFactory(File_U.convertPathSlish(r"C:\Users\sdz\workspaceJavaEE\3DPrinterN\output\sample")).getPrinter()
#    printer = Printer(File_U.convertPathSlish(r"C:\Users\sdz\workspaceJavaEE\3DPrinterN\output\sample"))
    printer.searchPortSignal.connect(searchPortSignalAccept)
#    printer.writeCom.uploadProcessSingal.connect(searchPortSignalAccept)
    printer.start()
    
    
    time.sleep(50)
    print "EEEEEEEEEEEEEEEEEE",printer.qu.qsize()
    printer.exec_()
    printer.exit()
    app.exec_()
    
#    printer.searchPortSignal.connect(searchPortSignalAccept)
#    a = PrinterFactory()
#    b = PrinterFactory()
#    print "a == b", a == b
    
        