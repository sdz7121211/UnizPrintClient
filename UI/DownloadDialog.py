#coding:utf8
'''
Created on 2014-1-13

@author: sdz
'''

from PyQt4 import QtGui
from PyQt4 import QtCore
import DownloadDialogUI

from download import StartRequest
from download import DownloadURL
from util import File_U

debug = False

class DownloadDialog(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(DownloadDialog, self).__init__(parent)
        
        self._loadUI()
        self._connectButtonClickedAction()
        
        self.ui.progressBar.setValue(0)
                
        
        if debug:
            self.ui.label_url.setText("http://www.uniz.cc/modelview/content/EiffelTower.7z")
            
    def initRequest(self):
#        source = File_U._fromUtf8(self.ui.label_url.text())
#        destination = DownloadURL.DownloadURL(source).getDestination()
#
#        self.getfile = StartRequest.StartRequest(source, destination)    
        pass 
        
    def _loadUI(self):
        

        self.ui = DownloadDialogUI.Ui_WidgetClass()
        self.ui.setupUi(self)
        
    def _connectButtonClickedAction(self):
#        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL(DownloadDialogUI._fromUtf8("clicked()")), self.buttonClickedAction)
        self.ui.pushButton.clicked.connect(self.buttonClickedAction)                      
                               
    def buttonClickedAction(self):
        if debug:
            print "click"
            
        self.ui.pushButton.setEnabled(False)
        source = File_U._fromUtf8(self.ui.label_url.text())
        destination = DownloadURL.DownloadURL(source).getDestination()

        self.getfile = StartRequest.StartRequest(source, destination)
        self.getfile.setObserver(self.ui.progressBar)  
           
        self.getfile.run()
        
    def closeEvent(self, closeEvent):
        self.ui.pushButton.clicked.disconnect(self.buttonClickedAction)
        self.close()
#        QtGui.QApplication.quit()
        
#        if debug:
#            print "source", source
#            print "destination", destination
        

        
        
        
    
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
    dd = DownloadDialog()
    dd.show()
    
    app.exec_()
    
    
        
        
        