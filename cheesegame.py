from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
import sys, time, math,traceback,threading
import numpy
import cv2
from webcam import *
from getTheCheese import GetTheCheese_MainWindow


class CheeseGameWidget(QWidget):
    """
        Cheese game widget
    """

    def __init__(self, widget:QWidget, parent=None, container: QLayout = None):
        super(CheeseGameWidget, self).__init__(parent)
        self.container = container
        self.widget = widget

        self.initialize()

    def initialize(self):
        self.gameFrame = QLabel()
        self.container.addWidget(self.gameFrame)


    def play(self):
        
        player = Player(1, 1, "")
        self.game = Game(self.container, self.gameFrame,player, level=2)
        self.game.setSettings(cheesePositions=[(1, 2),(12,12)])

    
    def update(self,angle):
        print("updating Game Widget ...")        


class Player:
    """
        Basic Cheese game player
    """
    def __init__(self, x: int, y: int, img: str, speed=1):
        super().__init__()
        self.initial_x = self.x = x
        self.initial_y = self.y = y
        self.speed = speed
        self.image = img

    def move(self, angle: float):
        amountx = math.cos(angle)
        amounty = math.sin(angle)
        if math.cos(angle) >= 0:
            self.moveRight(math.fabs(amountx * self.speed))
        else:
            self.moveLeft(math.fabs(amountx * self.speed))

        if math.sin(angle) >= 0:
            self.moveUp(math.fabs(amounty * self.speed))
        else:
            self.moveDown(math.fabs(amounty * self.speed))

    def moveRight(self, amount):
        self.x = int(self.x + amount)

    def moveLeft(self, amount):
        self.x = int(self.x - amount)

    def moveUp(self, amount):
        self.y = int(self.y - amount)

    def moveDown(self, amount):
        self.y = int(self.y + amount)


class Maze:
    def __init__(self, N: int, M: int, shape=None, wallImage=None):
        self.M = M
        self.N = N
        if shape is None:
            self.mazeShape = numpy.ndarray(shape=(N, M))
            self.mazeShape = self.makeShape()
        else:
            self.mazeShape = shape
        self.getObstacles()
        if wallImage is not None:
            self.wallImage = cv2.imread(wallImage)
        else:
            self.wallImage = cv2.imread("assets/wall.jpg")

        self.BLOCK_UNIT=self.wallImage.shape    
        _, self.playerImage = cv2.VideoCapture("assets\\running_mouse.gif").read()
        self.playerImage = cv2.resize(self.playerImage, (self.wallImage.shape[1] * 2, self.wallImage.shape[0] * 2))
        self.previousPos = None

    def draw(self, display_widget: QWidget):
        self.widget = display_widget
        n = self.wallImage.shape[0]
        m = self.wallImage.shape[1]
        ch = self.wallImage.shape[2]

        np = self.playerImage.shape[0]
        mp = self.playerImage.shape[1]
        self.image = numpy.full((self.N * n, self.M * m, 3), 255, dtype="uint8")
        for i in range(0, self.N):
            for j in range(self.M):
                if self.mazeShape[i, j] == 1:
                    self.image[i * n:i * n + n, j * m:j * m + m] = self.wallImage[:, :]
                if self.mazeShape[i, j] == 2:
                    self.image[i * np:i * np + np, j * mp:j * mp + mp] = self.playerImage[:, :]

         
        convertToQtFormat = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0],
                                         self.image.shape[1] * ch, QtGui.QImage.Format_RGB888)
        pix = convertToQtFormat.scaled(display_widget.width(), display_widget.height(), Qt.KeepAspectRatio)
        display_widget.setPixmap(QPixmap.fromImage(pix))

    def render(self, playerPos):

        self.mazeShape[playerPos[0], playerPos[1]] = 2
        np = self.playerImage.shape[0]
        mp = self.playerImage.shape[1]

        distance = 0
            # Clear previous painted
        if self.previousPos is not None:
            self.mazeShape[self.previousPos[0], self.previousPos[1]] = 0
            self.image[self.previousPos[0] * np:self.previousPos[0] * np + np,
                        self.previousPos[1] * mp:self.previousPos[1] * mp + mp] = [255, 255, 255]
        else: self.previousPos=(0,0)

        distX = math.pow(playerPos[0] - self.previousPos[0], 2)
        distY = math.pow(playerPos[1] - self.previousPos[1], 2)
        distance = math.sqrt(distX + distY)

        if distance > 0:
            cap = cv2.VideoCapture("assets/running_mouse.gif")
            _, frame = cap.read()
            i = 1
            while i < 10 and frame is not None:
                
                frame = cv2.resize(frame, (self.playerImage.shape[1], self.playerImage.shape[0]))
                frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                paintImage(frame, self.image, int(self.previousPos[0] + distX / 10),
                           int(self.previousPos[1] + distY / 10))
                convertToQtFormat = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0],
                                                 self.image.shape[1] * 3, QtGui.QImage.Format_RGB888)
                pix = convertToQtFormat.scaled(self.widget.width(), self.widget.height(), Qt.KeepAspectRatio)
                self.widget.setPixmap(QPixmap.fromImage(pix))
                
                cv2.waitKey(1)
                _, frame = cap.read()
                i += 1

        self.previousPos = playerPos
        print("render finished")

    def makeShape(self):
        for i in range(self.N):
            for j in range(self.M):
                if i == 0 or i == self.N - 1 or j == 0 or j == self.M-1:
                    self.mazeShape[i, j] = 1
                else:
                    self.mazeShape[i, j] = 0

    def getObstacles(self):
        self.walls = []
        for i in range(self.N):
            for j in range(self.M):
                if self.mazeShape[i, j] == 1:
                    self.walls.append((i, j))


