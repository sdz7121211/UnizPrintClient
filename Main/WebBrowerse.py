# 2014.01.20 23:20:45 中国标准时间
#Embedded file name: WebClient\WebBrowerse.pyc
"""
Created on 2014-1-12

@author: sdz
"""
from PyQt4 import QtGui
from UI import mainWindow
from PyQt4 import QtCore
import PyQt4
from PyQt4 import QtWebKit
from UI import DownloadDialog
from UI import DownloadListDialog
from util import File_U
import sys
import sip

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self._loadUI()
        self.setCentralWidget(self.ui.webView)
        self.ui.webView.load(QtCore.QUrl(mainWindow._fromUtf8('http://www.uniz.cc/modelview/')))
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap('../icon/main_big.png')))
        self.setWindowTitle(mainWindow._fromUtf8('Uniz Software - Model View'))
        self.setStatusBar(QtGui.QStatusBar(self))
        self.statusBar().showMessage(mainWindow._fromUtf8('Uniz Software - Model View'))
        self._initToolbar()
        self._connectWebViewLinkClicked()
        sip.setdestroyonexit(False)

    def _loadUI(self):
        self.ui = mainWindow.Ui_mainWindow()
        self.ui.setupUi(self)

    def _initToolbar(self):
        self.toolbar = QtGui.QToolBar(self)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.homepageActionItem = self._initToobarItem('../icon/homepage.png')
        self.forwardActionItem = self._initToobarItem('../icon/forward.png')
        self.backActionItem = self._initToobarItem('../icon/back.png')
        self.refeshActionItem = self._initToobarItem('../icon/download.png')
        self.downloadActionItem = self._initToobarItem('../icon/download.png')
        self.connect(self.homepageActionItem, QtCore.SIGNAL(mainWindow._fromUtf8('triggered()')), self.homepageClickAction)
        self.connect(self.forwardActionItem, QtCore.SIGNAL(mainWindow._fromUtf8('triggered()')), self.forwardClickAction)
        self.connect(self.backActionItem, QtCore.SIGNAL(mainWindow._fromUtf8('triggered()')), self.backClickAction)
        self.connect(self.refeshActionItem, QtCore.SIGNAL(mainWindow._fromUtf8('triggered()')), self.refeshClickAction)
        self.connect(self.downloadActionItem, QtCore.SIGNAL(mainWindow._fromUtf8('triggered()')), self.downloadListClickAction)
        self.toolbar.addAction(self.homepageActionItem)
        self.toolbar.addAction(self.forwardActionItem)
        self.toolbar.addAction(self.backActionItem)
        self.toolbar.addAction(self.refeshActionItem)
        self.toolbar.addAction(self.downloadActionItem)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)

    def _connectWebViewLinkClicked(self):
        self.ui.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        QtCore.QObject.connect(self.ui.webView, QtCore.SIGNAL(mainWindow._fromUtf8('linkClicked(QUrl)')), self.clickUrlAction)

    def homepageClickAction(self):
        self.ui.webView.setUrl(QtCore.QUrl(mainWindow._fromUtf8('http://www.uniz.cc/modelview/')))

    def forwardClickAction(self):
        self.ui.webView.forward()

    def backClickAction(self):
        self.ui.webView.back()

    def refeshClickAction(self):
        self.ui.webView.reload()

    def downloadListClickAction(self):
        filelist = File_U.getAllFile(File_U.getCurrentUpDirPath() + '/temp')
        downloadlistDialog = DownloadListDialog.DownloadListDialog(self)
        downloadlistDialog.fillTableWidget(filelist)
        downloadlistDialog.show()

    @PyQt4.QtCore.pyqtSlot(QtCore.QUrl)
    def clickUrlAction(self, url):
        url_str = File_U._fromUtf8(url.toString())
        if not str(url_str).endswith('.7z'):
            self.ui.webView.setUrl(url)
        else:
            dd = DownloadDialog.DownloadDialog(self)
            dd.show()
            dd.ui.label_url.setText(url.toString())

    def _initToobarItem(self, img_path):
        item_action = QtGui.QAction(self)
        item_icon = QtGui.QIcon()
        item_icon.addPixmap(QtGui.QPixmap(img_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_action.setIcon(item_icon)
        return item_action

    def closeEvent(self, closeEvent):
        self.close()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()
