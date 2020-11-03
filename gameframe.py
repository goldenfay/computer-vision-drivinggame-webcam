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
import getTheCheeseController2
from getTheCheeseController2 import *

red = [(158, 128, 102), (180, 254, 254)]
green = [(50, 100, 0), (90, 254, 254)]

class GameWidget(QWidget):
    """
        Cheese Game widget
    """

    def __init__(self, controller, parent=None, container: QLayout = None):
        super(GameWidget, self).__init__(parent)
        self.container = container
        self.controller = controller

        self.gameFrame = QLabel()
        self.container.addWidget(self.gameFrame)

    def play(self):
        import random
        self.game = Game(self.gameFrame,(2,2),self.controller.gui.levelSlider.value())
        cheese_poses=random.sample([(i,j) for i in range(self.game.maze.shape[0]) 
                    for j in range(self.game.maze.shape[1]) 
                    if self.game.maze[i,j]!=1 and self.game.maze[i,j]!=2 ],k=4)
        self.game.set_params(self.controller.gui.levelSlider.value() ,cheese_poses)
        self.game.draw()
        

    def update(self,angle):
        print("updating Game Widget ...")        

class Game():
    """
        Basic Cheese Game game object
    """
    EASY = 1
    MEDIUM = 2
    HARD = 3
    SPEAAD_LEVELS = {EASY: 1, MEDIUM: 3, HARD: 5}
    CHANCES=3

    def __init__(self,gameImage:QLabel,initial_pos,level=1,number=20):
        super().__init__()
        self.level=level
        self.CHANCES=3
        self.score=0
        self.WIN=False
        self.game_image=gameImage
        self.player_image=cv2.imread("assets/mouse_intro_icon.jpg")
        self.wall_image=cv2.imread("assets/wall.jpg")
        self.wall_image=cv2.resize(self.wall_image, (int(gameImage.width()/number), int(gameImage.height()/number)))
        self.block_unit=self.wall_image.shape
        self.player_image=cv2.resize(self.player_image, (self.wall_image.shape[1], self.wall_image.shape[0]))
        self.cheese_image=cv2.imread("assets/cheese.jpg")
        self.cheese_image=cv2.resize(self.cheese_image, (self.wall_image.shape[1], self.wall_image.shape[0]))
        self.player_x=initial_pos[0]
        self.player_y=initial_pos[1]
        self.cheese_positions=[]
        #self.maze=self.generateMazeShape(int(gameImage.height()/self.wall_image.shape[0]),int(gameImage.width()/self.wall_image.shape[1]),initial_pos)
        self.maze=self.generateMazeShape(number,number,initial_pos)
        self.draw()

        

    def set_params(self,level,cheese_positions:list=None) :
        self.level=level
        if level==1:
            self.CHANCES=3
        elif level==2:
            self.CHANCES=2
        else:
            self.CHANCES=1    

        if cheese_positions is not None:
            for (i,j) in cheese_positions:
                if j in range(self.maze.shape[1]) and i in range(self.maze.shape[0]):   
                    self.maze[i,j]=3 if self.maze[i,j]==0 else 0  
                    self.cheese_positions.append((i,j)) 
            


    def generateMazeShape(self,nbl,nbcol,initialpos):
            # 1: obstacle , 2: player pos, 3: cheesePos
        shap=numpy.zeros((nbl,nbcol))
        import random
            

        for i in range(shap.shape[0]):
            for j in range(shap.shape[1]):
                if i == 0 or i == nbl - 1 or j == 0 or j == nbcol - 1:
                    shap[i, j] = 1
                    continue
                    # Opencv : x is col and y is line
                if i==initialpos[1] and j==initialpos[0]:
                    shap[i,j]=2
                    continue
                shap[i,j]=0

                    
                if j==int(nbcol/2) and i in range(int(nbl/4),int(nbl*3/4)):
                        
                    shap[i,j]=1

        if self.level==2:
            print("MEDIUM")
            random_walls=random.sample([(i,j) for i in range(shap.shape[0]) 
                                                for j in range(shap.shape[1]) 
                                                if shap[i,j]==0],k=5)
            for (i,j) in random_walls:     
                shap[i,j]=1 

        elif self.level==3:
            print("HARD")        
            
            random_walls=random.sample([(i,j) for i in range(shap.shape[0]) 
                                                for j in range(shap.shape[1]) 
                                                if shap[i,j]==0],k=8)
            for (i,j) in random_walls:     
                shap[i,j]=1           



        return shap         

              

    def draw(self):
        img=numpy.full((self.maze.shape[0]*self.wall_image.shape[0],self.maze.shape[1]*self.wall_image.shape[1],3),255,dtype="uint8")
        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                if self.maze[i,j]==1:
                    img[i*self.block_unit[0]:i*self.block_unit[0]+self.block_unit[0],
                        j*self.block_unit[1]:j*self.block_unit[1]+self.block_unit[1]]=self.wall_image[:]
                if self.maze[i,j]==2:
                    img[i*self.block_unit[0]:i*self.block_unit[0]+self.block_unit[0],
                        j*self.block_unit[1]:j*self.block_unit[1]+self.block_unit[1]]=self.player_image[:]

                if self.maze[i,j]==3:
                    img[i*self.block_unit[0]:i*self.block_unit[0]+self.block_unit[0],
                        j*self.block_unit[1]:j*self.block_unit[1]+self.block_unit[1]]=self.cheese_image[:]         

        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QtGui.QImage(img.data,img.shape[1],img.shape[0],
                                        img.shape[1] * img.shape[2], QtGui.QImage.Format_RGB888)
        pix = convertToQtFormat.scaled(self.game_image.width(), self.game_image.height(), Qt.KeepAspectRatio)
        self.game_image.setPixmap(QPixmap.fromImage(pix))

    def moveplayer(self,direction):
        self.maze[self.player_y,self.player_x]=0
        x=self.player_x
        y=self.player_y
        if direction==0:
            self.moveRight()
        elif direction==1:
            self.moveRight()
            self.moveUp()
        elif direction==2:
            self.moveUp()  
        elif direction==3:
            self.moveLeft()
            self.moveUp()
        elif direction==4:
            self.moveLeft()
        elif direction==5:
            self.moveDown()
            self.moveLeft()
        elif direction==6:
            self.moveDown()
        else: 
            self.moveDown()
            self.moveRight()     
        try:
             
            if self.maze[self.player_y,self.player_x]==1:
                print("Wall Crash")
                self.player_x=x
                self.player_y=y
                self.CHANCES-=1
                if self.CHANCES==0:
                    raise OutOfMazeException("Out Of boundaries")
            elif (self.player_y,self.player_x)  in self.cheese_positions:
                    self.cheese_positions.remove((self.player_y,self.player_x))
                    self.score+=1
                    if len(self.cheese_positions)==0:
                        print("YOU WON !!")
                        raise WinnerException("You won dude !")
                    
            self.maze[self.player_y,self.player_x]=2       
        except  IndexError as ie:
            print("crashhh!!!!!!!")
            self.player_x=x
            self.player_y=y
            self.CHANCES-=1
            if self.CHANCES==0:
                raise OutOfMazeException("Out Of boundaries")              

    def moveRight(self):
        self.player_x += self.SPEAAD_LEVELS[self.level] 

    def moveLeft(self):
        self.player_x -= self.SPEAAD_LEVELS[self.level]

    def moveUp(self):
        self.player_y -= self.SPEAAD_LEVELS[self.level]

    def moveDown(self):
        self.player_y += self.SPEAAD_LEVELS[self.level]



