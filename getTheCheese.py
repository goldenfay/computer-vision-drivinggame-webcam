# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'getTheCheese.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class GetTheCheese_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 700)
        MainWindow.setStyleSheet("* {\n"
"background-color:white;\n"
"}\n"
"QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: white;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
"    stop: 0 #66e, stop: 1 #bbf);\n"
"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
"    stop: 0 #bbf, stop: 1 #55f);\n"
"border: 1px solid #777;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background: #fff;\n"
"border: 1px solid #777;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #eee, stop:1 #ccc);\n"
"border: 1px solid #777;\n"
"width: 13px;\n"
"margin-top: -2px;\n"
"margin-bottom: -2px;\n"
"border-radius: 6px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #fff, stop:1 #ddd);\n"
"border: 1px solid #444;\n"
"border-radius: 6px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 671, 401))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.gameContainer = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.gameContainer.setContentsMargins(0, 0, 0, 0)
        self.gameContainer.setObjectName("gameContainer")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 410, 671, 281))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.webCamContainer = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.webCamContainer.setContentsMargins(0, 0, 0, 0)
        self.webCamContainer.setObjectName("webCamContainer")
        self.gameSettingsGB = QtWidgets.QGroupBox(self.centralwidget)
        self.gameSettingsGB.setGeometry(QtCore.QRect(730, 40, 281, 201))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.gameSettingsGB.setFont(font)
        self.gameSettingsGB.setStyleSheet("color:#346ec9;")
        self.gameSettingsGB.setObjectName("gameSettingsGB")
        self.levelSlider = QtWidgets.QSlider(self.gameSettingsGB)
        self.levelSlider.setGeometry(QtCore.QRect(110, 40, 160, 19))
        self.levelSlider.setStyleSheet("")
        self.levelSlider.setMinimum(1)
        self.levelSlider.setMaximum(3)
        self.levelSlider.setOrientation(QtCore.Qt.Horizontal)
        self.levelSlider.setObjectName("levelSlider")
        self.label = QtWidgets.QLabel(self.gameSettingsGB)
        self.label.setGeometry(QtCore.QRect(20, 40, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.hueslider = QtWidgets.QSlider(self.gameSettingsGB)
        self.hueslider.setGeometry(QtCore.QRect(110, 80, 160, 19))
        self.hueslider.setStyleSheet("")
        self.hueslider.setMinimum(0)
        self.hueslider.setMaximum(180)
        self.hueslider.setOrientation(QtCore.Qt.Horizontal)
        self.hueslider.setObjectName("hueslider")
        self.satslider = QtWidgets.QSlider(self.gameSettingsGB)
        self.satslider.setGeometry(QtCore.QRect(110, 110, 160, 19))
        self.satslider.setStyleSheet("")
        self.satslider.setMinimum(0)
        self.satslider.setMaximum(255)
        self.satslider.setOrientation(QtCore.Qt.Horizontal)
        self.satslider.setObjectName("satslider")
        self.valueslider = QtWidgets.QSlider(self.gameSettingsGB)
        self.valueslider.setGeometry(QtCore.QRect(110, 140, 160, 19))
        self.valueslider.setStyleSheet("")
        self.valueslider.setMinimum(0)
        self.valueslider.setMaximum(255)
        self.valueslider.setOrientation(QtCore.Qt.Horizontal)
        self.valueslider.setObjectName("valueslider")
        self.label_6 = QtWidgets.QLabel(self.gameSettingsGB)
        self.label_6.setGeometry(QtCore.QRect(10, 110, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.hsv_text = QtWidgets.QLabel(self.gameSettingsGB)
        self.hsv_text.setGeometry(QtCore.QRect(60, 170, 151, 20))
        self.hsv_text.setText("")
        self.hsv_text.setObjectName("hsv_text")
        self.startGameButton = QtWidgets.QPushButton(self.centralwidget)
        self.startGameButton.setGeometry(QtCore.QRect(780, 570, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.startGameButton.setFont(font)
        self.startGameButton.setStyleSheet("background-color:#eb4034;\n"
"color:white;\n"
"")
        self.startGameButton.setObjectName("startGameButton")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(730, 250, 281, 131))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(60, 10, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:#d90707;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.won_label = QtWidgets.QLabel(self.groupBox)
        self.won_label.setGeometry(QtCore.QRect(60, 70, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.won_label.setFont(font)
        self.won_label.setStyleSheet("color:#10cc29;")
        self.won_label.setAlignment(QtCore.Qt.AlignCenter)
        self.won_label.setObjectName("won_label")
        self.scoreGB = QtWidgets.QGroupBox(self.centralwidget)
        self.scoreGB.setGeometry(QtCore.QRect(730, 410, 281, 91))
        self.scoreGB.setTitle("")
        self.scoreGB.setObjectName("scoreGB")
        self.label_3 = QtWidgets.QLabel(self.scoreGB)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:#10cc29;")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.scoreGB)
        self.label_4.setGeometry(QtCore.QRect(20, 50, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:#d90707;")
        self.label_4.setObjectName("label_4")
        self.score_label = QtWidgets.QLabel(self.scoreGB)
        self.score_label.setGeometry(QtCore.QRect(186, 12, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.score_label.setFont(font)
        self.score_label.setStyleSheet("color:#10cc29;")
        self.score_label.setText("")
        self.score_label.setObjectName("score_label")
        self.chances_label = QtWidgets.QLabel(self.scoreGB)
        self.chances_label.setGeometry(QtCore.QRect(186, 52, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.chances_label.setFont(font)
        self.chances_label.setStyleSheet("color:#d90707;")
        self.chances_label.setText("")
        self.chances_label.setObjectName("chances_label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Get The Chesse !"))
        self.gameSettingsGB.setTitle(_translate("MainWindow", "Game Settings :"))
        self.label.setText(_translate("MainWindow", "Level :"))
        self.label_6.setText(_translate("MainWindow", "Color(HSV):"))
        self.startGameButton.setText(_translate("MainWindow", "Start "))
        self.label_2.setText(_translate("MainWindow", "GAME OVER !"))
        self.won_label.setText(_translate("MainWindow", "YOU WON !"))
        self.label_3.setText(_translate("MainWindow", "Score :"))
        self.label_4.setText(_translate("MainWindow", "Remaining chances :"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
