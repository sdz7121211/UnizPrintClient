#coding:utf8
'''
Created on 2014-1-14

@author: sdz
'''

from PyQt4 import QtGui
import DownloadListDialogUI
import PyQt4
from UI import PrintDialog

debug = True

class DownloadListDialog(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(DownloadListDialog, self).__init__(parent)
        
        self._loadUI()
        self.setFixedSize(self.size())
        self._initAction()
        self.ui.tableWidget.setFocus()
        
        self.selectContent = None
        self.initTableWidget()
        
        self.ui.pushButton.setEnabled(False)
#        self.setRowCount(3)
#        self.fillTableWidget(["ssss", "mmm", "dddd"])
        
        
        
    def initTableWidget(self):
#        self.ui.tableWidget.setRangeSelected(QtGui.QTableWidgetSelectionRange(0,0,2,2), True)
#        self.ui.tableWidget.setFocus()
        self.ui.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
#        self.ui.tableWidget.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
    
    def _loadUI(self):
        
        self.ui = DownloadListDialogUI.Ui_Form()
        self.ui.setupUi(self)
        
    def _initAction(self):
        self.ui.pushButton.clicked.connect(self.clickPrintButtonAction)
        self.ui.tableWidget.itemClicked[QtGui.QTableWidgetItem].connect(self.clickTableWidgetAction)
        
    def clickTableWidgetAction(self, item):# type(item) QTableWidgetItem
        
        if not self.ui.pushButton.isEnabled():
            self.ui.pushButton.setEnabled(True)
        self.selectContent = item.text() # return QString
        
        if debug:
            print "click TableWidget", self.selectContent
            
    def setRowCount(self, num):
        self.ui.tableWidget.setRowCount(num)
            
    @PyQt4.QtCore.pyqtSlot(QtGui.QTableWidgetItem)
    def clickPrintButtonAction(self):
        if debug:
            print "click Print Button", self.selectContent
            
        printDialog = PrintDialog.PrintDialog(self.parent())
        printDialog.setSlectedItem(self.selectContent)
        printDialog.show()
        self.close()
            
#            print item.text()
#            # return QTableWidgetItem
#            print len(self.ui.tableWidget.selectedItems())
#            for item in self.ui.tableWidget.selectedItems():
#                print item.row()
                
    def fillTableWidget(self, lis):
#        self.setRowCount(len(lis))
        row = 0
        col = 0
        fileindex = []
        for item1 in lis:
            if str(item1).endswith(".7z"):
                fileindex.append(item1)
                row += 1
        self.setRowCount(row)
        for idx in range(len(fileindex)):
            self.ui.tableWidget.setItem(idx, col, QtGui.QTableWidgetItem(fileindex[idx]))       
            
                
        self.setRowCount(row)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
    tested = DownloadListDialog()
    tested.show()
    
    app.exec_()       