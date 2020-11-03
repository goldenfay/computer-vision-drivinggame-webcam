import cv2
import imutils
import numpy as np
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import QThread, Qt, pyqtSignal

class webCamCapture(QWidget):
    """
        Webcam video capture widget class.
    """
    update_video = QtCore.pyqtSignal()
    def __init__(self, parent:QtWidgets.QLayout=None):
        super(QWidget, self).__init__()
        self.parent=parent
        self.thread=WebCamThread(self)
        #self.setLayout(parent)

        





    def setup(self):
        self.camFrame=QLabel()
        self.parent.addWidget(self.camFrame)
    


    def startRecording(self):
        print("Start Capturing....")
        self.webcam = cv2.VideoCapture(0)
        try:
            self.thread.setParams(self.camFrame,self.webcam)
            self.thread.changePixmap.connect(self.setImage)
            self.thread.setTerminationEnabled(True)
            self.thread.start()
        except Exception as e:
            print("Error occured when capturing \n \t ",e) 
            self.webcam.release()
        
        
    
    def setImage(self, image):
        self.camFrame.setPixmap(QPixmap.fromImage(image))    

    
    





class WebCamThread(QThread):
    """
        Custom PyQT thread to enable threading on GUI
    """
    changePixmap = pyqtSignal(QImage)
    moveChange=pyqtSignal(object)
    
    def __init__(self, parent):
        super().__init__(parent)

    def setParams(self,frame,webcam):
        self.camFrame=frame
        self.camera=webcam
        self.Terminate=False

    def run(self):
       
        try:
            while True:
                
                ok,self.frame=self.camera.read()
                if self.frame is not None:
                    print('self.frame.data)')
                    # treatFrame(self.frame)
                    height, width, channel = self.frame.shape
                    bytesPerLine = channel * width
                    convertToQtFormat = QtGui.QImage(self.frame.data, width, height, bytesPerLine)
                    pix = convertToQtFormat.scaled(width,height, Qt.KeepAspectRatio)
                    #pix = QtGui.QPixmap(QtGui.QImage(self.frame.data, width, height, width*2, QtGui.QImage.Format_RGB888))
                    self.changePixmap.emit(pix)
                    self.moveChange.emit(45)
                    
                if cv2.waitKey(100) & 0xFF == ord('q') or self.Terminate:
                    
                    self.camera.release()  
                    break 


                
        except Exception as ce:
            print("Error on video recording \n \t ",ce)
            self.camera.release()

    def terminate(self):
        print("bye bye")
        return super().terminate()
    

def treatFrame(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   
    #detectContours(frame)
    contoursDetection(hsv_frame)



def detectContours(frame):
    """
        Detect contours in the giving frame, using pre-defined findContours function
    """
    imgGrey=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    _,seuil=cv2.threshold(imgGrey,10,255,cv2.THRESH_BINARY)
    contours,_=cv2.findContours(seuil,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    if len(contours)==0:
        print("No contour found")
    for contour in contours:
        regionApprox=cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        
        cv2.drawContours(frame,[regionApprox],0,(66, 135, 245),4)
        if len(regionApprox)==3:
            
            M = cv2.moments(contour)
            centreDebutX = int(M["m10"] / M["m00"])
            centreDebutY = int(M["m01"] / M["m00"]) 
            cv2.circle(frame, (centreDebutX, centreDebutY), 7, (255, 255, 255), -1)
            cv2.putText(frame,"Triangle detected",(centreDebutX - 20, centreDebutY - 20),cv2.FONT_HERSHEY_PLAIN,0.5,(255,10,1))


def contoursDetection(frame):
    """
        Detect contours in the giving frame, using classic method
    """
    # Red color
    low_red = np.array([161, 20, 70])
    high_red = np.array([190, 255, 255])
    # blue color
    low_blue = np.array([0, 0, 0])
    high_blue = np.array([50, 50, 100])
    
    red_mask = cv2.inRange(frame, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)
    
    blue_mask = cv2.inRange(frame, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    
    mask_result = cv2.bitwise_or(blue_mask, red_mask)
    result = cv2.bitwise_and(frame,frame, mask=mask_result)
    
    gray_red = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
    gray_blue = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
    
    blurred_red = cv2.GaussianBlur(gray_red, (5, 5), 0)
    blurred_blue = cv2.GaussianBlur(gray_blue, (5, 5), 0)
    
    thresh_red = cv2.threshold(blurred_red, 60, 255, cv2.THRESH_BINARY)[1]
    thresh_blue = cv2.threshold(blurred_blue, 60, 255, cv2.THRESH_BINARY)[1]
    
    cnts = cv2.findContours(thresh_red.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    centreDebutX=None
    centreDebutY=None
    centreFinX=None
    centreFinY=None
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        try :
            centreDebutX = int(M["m10"] / M["m00"])
            centreDebutY = int(M["m01"] / M["m00"]) 
            cv2.drawContours(red, [c], -1, (0, 255, 0), 2)
            cv2.circle(red, (centreDebutX, centreDebutY), 7, (255, 255, 255), -1)
            cv2.putText(red, "center1", (centreDebutX - 20, centreDebutY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv2.circle(frame, (centreDebutX, centreDebutY), 7, (255, 255, 255), -1)
            cv2.putText(frame, "center1", (centreDebutX - 20, centreDebutY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            break
        except :
            pass
        
    cnts = cv2.findContours(thresh_blue.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        try :
            centreFinX = int(M["m10"] / M["m00"])
            centreFinY = int(M["m01"] / M["m00"]) 
            cv2.drawContours(blue, [c], -1, (0, 255, 0), 2)
            cv2.circle(blue, (centreFinX, centreFinY), 7, (255, 255, 255), -1)
            cv2.putText(blue, "center2", (centreFinX - 20, centreFinY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv2.circle(frame, (centreFinX, centreFinY), 7, (255, 255, 255), -1)
            cv2.putText(frame, "center2", (centreFinX - 20, centreFinY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            break
        except :
            pass