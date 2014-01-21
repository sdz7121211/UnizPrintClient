'''
Created on 2014-1-20

@author: sdz
'''
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
from UI import mainWindow
from util_U import File_U
from Agent import Agent
from Manager import DirectoryManager

from Manager import GlobalVariable

from UI import DownloadListDialog
from UI import DownloadDialog


class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(MainWindow, self).__init__()
        self._loadUI()
        self.setCentralWidget(self.ui.webView)
        self.initToolbar()
        self.initHomePage()
        self.initWebView()
        
    
        
    def initHomePage(self):
        self.ui.webView.setUrl(QtCore.QUrl(GlobalVariable.HomePage))
        
    def initToolbar(self):
        import os
        updir = File_U.convertPathSlish(os.getcwd())
        self.toolBar = QtGui.QToolBar(self)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        
        self.homeClick = QtGui.QAction(self)
        self.homeIcon = QtGui.QIcon()
        self.homeIcon.addPixmap(QtGui.QPixmap(updir + "/icon/homepage.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.homeClick.setIcon(self.homeIcon)
        Agent.Agent().noticeToReceiver(self.homeClick.triggered, self.homeClickAction)

        self.refeshClick = QtGui.QAction(self)
        self.refeshIcon = QtGui.QIcon()
        self.refeshIcon.addPixmap(QtGui.QPixmap(updir + "/icon/refesh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refeshClick.setIcon(self.refeshIcon)
        Agent.Agent().noticeToReceiver(self.refeshClick.triggered, self.reflashClickAction)
        
        self.preClick = QtGui.QAction(self)
        self.preIcon = QtGui.QIcon()
        self.preIcon.addPixmap(QtGui.QPixmap(updir + "/icon/forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.preClick.setIcon(self.preIcon)       
        Agent.Agent().noticeToReceiver(self.preClick.triggered, self.preClickAction)
        
        self.backClick = QtGui.QAction(self)
        self.backIcon = QtGui.QIcon()
        self.backIcon.addPixmap(QtGui.QPixmap(updir + "/icon/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backClick.setIcon(self.backIcon)       
        Agent.Agent().noticeToReceiver(self.backClick.triggered, self.backClickAction)

        self.downloadListClick = QtGui.QAction(self)
        self.downloadListIcon = QtGui.QIcon()
        self.downloadListIcon.addPixmap(QtGui.QPixmap(updir + "/icon/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadListClick.setIcon(self.downloadListIcon)       
        Agent.Agent().noticeToReceiver(self.downloadListClick.triggered, self.downloadListClickAction)
        
        
        self.toolBar.addAction(self.homeClick)
        self.toolBar.addAction(self.refeshClick)
        self.toolBar.addAction(self.preClick)
        self.toolBar.addAction(self.backClick)
        self.toolBar.addAction(self.downloadListClick)
        
    
    def initWebView(self):
        self.ui.webView.linkClicked.connect(self.clickLinkAction)
        self.ui.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        
    
    def clickLinkAction(self, qurl):
        
        url = File_U._fromUtf8(qurl.toString() )
        if str(url).endswith(".7z"):
            dd = DownloadDialog.DownloadDialog(self)
            dd.ui.label_url.setText(url)
            dd.show()
        else:
            self.ui.webView.setUrl(qurl)
        
    
        
    def _loadUI(self):
        
        self.ui = mainWindow.Ui_mainWindow()         
        self.ui.setupUi(self)
                
    def homeClickAction(self):
        self.ui.webView.setUrl(QtCore.QUrl(GlobalVariable.HomePage))
    
    def reflashClickAction(self):
        self.ui.webView.reload()
    
    def preClickAction(self):
        self.ui.webView.forward()
        
    def backClickAction(self):
        self.ui.webView.back()
    
    def downloadListClickAction(self):
        modelList = File_U.getAllFile(DirectoryManager.getDownloadFilePath())
        dl = DownloadListDialog.DownloadListDialog(self)
        dl.fillTableWidget(modelList)
        dl.show()
        
        
    

    
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    tested = MainWindow()
    tested.show()
    app.exec_()