class Game:
    """
        Base Cheese game Game object.
    """
    EASY = 1
    MEDIUM = 2
    HARD = 3
    SPEAAD_LEVELS = {EASY: 1, MEDIUM: 4, HARD: 8}

    def __init__(self, surface:QLayout, container:QLabel,player:Player, maze: Maze = None, level=1):
        super().__init__()
        self.container = container
        self.surface = surface
        self.running = False
        self.level = level
        self.player = player
        self.player.speed = self.SPEAAD_LEVELS[self.level]
        if maze is None:
            self.maze = self.generateMaze(int(self.container.height()/24)-1, int(self.container.height()/24)-1)  # int(self.container.height()/13),int(self.container.height()/16))
        else:
            self.maze = maze
        try:
            self.maze.mazeShape[self.player.initial_x,self.player.initial_y]=2
            
        except:
            pass    
        self.maze.draw(self.container)
        self.container.setStyleSheet("border: 2px inset red;")

    def setSettings(self, player: Player=None,maze: Maze = None, cheesePositions: list = None, wallImage=""):
        if player is not None:
            self.player = player
            self.player.speed = self.SPEAAD_LEVELS[self.level]
        
        if maze is not None:
            self.maze = maze
        self.wallImage = wallImage

        if cheesePositions is not None:
            for (x,y) in cheesePositions:
                try:
                    self.maze.mazeShape[x,y]=3
                except:
                    pass


            self.maze.draw(self.container)    
        

    def start(self):
        self.running = True

    def pause(self):
        pass

    def finish(self):
        self.running = False

    def stateUpdated(self, angle):
        playerAngle = self.calculateAngle(angle, self.player.x, self.player.y)
        self.player.move(0)
        print("New Coordinates :",(self.player.x, self.player.y))
        pHeight = self.maze.wallImage.shape[0]
        pwidth = self.maze.wallImage.shape[1]
        if self.player.x * pHeight + self.maze.playerImage.shape[0] < self.maze.image.shape[0] \
                and self.player.y * pwidth + self.maze.playerImage.shape[1] < self.maze.image.shape[1] \
                and self.player.x > self.maze.BLOCK_UNIT[0] \
                and self.player.y > self.maze.BLOCK_UNIT[1]:
            thread1 = threading.Thread(target =self.maze.render , args = ((self.player.x, self.player.y)))
            thread1.start()
            
        else: print("Crash !!!")    

    def calculateAngle(self, angle, x, y):

        return angle

    def generateMaze(self, width, height):

        shape = numpy.ndarray(shape=(height, width))
        for i in range(height):
            for j in range(width):
                if i == 0 or i == height - 1 or j == 0 or i == width - 1:
                    shape[i, j] = 1

        if self.level == self.EASY:
            for i in range(1, height - 1):
                for j in range(1, width - 1):
                    if j % (width / 4) == 0 and i in range(int(height / 4), int(height / 4 * 3)):
                        shape[i, j] = 1

        if self.level == self.MEDIUM:
            for i in range(height):
                for j in range(width):
                    if i == 0 or i == height - 1 or j == 0 or i == width - 1:
                        shape[i, j] = 1
        return Maze(height, width, shape)