class GameThread(QThread):
    """
        Custom PyQt thread class to enable threads in GUI.
    """
    
    changeCamFrame = pyqtSignal(QImage)
    changeGameFrame = pyqtSignal(QImage)
    def __init__(self,gui:GetTheCheese_MainWindow,camWidget:webCamCapture=None, gameWidget:GameWidget=None):
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
        
        
        try:
            self.camera=cv2.VideoCapture(0)
            game=self.gameW.play()
            cpt=0
            while True:

                ok,self.frame=self.camera.read()
                cpt+=1

                if cpt==120:
                    cpt=0
                if self.frame is not None and cpt%2==0:
                        print(self.frame.data)
                        self.frame=cv2.flip(self.frame,1)
                        [self.frame,self.direction]=self.treatFrame(self.frame)
                        self.frame=cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                        height, width, channel = self.frame.shape
                        bytesPerLine = channel * width
                        convertToQtFormat = QtGui.QImage(self.frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
                        pix = convertToQtFormat.scaled(self.camFrame.width(),self.camFrame.height(), Qt.KeepAspectRatio)
                        self.changeCamFrame.emit(pix)
                        self.changeGameFrame.emit(pix)
                        
                        
                if cv2.waitKey(1) & 0xFF == ord('q') or self.Terminate:
                        self.camera.release()  
                        break

        except Exception as ce:
            print("WEBCAM THREAD : Error on video recording \n \t ")
            self.camera.release()
            traceback.print_exc()  
            self.terminate()
            self.exit()


    def setGameImage(self,image):
        
     
        try:
            if self.direction!=-1:
                self.gameW.game.moveplayer(self.direction) 
                self.gameW.controller.gui.chances_label.setText(str(self.gameW.game.CHANCES))
                self.gameW.controller.gui.score_label.setText(str(self.gameW.game.score))
                
                self.gameW.game.draw() 
        except OutOfMazeException as out:
            label=QLabel("Game Over")
            self.gameW.controller.gui.groupBox.setVisible(True)
            self.Terminate=True   
            self.terminate()
        except WinnerException as we:
            print("Yey")
            img=cv2.imread("assets/win_img.jpg")
            img=cv2.resize(img,(self.gameFrame.width(),self.gameFrame.height()))
            convertToQtFormat = QtGui.QImage(img.data,img.shape[1],img.shape[0],
                                        img.shape[1] * img.shape[2], QtGui.QImage.Format_RGB888)
            pix = convertToQtFormat.scaled(self.gameFrame.width(), self.gameFrame.height(), Qt.KeepAspectRatio)
            self.gameFrame.setPixmap(QPixmap.fromImage(pix))
            self.gameW.controller.gui.won_label.setVisible(True)
            self.terminate()
            self.exit()

    def treatFrame(self,frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   
        
            # Note : Coment the line and uncomment the 3 others
        # color1=[(self.gameW.controller.gui.hueslider.value()-20,self.gameW.controller.gui.satslider.value()-10,self.gameW.controller.gui.valueslider.value()-10),
        #         (self.gameW.controller.gui.hueslider.value()+20,self.gameW.controller.gui.satslider.value()+10,self.gameW.controller.gui.valueslider.value()+10)]
        return self.detectColors(frame,green,red)
        # return self.detectColors(frame,green,color1)




                        
        
    # Detection function ordered in project
    # Only basique opencV functions and standard python function used
    
    def detectColors(self,original,color1,color2):
        frame=cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
        
        matchSet1=[]
        matchSet2=[]

        for i  in range(0,frame.shape[0],4):
            for j in range(0,frame.shape[1],4):
                if (frame[i,j]>=color1[0]).all() and (frame[i,j]<=color1[1]).all():
                    matchSet1.append((i,j))


                if (frame[i,j]>=color2[0]).all() and (frame[i,j]<=color2[1]).all():
                    matchSet2.append((i,j))    
        

       

        
        direction = -1
        center1=center2=None

        if len(matchSet1) >= 100 and len(matchSet2) >= 200:

            x_min = min(matchSet1, key=lambda val: val[1])[1]
            y_min = min(matchSet1, key=lambda val: val[0])[0]
            x_max = max(matchSet1, key=lambda val: val[1])[1]
            y_max = max(matchSet1, key=lambda val: val[0])[0]

            cv2.rectangle(original, (x_min, y_min), (x_max, y_max), (10, 198, 250), 2)
            center1 = (int((x_min+x_max)/2), int((y_min+y_max)/2))
            cv2.circle(original, center1, 2, (10, 198, 250), -1)

            x_min = min(matchSet2, key=lambda val: val[1])[1]
            y_min = min(matchSet2, key=lambda val: val[0])[0]
            x_max = max(matchSet2, key=lambda val: val[1])[1]
            y_max = max(matchSet2, key=lambda val: val[0])[0]
            cv2.rectangle(original, (x_min, y_min), (x_max, y_max), (10, 198, 250), 2)
            center2 = (int((x_min+x_max)/2), int((y_min+y_max)/2))
            cv2.circle(original, center2, 2, (10, 198, 250), -1)

            cv2.arrowedLine(original, center1, center2, (10, 198, 250), 2, cv2.LINE_AA)

            sin = center2[1] - center1[1]
            cos = center2[0] - center1[0]
            
            if cos == 0 :
                angle = 90 
            else :
                angle=int(abs(math.degrees(math.atan(sin/cos))))

            if not (sin <= 0 and cos >= 0):
                if sin <= 0 and cos <= 0:
                    angle = 180 - angle
                elif sin > 0 and cos <= 0:
                    angle += 180
                elif sin > 0 and cos > 0:
                    angle = 360 - angle

            text = ""

            if (0 <= angle <= 20) or (340 <= angle <= 360):
                text = "RIGHT"
                direction = 0
            elif 40 <= angle <= 60:
                text = "UP RIGHT"
                direction = 1
            elif 80 <= angle <= 100:
                text = "UP"
                direction = 2
            elif 120 <= angle <= 150:
                text = "UP LEFT"
                direction = 3
            elif 170 <= angle <= 190:
                text = "LEFT"
                direction = 4
            elif 210 <= angle <= 240:
                text = "DOWN LEFT"
                direction = 5
            elif 260 <= angle <= 280:
                text = "DOWN"
                direction = 6
            elif 300 <= angle <= 330:
                text = "DOWN RIGHT"
                direction = 7

            text = "GO "+text+" with "+str(angle)+" degrees."

            cv2.putText(original, text, (center2[0]+10,center2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (42, 10, 219), 4)

        return [original,direction]









def paintImage(small_image, image, x, y):
    np = small_image.shape[0]
    mp = small_image.shape[1]
    image[x:x + np, y:y + mp] = small_image[:, :]

class OutOfMazeException(Exception):

    pass

class WinnerException(Exception):
    pass


