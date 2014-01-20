# -*- coding: utf-8 -*-
#@author sdz
from PyQt4 import QtCore


global com_dr, BANDRATE
com_dr = 'com2'
BANDRATE = 115200

import Image
import time
import os
import serial 
import sys
from multiprocessing import Value
from PyQt4 import QtCore

from util import File_U

import Queue

import thread


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


CWD = str(_fromUtf8(os.getcwd()).toUtf8()).decode()
CWD_OUT = str(_fromUtf8(CWD + "\\output").toUtf8()).decode()



global print_dialog_active
#print_dialog_active = Value("b", 0)

global ana_image_sleep_time
ana_image_sleep_time = 5

global MAXSIZE
MAXSIZE = 18000

global qu 
qu = Queue.Queue(maxsize = MAXSIZE)

global end_flag
end_flag = False

global progrssBar_value

global progressBar_min_value

global progressBar_max_value



def initCom():
    global com_dr, BANDRATE
    f = QtCore.QFile()
    f.setFileName("./sys/confPort.txt")
    
    if f.exists():
        if f.open(QtCore.QIODevice.ReadOnly):
            i = 0
            for item in file("./sys/confPort.txt").readlines():
                try:
                    if i == 0:
                        com_dr = str(item).split()[1]
                    if i == 1:
                        BANDRATE = int(str(item).split()[1])
                    i += 1
                except:
                    print "acquiesce port: com2, Bandrate: 115200"
                    com_dr = 'com2'
                    BANDRATE = 115200

global ser
ser = None
def PrintModelWraper(slicesFilePath, modelName, *shareData):
    print "PrintModelWraper start"
    PrintModel(slicesFilePath, modelName, shareData) 
    
    
def PrintModel(slicesFilePath, modelName):
    global ser
    global com_dr, BANDRATE
    global qu 
    global MAXSIZE
    global end_flag
    

    initCom()
    if slicesFilePath:
        pass
    else:   
        slicesFilePath = CWD_OUT
        
    modelName = str(_fromUtf8(modelName).toUtf8()).decode() 
    idx_location = slicesFilePath + "\\" + str(modelName).split(".")[0] + "\\" + str(modelName).split(".")[0] + ".idx"    
    ser = serial.Serial(com_dr, BANDRATE) 
    

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
    # ==================================== 索引读取 完毕 =================================
    
    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    ser.write('s')                               
    time.sleep(0.8)

    
    thread.start_new_thread(thread_write_COM, ())
    
    OK_stemp = []
    
    for photo_count in range(Model_Start, Model_End + 1 ):  #分层循环
        
        del OK_stemp[:]

        if_start_fill = False
        image_st = slicesFilePath + "\\" + str(modelName).split(".")[0] + "\\" + str(modelName).split(".")[0] + str(photo_count)+'.png'
        
        processing_image = Image.open(image_st)         #文件位置
        black_image = processing_image.convert("1")
        
        print File_U._fromUtf8("总体进度:" + str(photo_count/Model_End))
        s = black_image.getdata()
        i = 0
        for re_line in range(0, black_image.size[1]): # 行
        
            start_line_flag = False
            if i%2 == 0:
                re_row = 0 
                while re_row < black_image.size[0]: # 列
                    if (s[re_line * black_image.size[0] + re_row] == 255): # 起始边界
                        
                        if if_start_fill == False:
                            if_start_fill = True
                            start_str_hex = _hex_16_bit(re_line)
                            OK_stemp.append(start_str_hex)
                                               
                        x1 = re_row
                        while (s[re_line * black_image.size[0] + re_row] == 255 ): # 结束边界
                            re_row += 1
                            if re_row == black_image.size[0]:
                                break
                            
                        x2 = re_row - 1                        
                        
                            
                        str_hex = _HEX_Result(x1, x2)
                        if qu.qsize() == MAXSIZE:
                            time.sleep(ana_image_sleep_time)
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
#                            start_line_flag = True
                            start_str_hex = _hex_16_bit(re_line)
                            OK_stemp.append(start_str_hex)
#                            qu.put(str_hex, 1)
                                                                                
                        x1 = re_row
                        while (s[re_line * black_image.size[0] + re_row] == 255 ): # 结束边界
                            re_row -= 1
                            if re_row == -1:                            
                                break
                            
                        x2 = re_row + 1   
                                             
                        str_hex = _HEX_Result(x1, x2)
                        if qu.qsize() == MAXSIZE:
                            time.sleep(ana_image_sleep_time) 
                        OK_stemp.append(str_hex)                       
#                        qu.put(str_hex, 1)
                        re_row -= 1 
                    else:
                        re_row -= 1                
            i += 1
            if if_start_fill == True:
                OK_stemp.append('555555')            

        OK_stemp.append('666666')
        cut_last(OK_stemp)

        for item in OK_stemp:
            
            qu.put(item, 1)                
                
    qu.put("777777", 1)   
    end_flag = True

cut_num = 0 
def cut_last(ls):

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

              
def _HEX_Result(x1,x2): # 24  bit

    hex_x1 = ''
    hex_x2 = ''
    for i in range (0,3 - len(hex(x1)[2:])):
        hex_x1 += '0'
    for i in range (0,3 - len(hex(x2)[2:])):
        hex_x2 += '0'
    hex_result = hex_x1 + hex(x1)[2:] + hex_x2 + hex(x2)[2:]

    return  hex_result





def _hex_16_bit(num): # 16 bit


    
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
    
    
    
    
    
def _send_cmd(processing_hex):
    global ser


    flag = False   
    rev = ser.read(1)  

    while rev == "U":
        flag = True    
        rev = ser.read(1)
    if flag == True:
        rev = ser.read(1)
      
    if rev == 's':
        print "memory is full"
        print ser.read(1) # b
        print ser.read(1) # o
        
    ser.write(processing_hex.decode("hex"))

def thread_write_COM():    
    global qu
    global ser
              
    while True:      
        if not end_flag:
            processing_hex = qu.get(1)
            if processing_hex == "666666":
                pass
            _send_cmd(processing_hex)
        else:
            if qu.empty():
                ser.close()
                break
            else:
                processing_hex = qu.get(1)
                _send_cmd(processing_hex)

            
    
if __name__ == "__main__":
    initCom()