
from getTheCheese import GetTheCheese_MainWindow
from webcam import *
from cheesegame import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QMouseEvent
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import threading
import cv2
import gameframe


class getTheCheese_Controller(QObject):

    def __init__(self, gui: GetTheCheese_MainWindow, window: QMainWindow = None):
        super().__init__()
        self.gui = gui
        self.mainWindow = window
        self.moveSignal = pyqtSignal()

    def setWindow(self, window: QMainWindow):
        self.mainWindow = window

    def setup(self):

        self.gui.groupBox.setVisible(False)
        self.gui.startGameButton.clicked.connect(lambda: self.start())
        self.gui.levelSlider.setSingleStep(1)
        self.gui.levelSlider.setValue(1)
        self.mainWindow.closeEvent = self.closeEvent
        self.initialiseEffects()

   

    def start(self):

        for i in reversed(range(self.gui.webCamContainer.count())):
            self.gui.webCamContainer.itemAt(i).widget().setParent(None)

        for i in reversed(range(self.gui.gameContainer.count())):
            self.gui.gameContainer.itemAt(i).widget().setParent(None)

        self.gui.chances_label.setText("3")
        self.gui.score_label.setText("0")
        self.gui.groupBox.setVisible(False)
        self.gui.won_label.setVisible(False)
        

        self.camCapture = webCamCapture(self.gui.webCamContainer)

        self.camCapture.setup()
        self.camera = cv2.VideoCapture(0)

        self.gameWidget = gameframe.GameWidget(
            self, container=self.gui.gameContainer)
        self.gameThread = gameframe.GameThread(
            self.gui, self.camCapture, self.gameWidget)

        self.gameThread.setParams(
            self.camCapture.camFrame, self.gameWidget.gameFrame)

        self.gameThread.changeCamFrame.connect(self.setCamImage)

        self.gameThread.setTerminationEnabled(True)
        self.camCapture.thread.moveChange.connect(self.updateGameWidget)
        
        try:
            self.gameThread.start()
        except Exception as e:
            print("Error occured \n \t ", e)
            self.camera.release()
            self.gameThread.Terminate = True
            self.gameThread.terminate()
            self.gameThread.exit()

    def setCamImage(self, image):
        self.camCapture.camFrame.setPixmap(QPixmap.fromImage(image))

    def setGameImage(self, image):
        pass

    def closeEvent(self, event):

        if hasattr(self, 'camCapture'):
            self.camera.release()
            if hasattr(self, "gameThread"):
                self.gameThread.Terminate = True
                self.gameThread.terminate()
                self.gameThread.exit()
           

        print("closing...")

        event.accept()

    def stopThreads(self):
        self.thread.join()
        super(QtGui.QMainWindow, self).closeEvent()

    def updateGameWidget(self, angle):
        print("updating")

    def eventFilter(self, source, event):

            if (event.type() == QEvent.Enter):
            
                shadow = QtWidgets.QGraphicsDropShadowEffect(self,
                                                            blurRadius=9.0,
                                                            color=QtGui.QColor(
                                                                14, 168, 240,140),
                                                            offset=QtCore.QPointF(
                                                                3.0, 3.0),
                                                                
                                                            )
                if source==self.gui.startGameButton:
                    self.gui.startGameButton.setGraphicsEffect(shadow)
                    

            if (event.type() == QEvent.Leave):
                if source==self.gui.startGameButton:
                    self.gui.startGameButton.setGraphicsEffect(None)

            if source==self.gui.hueslider or source==self.gui.satslider or source==self.gui.valueslider :
                self.gui.hsv_text.setText("H : "+str(self.gui.hueslider.value())+" , S: "+str(self.gui.satslider.value())+", V: "+str(self.gui.valueslider.value()))
                        
                

            return QMainWindow.eventFilter(self, source, event)

    def initialiseEffects(self):
        self.gui.startGameButton.installEventFilter(self)
        self.gui.hueslider.installEventFilter(self)
        self.gui.satslider.installEventFilter(self)
        self.gui.valueslider.installEventFilter(self)    

          

    