class GameThread(QThread):
    """
        Custom GUI Thread to enable PyQT threads on UI
    """
    
    changeCamFrame = pyqtSignal(QImage)
    changeGameFrame = pyqtSignal(QImage)
    def __init__(self,gui:GetTheCheese_MainWindow,camWidget:webCamCapture=None, gameWidget:CheeseGameWidget=None):
        super().__init__()
        self.gui=gui
        self.gameW=gameWidget
        self.camW=camWidget



    def setParams(self,camFrame:QLabel,gameFrame:QLabel):
        self.camFrame=camFrame
        self.gameFrame=gameFrame
        self.Terminate=False
        self.changeGameFrame.connect(self.setGameImage)


    def run(self):
        self.gui.gameSettingsGB.setEnabled(False)
        #self.gui.startGameButton.setEnabled(False)
        
        try:
            self.camera=cv2.VideoCapture(0)
            game=self.gameW.play()
            while True:

                ok,self.frame=self.camera.read()
                if self.frame is not None:
                        
                        [self.frame,(self.x1,self.y1),(self.x2,self.y2)]=self.treatFrame(self.frame)
                        self.frame=cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                        height, width, channel = self.frame.shape
                        bytesPerLine = channel * width
                        convertToQtFormat = QtGui.QImage(self.frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
                        pix = convertToQtFormat.scaled(width,height, Qt.KeepAspectRatio)
                        #pix = QtGui.QPixmap(QtGui.QImage(self.frame.data, width, height, width*2, QtGui.QImage.Format_RGB888))
                        self.changeCamFrame.emit(pix)
                        self.changeGameFrame.emit(pix)
                        
                if cv2.waitKey(300) & 0xFF == ord('q') or self.Terminate:
                        self.camera.release()  
                        break

        except Exception as ce:
            print("Error on video recording \n \t ")
            self.camera.release()
            traceback.print_exc()  
            self.terminate()


    def setGameImage(self,image):
        
        if self.x1 is None or self.y1 is None or self.x2 is None or self.y2 is None: return

        try:
            angle=math.atan((self.x1-self.x2)/(self.y1-self.y2))*180/math.pi
        except ZeroDivisionError as ze:
            angle=90.0
        print("Angle : ",angle)
        #self.gameW.game.calculateAngle(angle)
        self.gameW.game.stateUpdated(angle)
        #self.gameFrame.setPixmap(QPixmap.fromImage(image))    

    def treatFrame(self,frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   
        #frame=self.detectContours(frame)
        # frame=self.contoursDetection(frame)

        return self.contoursDetection(frame)



    def detectContours(self,frame):
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
                center1X = int(M["m10"] / M["m00"])
                center1Y = int(M["m01"] / M["m00"]) 
                cv2.circle(frame, (center1X, center1Y), 7, (255, 255, 255), -1)
                cv2.putText(frame,"Triangle detected",(center1X - 20, center1Y - 20),cv2.FONT_HERSHEY_PLAIN,0.5,(255,10,1))
        return frame        


    def contoursDetection(self,original):
        frame=cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
        # Red color
        low_red = np.array([161, 20, 70])
        high_red = np.array([190, 255, 255])
        # blue color
        bl=numpy.uint8([[[255,0,0]]])
        hsv_blue=cv2.cvtColor(bl,cv2.COLOR_BGR2HSV)

        low_blue = np.array([94, 80, 2])
        high_blue = np.array([126, 255, 255])
        # low_blue =numpy.array([hsv_blue[0][0][0]-10,hsv_blue[0][0][1]-20,hsv_blue[0][0][2]-20]) #np.array([0, 0, 0])
        # high_blue =numpy.array([hsv_blue[0][0][0]+10,hsv_blue[0][0][1]+20,hsv_blue[0][0][2]+20]) #np.array([50, 50, 100])
        
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
        thresh_blue = cv2.threshold(blurred_blue, 60, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]
        
        cnts = cv2.findContours(thresh_blue.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        center1X=None
        center1Y=None
        center2X=None
        center2Y=None
        for c in cnts:
            regionApprox=cv2.approxPolyDP(c,0.1*cv2.arcLength(c,True),True)
            if not len(regionApprox)==3: continue
            print("red triangle detected")
            # compute the center of the contour
            M = cv2.moments(c)
            try :
                center1X = int(M["m10"] / M["m00"])
                center1Y = int(M["m01"] / M["m00"]) 
                cv2.drawContours(original, [c], -1, (0, 255, 0), 2)
                cv2.circle(original, (center1X, center1Y), 7, (255, 255, 255), -1)
                cv2.putText(original, "center1", (center1X - 20, center1Y - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.drawContours(original, [c], -1, (0, 255, 0), 2)
                cv2.circle(original, (center1X, center1Y), 7, (255, 255, 255), -1)
                cv2.putText(original, "center1", (center1X - 20, center1Y - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                break
            except :
                pass
            
        cnts = cv2.findContours(thresh_red.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
            regionApprox=cv2.approxPolyDP(c,0.1*cv2.arcLength(c,True),True)
            if not len(regionApprox)==4: continue
            # compute the center of the contour
            M = cv2.moments(c)
            try :
                center2X = int(M["m10"] / M["m00"])
                center2Y = int(M["m01"] / M["m00"]) 
                cv2.drawContours(original, [c], -1, (0, 255, 0), 2)
                cv2.circle(original, (center2X, center2Y), 7, (255, 255, 255), -1)
                cv2.putText(original, "center2", (center2X - 20, center2Y - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.drawContours(original, [c], -1, (0, 255, 0), 2)
                cv2.circle(original, (center2X, center2Y), 7, (255, 255, 255), -1)
                cv2.putText(original, "center2", (center2X - 20, center2Y - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                break
            except :
                pass  

        if center1X is not None and center1Y is not None and center2X is not None and center2X is not None:
            cv2.arrowedLine(self.frame,(center1X,center1Y),(center2X,center2Y),(0,0,255),4)
            angle=math.atan((center1X-center1Y)/(center2X-center2Y))*180/math.pi
            cv2.putText(self.frame,"Angle   "+str(angle)[:4], (center2X - 20, center2Y - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)    
        return [original,(center1X,center1Y),(center2X,center2X)]                    



def paintImage(small_image, image, x, y):
    """
        Util function to repaint the image after player moves
    """
    np = small_image.shape[0]
    mp = small_image.shape[1]
    image[x:x + np, y:y + mp] = small_image[:, :]




