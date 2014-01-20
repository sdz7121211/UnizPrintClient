'''
Created on 2014-1-12

@author: sdz
'''

from PyQt4 import QtGui
import sys
from WebClient import WebBrowerse

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)    
    main = WebBrowerse.MainWindow()
    main.show()    
    app.exec_()