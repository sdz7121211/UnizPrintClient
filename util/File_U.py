#coding:utf8
'''
Created on 2013-12-19

@author: sdz
'''
#from PyQt4 import QtCore
import py7zlib
import sys
#import PyQt4

#import zipfile
from PyQt4 import QtCore
#import PyQt4

import os

debug = True

reload(sys)
sys.setdefaultencoding("utf-8")

try:
    def _fromUtf8(s):
        _FU = QtCore.QString.fromUtf8
        return str(_FU(s).toUtf8()).decode()    
except:
    def _fromUtf8(s):
        return s

def excludeExtentionName(filename):
    filename = _fromUtf8(filename)
    lis = str(filename).split(".")
    if len(lis) == 1:
        return filename
    result = None
    if len(lis) == 2:
        return str(lis[0])    
    else:
        for item in lis[:-1]:
            result += item
            
        return result
         
    


def convertPathSlish(filepath):
    fp = _fromUtf8(filepath)

    dr = QtCore.QDir(filepath)

    return "/".join(_fromUtf8(fp).split("\\"))

def getUpDirPath(filepath):
    filepath = convertPathSlish(filepath)
    dr = QtCore.QDir(filepath)
    dr.cdUp()
    return _fromUtf8(dr.absolutePath())
    
def getCurrentUpDirPath():
    CWD = _fromUtf8(os.getcwd())
#    print "CWD", CWD
    result = getUpDirPath(CWD)
    return result


def pathExist(filepath):
    return QtCore.QFile.exists(filepath)

def getAllFile(path, filter_ = None):
    dir_ = QtCore.QDir(path)
#    if filter_:
#        
#
#        dir_.setFilter(filter_)
        
    return list(dir_.entryList(sort = QtCore.QDir.Time))

def cleardir(filepath):
    filepath = _fromUtf8(filepath)
        
    if os.path.isdir(filepath):
        for root, dirs, files in os.walk(filepath, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(filepath)
    return True
        
    


def rmfile_beta(filepath):
    qbasedir = QtCore.QDir(_fromUtf8(filepath))
    if qbasedir.exists():
        filelist = getAllFile(filepath)
        for item in filelist:
            qbasedir.remove(_fromUtf8(item))
#            print item
        qbasedir.rmdir(_fromUtf8(filepath))
    
    

def unpack7z(filepath):
    
    fp = open(filepath, 'rb')
    archive = py7zlib.Archive7z(fp)
#    n = len(archive.getnames())
    for name in archive.getnames():
        outfilename = os.path.join(filepath, name)
        outdir = os.path.dirname(outfilename)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        outfile = open(outfilename, 'wb')
        outfile.write(archive.getmember(name).read())
        outfile.close()
        
def unpackzip(filepath):
    pass




class DeCompress7z(QtCore.QObject):

    correctFinished = QtCore.pyqtSignal()
    incorrectFinished = QtCore.pyqtSignal()    
    
    def __init__(self, filepath, outpath = None, observer = None):
        
        super(DeCompress7z, self).__init__()
        
        self.observer = observer
        
        self.act = QtCore.QProcess()
        
        self.program = getCurrentUpDirPath() + "/tool/7za.exe" 
        
        self.outpath = outpath
        
        if not self.outpath:
            self.outpath = str(str(filepath).split(".")[0])
        
        self.arvgList = ["e", _fromUtf8(filepath), "-o" + _fromUtf8(self.outpath)]
       
#        self.initConnect()

        
    
    def initConnect(self):
        self.act.finished.connect(self.deCompressFinishAction) #[QtCore.QProcess.ExitStatus]
        self.act.readyRead.connect(self.deCompressReadyReadStandardOutputAction)
        


    def unpack7zCommand(self):
        
        rmfile_beta(self.outpath)
        self.act.setProcessChannelMode(QtCore.QProcess.SeparateChannels)
        self.act.setReadChannel(QtCore.QProcess.StandardOutput)
#        os.chdir(os.getcwd())
        
        self.act.start(self.program, self.arvgList)
        self.initConnect()
#        self.initConnect()
        
        
#        self.act.waitForStarted()
#        self.act.waitForFinished()
    
#    @PyQt4.QtCore.pyqtSlot(QtCore.QProcess.ExitStatus) 
    def deCompressFinishAction(self, exitStatus):
        if debug:
            print "after finish act.state()", self.act.state()
            
        if self.act.exitStatus() == 0:
            self.correctFinished.emit()
        elif self.act.exitStatus() == 1:
            self.incorrectFinished.emit()
        else:
            self.incorrectFinished.emit()
            
    
    
    def deCompressReadyReadStandardOutputAction(self):
#        print self.act.readAll()
#        if debug:
#            print int(self.act.state())
#            print "ready read sdz", QtCore.QString(self.act.readAllStandardOutput())
        
        if self.observer:
            self.observer.inform(QtCore.QString(self.act.readAllStandardOutput()))
            



#def mkdir_(path):
#    print "mkdir_", _fromUtf8(path)
#    os.mkdir(_fromUtf8(path))
    
    
                    
                    
if __name__ == "__main__":
    
    #test rmfile_beta
    
#    rmfile_beta(convertPathSlish(r"C:\Users\sdz\workspaceJavaEE\WebClient\temp\EiffelTower"))
    
    # test DeCompress7z

    tested = DeCompress7z(convertPathSlish(r"C:\Users\sdz\workspaceJavaEE\WebClient\temp\EiffelTower.7z"))
    tested.unpack7zCommand()
#    print convertPathSlish(_fromUtf8(r"C:\水水水水撒\刷刷刷\workspaceJavaEE\3DPrinterN"))
#    getUpDirPath(_fromUtf8(r"C:\Users\sdz\workspaceJavaEE\3DPrinterN"))
#    print getCurrentUpDirPath()
#    print QtCore.QFile.exists(getCurrentUpDirPath()+"/output/EiffelTower/EiffelTower1980.png")


    # test getAllFile
#    print len(getAllFile(getCurrentUpDirPath()))
#    for item in getAllFile(getCurrentUpDirPath()):
#         
#        print item

    # test unpack7z
#    unpack7z("C:/Users/sdz/Desktop/EiffelTower.7z")

    
    pass