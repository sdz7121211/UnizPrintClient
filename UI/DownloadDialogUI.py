# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PrintDialog.ui'
#
# Created: Mon Jan 13 19:30:08 2014
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_WidgetClass(object):
    def setupUi(self, WidgetClass):
        WidgetClass.setObjectName(_fromUtf8("WidgetClass"))
        WidgetClass.resize(493, 112)
        self.layoutWidget = QtGui.QWidget(WidgetClass)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 30, 431, 68))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.pushButton = QtGui.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_url = QtGui.QLabel(self.layoutWidget)
        self.label_url.setObjectName(_fromUtf8("label_url"))
        self.verticalLayout.addWidget(self.label_url)
        self.progressBar = QtGui.QProgressBar(self.layoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(WidgetClass)
        QtCore.QMetaObject.connectSlotsByName(WidgetClass)

    def retranslateUi(self, WidgetClass):
        WidgetClass.setWindowTitle(_translate("WidgetClass", "Download", None))
        self.label.setText(_translate("WidgetClass", "URL地址：", None))
        self.pushButton.setText(_translate("WidgetClass", "下载", None))
        self.label_url.setText(_translate("WidgetClass", "TextLabel", None))

#import widget_rc
