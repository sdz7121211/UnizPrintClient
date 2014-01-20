'''
Created on 2014-1-18

@author: sdz
'''
from PyQt4 import QtGui

from util import File_U

class MessageBoxSample(QtGui.QMessageBox):
    '''
    classdocs
    '''


    def __init__(self, parent, title, content):
        if parent:
            super(MessageBoxSample, self).__init__(parent)
        else:
            super(MessageBoxSample, self).__init__()
        
        self.setWindowTitle(File_U._fromUtf8(title))
        
        self.setText(File_U._fromUtf8(content))
        
        self.addButton(QtGui.QMessageBox.Yes)
        
        self.addButton(QtGui.QMessageBox.No)
        
        self.setDefaultButton(QtGui.QMessageBox.No)


if __name__ == "__main__":
    p = QtGui.QWidget()
    MessageBoxSample(None, "sssss","ssssssssssss").show()