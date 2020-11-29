# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerlFLHGN.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setFixedSize(632, 451)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet(u"border-color: rgb(226, 226, 226);\n"
"background-color: rgb(231, 231, 231);")
        self.messageHistoryBox = QPlainTextEdit(Form)
        self.messageHistoryBox.setObjectName(u"messageHistoryBox")
        self.messageHistoryBox.setGeometry(QRect(10, 30, 611, 331))
        self.messageHistoryBox.setStyleSheet(u"background-color: rgb(255, 255, 255);color: rgb(0, 0, 0);")
        self.messageHistoryBox.setReadOnly(True)
        self.messageInputBox = QPlainTextEdit(Form)
        self.messageInputBox.setObjectName(u"messageInputBox")
        self.messageInputBox.setGeometry(QRect(10, 390, 521, 51))
        self.messageInputBox.setStyleSheet(u"background-color: rgb(255, 255, 255);color: rgb(0, 0, 0);")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 121, 16))
        self.label.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 370, 121, 16))
        self.label_2.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.sendButton = QPushButton(Form)
        self.sendButton.setObjectName(u"sendButton")
        self.sendButton.setGeometry(QRect(540, 390, 81, 51))
        self.sendButton.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def updateMessageHistoryBox(self, msg):
        self.messageHistoryBox.appendPlainText(f"[Me] {msg}")
    def clearMessageBox(self):
        self.messageInputBox.setPlainText("")

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"LAN Chatting Client", None))
        self.label.setText(QCoreApplication.translate("Form", u"Message history", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Message content", None))
        self.sendButton.setText(QCoreApplication.translate("Form", u"Send", None))
    # retranslateUi


