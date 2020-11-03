from firstwindow import *
from mainwindowsController import MainWindow_Controller
import mainwindows
from PyQt5 import QtGui, QtCore, QtWidgets
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import getTheCheese, getTheCheeseController



class firstWindow_Controller(QObject):

    def __init__(self, gui: Ui_MainWindow):
        super().__init__()
        self.gui = gui

    def setWindow(self,window:QMainWindow):
        self.mainWindow=window    
        

    def setup(self):
        self.gui.startButton.clicked.connect(lambda: self.goToMainWindow())




    def goToMainWindow(self):
        mainWindow=mainwindows.mainwindows_MainWindow()
        
        window=QMainWindow(self.gui.centralwidget)
        mainWindow.setupUi(window)
        cntr=MainWindow_Controller(mainWindow)
        cntr.setWindow(window)
        cntr.setup()
        #self.mainWindow.hide()
        window.show()
        
        



if __name__ == "__main__":
    import sys
  

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = getTheCheese.GetTheCheese_MainWindow()
    ui.setupUi(MainWindow)
    controller=getTheCheeseController.getTheCheese_Controller(ui)
    controller.setWindow(MainWindow)
    try:
        controller.setup()
    
        MainWindow.show()
    except Exception as e:
        print(e)    
    sys.exit(app.exec_())
