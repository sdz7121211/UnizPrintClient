#coding:utf8
'''
Created on 2014-1-16

@author: sdz
'''
from PyQt4 import QtGui
import PrintDialogUI
from util import File_U
from Upload import ControlerUpload
from Printer import PrinterFactory
from Manager import DirectoryManager
from Agent import Agent

from UNIZGUI import MessageBoxSample



class PrintDialog(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(PrintDialog, self).__init__(parent)       
        
        self._loadUI()
              
        self.setFixedSize(self.size())
        
        self.addReceiverToTextEditWegdit()
        
        self.initConnect()
        
#        wareHouse = DirectoryManager.getModelPath(File_U.excludeExtentionName(zipfilename))
        self.agent = Agent.Agent()
       
        self.printer = None
        
        
    def setSlectedItem(self, item):
        self.printmodelname = item
        self.work = ControlerUpload.ControlerUpload(self.printmodelname, self)
        self.work.setObserver(self.ui.textEdit)
        
#        self.unpack = File_U.DeCompress7z(File_U.getCurrentUpDirPath() + "/temp/" + self.printmodelname, observer = self.ui.textEdit)
        
        
    def _loadUI(self):
        
        self.ui = PrintDialogUI.Ui_Form()
        self.ui.setupUi(self)
        self.ui.textEdit.setEnabled(True)
        
    def initConnect(self):
        self.ui.commandLinkButton.clicked.connect(self.commandLinkButtonClickedAction)
        
        
    def commandLinkButtonClickedAction(self):
#        print "commandLinkButtonClickedAction"
        self.ui.commandLinkButton.setEnabled(False)
        self.work.run()
        self.work.unpackThread.correctFinished.connect(self.upload)
#        self.unpack.unpack7zCommand()
        
    
    def addReceiverToTextEditWegdit(self):
         
        self.ui.textEdit.inform = self.informTextEdit
#        self.ui.textEdit.inform(self,0)
        
    def informTextEdit(self, addcontent):
#        print "sss",s.ui
        self.ui.textEdit.append(addcontent)
#        pass


    def upload(self):
        
        wareHouse = DirectoryManager.getModelPath(File_U.excludeExtentionName(self.printmodelname))
        self.printer = PrinterFactory.PrinterFactory(wareHouse).getPrinter(self)
        self.printer.start()
                
        self.agent.noticeToReceiver(self.printer.searchPortSignal, self.searchPortAction)
        self.agent.noticeToReceiver(self.printer.writeCom.uploadProcessSingal, self.uploadProcessAction)
                
        
    def searchPortAction(self, info):
        
        self.ui.textEdit.append(info)    
        
    def uploadProcessAction(self, pro, maxv):
        self.ui.progressBar.setMaximum(int(maxv))
        self.ui.progressBar.setValue(int(pro))
        
    def closeEvent(self, closeEvent):

        if self.printer:
            if self.printer.isRunning():
                ask = MessageBoxSample.MessageBoxSample(self, File_U._fromUtf8("警告"), File_U._fromUtf8("您是否要结束此次打印任务？"))
                if ask.exec_() == QtGui.QMessageBox.Yes:
                    self.printer.stop()                
                else:
                    closeEvent.ignore()
            
            
        
        
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
    tested = PrintDialog()
    tested.addReceiverToTextEditWegdit()
    tested.setSlectedItem("EiffelTower.7z")
    tested.show()
    
    app.exec_()
    import time
    time.sleep(10000)