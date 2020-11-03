# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindows.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class mainwindows_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("*{\n"
" background-color:white;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cheeseButton = QtWidgets.QGroupBox(self.centralwidget)
        self.cheeseButton.setGeometry(QtCore.QRect(220, 150, 351, 111))
        self.cheeseButton.setTitle("")
        self.cheeseButton.setObjectName("cheeseButton")
        self.label = QtWidgets.QLabel(self.cheeseButton)
        self.label.setGeometry(QtCore.QRect(20, 20, 71, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("assets/mouse_intro_icon2.jpg"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.cheeseButton)
        self.label_2.setGeometry(QtCore.QRect(120, 30, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:#ed4b15;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.raceButton = QtWidgets.QGroupBox(self.centralwidget)
        self.raceButton.setGeometry(QtCore.QRect(220, 330, 351, 111))
        self.raceButton.setTitle("")
        self.raceButton.setObjectName("raceButton")
        self.label_3 = QtWidgets.QLabel(self.raceButton)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 71, 71))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("assets/mouse_intro_icon2.jpg"))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.raceButton)
        self.label_4.setGeometry(QtCore.QRect(110, 30, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:#ed4b15;")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main Window"))
        self.label_2.setText(_translate("MainWindow", "Get the Cheese"))
        self.label_4.setText(_translate("MainWindow", "drive without wheel"))


