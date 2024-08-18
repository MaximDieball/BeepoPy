from IDE import Ui_IDE
import sys
import time
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QFont
from PyQt5 import QtCore, QtGui, QtWidgets


#   SYNTAX ["Beepo","Wall","Gear","Door","Button"] x = empty
grid = []

# globale variablen
directions = ["n", "o", "s", "w"]
beepo_x = 0
beepo_y = 0
beepo_rotation = "s"
selected_piece = "B"
grid_height = 4
grid_width = 4
error = "code crashed"
gears_picked_up = 0
sleep_time = 1

# MAIN WINDOW/APP CLASS
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    # overwriting resizeEvent from pyqt5 to RESIZE WINDOW correctly
    def resizeEvent(self, event):
        self.RightButtonFrame.setGeometry(QtCore.QRect(event.size().width()-181, 0, 181, event.size().height()))
        self.LeftButtonFrame.setFixedHeight(event.size().height())
        self.BottomButtonFrame.setGeometry(QtCore.QRect(180, event.size().height() - 180, event.size().width()-360, 161))
        self.TopButtonFrame.setGeometry(QtCore.QRect(180, 0, event.size().width()-360, 101))

    def setupUi(self):

        # MAIN WINDOW
        self.setObjectName("MainWindow")
        self.resize(919, 655)
        self.setMinimumSize(QtCore.QSize(919, 655))
        self.setMaximumSize(QtCore.QSize(3000, 3000))

        # CENTRAL WIDGET
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("background: rgb(190, 233, 232)")
        self.centralwidget.setObjectName("centralwidget")

        # RIGHT BUTTON FRAME
        self.RightButtonFrame = QtWidgets.QFrame(self.centralwidget)
        self.RightButtonFrame.setGeometry(QtCore.QRect(740, 0, 181, 631))
        self.RightButtonFrame.setStyleSheet("background: rgb(98, 182, 203)")
        self.RightButtonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.RightButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.RightButtonFrame.setObjectName("RightButtonFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.RightButtonFrame)
        self.verticalLayout.setObjectName("verticalLayout")

        # LEFT BUTTON FRAME
        self.LeftButtonFrame = QtWidgets.QFrame(self.centralwidget)
        self.LeftButtonFrame.setGeometry(QtCore.QRect(0, 0, 181, 631))
        self.LeftButtonFrame.setStyleSheet("background: rgb(98, 182, 203)")
        self.LeftButtonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LeftButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LeftButtonFrame.setObjectName("LeftButtonFrame")

        # TOP BUTTON FRAM
        self.TopButtonFrame = QtWidgets.QFrame(self.centralwidget)
        self.TopButtonFrame.setGeometry(QtCore.QRect(180, 0, 561, 101))
        self.TopButtonFrame.setStyleSheet("background: rgb(98, 182, 203)")
        self.TopButtonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TopButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TopButtonFrame.setObjectName("TopButtonFrame")

        # BOTTOM BUTTON FRAME
        self.BottomButtonFrame = QtWidgets.QFrame(self.centralwidget)
        self.BottomButtonFrame.setGeometry(QtCore.QRect(180, 470, 561, 161))
        self.BottomButtonFrame.setStyleSheet("background: rgb(98, 182, 203)")
        self.BottomButtonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BottomButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BottomButtonFrame.setObjectName("DownButtonFrame")

        # FILL FRAME
        self.frame_6 = QtWidgets.QFrame(self.RightButtonFrame)
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout.addWidget(self.frame_6)

        # GEAR COUNTER
        self.GearCounter = QtWidgets.QLabel(self.frame_6)
        self.GearCounter.setGeometry(QtCore.QRect(6,0,50,50))
        self.GearCounter.setObjectName("GearCounter")

        # LOGO
        self.Logo = QtWidgets.QLabel(self.TopButtonFrame)
        self.Logo.setGeometry(QtCore.QRect(0, 0, 600, 100))
        self.Logo.setObjectName("GearCounter")
        self.Logo.setFont(QFont("Arial", 10))
        self.Logo.setText("""
  ___                    ___      
 | _ ) ___ ___ _ __  ___| _ \\_  _ 
 | _ \\/ -_) -_) '_ \\/ _ \\  _/ || |
 |___/\\___\\___| .__/\\___/_|  \\_, |
              |_|            |__\\/ 

        """)

        # TURN RIGHT BUTTON
        self.TurnRightButton = QtWidgets.QPushButton(self.BottomButtonFrame)
        self.TurnRightButton.setGeometry(80, 20, 60, 60)
        self.TurnRightButton.setObjectName("TurnRightButton")
        self.TurnRightButton.clicked.connect(lambda: (Beepo.turn_right(), self.update()))
        self.TurnRightButton.setIcon(QIcon("imgs/TurnRight.png"))
        self.TurnRightButton.setIconSize(QtCore.QSize(20,20))


        # TURN LEFT BUTTON
        self.TurnLeftButton = QtWidgets.QPushButton(self.BottomButtonFrame)
        self.TurnLeftButton.setGeometry(0, 20, 60, 60)
        self.TurnLeftButton.setObjectName("TurnLeftButton")
        self.TurnLeftButton.clicked.connect(lambda: (Beepo.turn_left(), self.update()))
        self.TurnLeftButton.setIcon(QIcon("imgs/TurnLeft.png"))
        self.TurnLeftButton.setIconSize(QtCore.QSize(20,20))

        # BEEPO BUTTON
        self.BeepoButton = QtWidgets.QPushButton(self.RightButtonFrame)
        self.BeepoButton.setMinimumSize(QtCore.QSize(60, 60))
        self.BeepoButton.setMaximumSize(QtCore.QSize(60, 60))
        self.BeepoButton.setObjectName("BeepoButton")
        self.verticalLayout.addWidget(self.BeepoButton)
        self.BeepoButton.clicked.connect(lambda: self.set_piece("B"))

        # WALL BUTTON
        self.WallButton = QtWidgets.QPushButton(self.RightButtonFrame)
        self.WallButton.setMinimumSize(QtCore.QSize(60, 60))
        self.WallButton.setMaximumSize(QtCore.QSize(60, 60))
        self.WallButton.setObjectName("WallButton")
        self.verticalLayout.addWidget(self.WallButton)
        self.WallButton.clicked.connect(lambda: self.set_piece("W"))

        # GEAR BUTTON
        self.GearButton = QtWidgets.QPushButton(self.RightButtonFrame)
        self.GearButton.setMinimumSize(QtCore.QSize(60, 60))
        self.GearButton.setMaximumSize(QtCore.QSize(60, 60))
        self.GearButton.setObjectName("GearButton")
        self.verticalLayout.addWidget(self.GearButton)
        self.GearButton.clicked.connect(lambda: self.set_piece("G"))

        # BUTTON BUTTON
        self.ButtonButton = QtWidgets.QPushButton(self.RightButtonFrame)
        self.ButtonButton.setEnabled(True)
        self.ButtonButton.setMinimumSize(QtCore.QSize(60, 60))
        self.ButtonButton.setMaximumSize(QtCore.QSize(60, 60))
        self.ButtonButton.setObjectName("ButtonButton")
        self.verticalLayout.addWidget(self.ButtonButton)
        self.ButtonButton.clicked.connect(lambda: self.set_piece("B_np"))

        # DOOR BUTTON
        self.DoorButton = QtWidgets.QPushButton(self.RightButtonFrame)
        self.DoorButton.setEnabled(True)
        self.DoorButton.setMinimumSize(QtCore.QSize(60, 60))
        self.DoorButton.setMaximumSize(QtCore.QSize(60, 60))
        self.DoorButton.setObjectName("DoorButton")
        self.verticalLayout.addWidget(self.DoorButton)
        self.DoorButton.clicked.connect(lambda: self.set_piece("D"))

        # PLAY BUTTON
        self.PlayButton = QtWidgets.QPushButton(self.RightButtonFrame)
        #self.PlayButton.setMinimumSize(QtCore.QSize(0, 100))
        self.PlayButton.setFixedSize(QtCore.QSize(150, 130))
        self.PlayButton.setObjectName("PlayButton")
        self.verticalLayout.addWidget(self.PlayButton)
        self.PlayButton.clicked.connect(self.run)

        # SQARE FRAME
        self.SqareFrame = QtWidgets.QFrame(self.centralwidget)
        self.SqareFrame.setGeometry(QtCore.QRect(180, 100, 300, 300))
        self.SqareFrame.setStyleSheet("")
        self.SqareFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SqareFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SqareFrame.setObjectName("SqareFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.SqareFrame)
        self.gridLayout.setObjectName("gridLayout")

        # ZOOM SLIDER
        self.ZoomSlider = QtWidgets.QSlider(self.LeftButtonFrame)
        self.ZoomSlider.setGeometry(QtCore.QRect(140, 180, 22, 160))
        self.ZoomSlider.setMaximum(100)
        self.ZoomSlider.setProperty("value", 50)
        self.ZoomSlider.setOrientation(QtCore.Qt.Vertical)
        self.ZoomSlider.setObjectName("ZoomSlider")
        self.ZoomSlider.valueChanged.connect(self.zoom)

        # SIZE SLIDER
        self.SizeSlider = QtWidgets.QSlider(self.LeftButtonFrame)
        self.SizeSlider.setGeometry(QtCore.QRect(75, 180, 22, 160))
        self.SizeSlider.setMaximum(20)
        self.SizeSlider.setMinimum(4)
        self.SizeSlider.setProperty("value", 4)
        self.SizeSlider.setOrientation(QtCore.Qt.Vertical)
        self.SizeSlider.setObjectName("SizeSlider")
        self.SizeSlider.sliderReleased.connect(lambda: self.generate_board(self.SizeSlider.value(), self.SizeSlider.value()))

        # PROGRAM BUTTON
        self.ProgramButton = QtWidgets.QPushButton(self.LeftButtonFrame)
        self.ProgramButton.setGeometry(QtCore.QRect(60, 70, 75, 31))
        self.ProgramButton.setObjectName("Program")
        self.ProgramButton.clicked.connect(self.open_ide)

        # PIXEL MAPS
        # Beepo
        self.pixelmap_B_x_x_x_x_n = QPixmap("imgs/N[B,x,x,x,x].png")
        self.pixelmap_B_x_x_x_x_o = QPixmap("imgs/O[B,x,x,x,x].png")
        self.pixelmap_B_x_x_x_x_s = QPixmap("imgs/S[B,x,x,x,x].png")
        self.pixelmap_B_x_x_x_x_w = QPixmap("imgs/W[B,x,x,x,x].png")
        # GEAR
        self.pixelmap_x_x_G_x_x = QPixmap("imgs/[x,x,G,x,x].png")
        # WALL
        self.pixelmap_x_W_x_x_x = QPixmap("imgs/[x,W,x,x,x].png")
        # BUTTON
        self.pixelmap_x_x_x_x_B_np = QPixmap("imgs/[x,x,x,x,B]np.png")
        self.pixelmap_x_x_x_x_B_p = QPixmap("imgs/[x,x,x,x,B]p.png")

        # SHIT
        self.SqareFrame.raise_()
        self.RightButtonFrame.raise_()
        self.LeftButtonFrame.raise_()
        self.TopButtonFrame.raise_()
        self.BottomButtonFrame.raise_()
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 919, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.BeepoButton.setText(_translate("MainWindow", "Beepo"))
        self.WallButton.setText(_translate("MainWindow", "Wall"))
        self.GearButton.setText(_translate("MainWindow", "Gear"))
        self.ButtonButton.setText(_translate("MainWindow", "Button"))
        self.DoorButton.setText(_translate("MainWindow", "Door"))
        self.PlayButton.setText(_translate("MainWindow", "Play"))
        self.ProgramButton.setText(_translate("MainWindow", "Program"))
        self.GearCounter.setText("Gears: 0")

    # creates a BOARD using LISTS inside LISTS which contain LISTS that contain information about what is on the square
    # the BOARD is stored in the GRID variable
    # calling a function to create a BUTTON for every square to display on the UI
    def generate_board(self, height, width):
        global grid
        for row_count, row in enumerate(grid):
            for column_count, column in enumerate(row):
                exec(f"self.square{row_count}_{column_count}.deleteLater()")
        grid = []
        for row in range(height):
            row_list = []
            for column in range(width):
                row_list.append(["x","x","x","x","x"])
            grid.append(row_list)

        for row in range(0, height):
            for column in range(0, width):
                self.generate_square(row, column)
        self.update()

    # CREATES a BUTTON for every square to display on the UI
    def generate_square(self, height, width):
        self.square = QPushButton(self.SqareFrame)
        self.gridLayout.addWidget(self.square, height, width, 1, 1)
        self.square.clicked.connect(lambda: self.place_piece(height, width))
        self.square.setObjectName(f"square{str(height)}_{str(width)}")
        setattr(Ui_MainWindow, f"square{str(height)}_{str(width)}", self.square)

    # RESIZES every BUTTON which displays a SQUARE on the ui
    def zoom(self, value):
        self.SqareFrame.resize(200+value*3,200+value*3)
        for row_count, row in enumerate(grid):
            for square_count, square in enumerate(row):
                exec(f'self.square{row_count}_{square_count}.setMinimumHeight(self.SqareFrame.height()//{grid_height});self.square{row_count}_{square_count}.setMinimumWidth(self.SqareFrame.width()//{grid_width})')
                exec(f'self.square{row_count}_{square_count}.setIconSize(self.square{row_count}_{square_count}.size())')

    # CREATES a new WINDOW (the IDE)
    def open_ide(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_IDE()
        self.ui.setupUi(self.window)
        self.window.show()

    # RUNS the CODE writen in the Compiled.py file
    def run(self):
        global sleep_time
        global error
        global gears_picked_up
        gears_picked_up = 0
        error = "Crash"
        try:
            exec(open("Compiled.py").read())
        except:
            self.error()


    # SPAWNS MESSAGEBOX
    def error(self):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText(error)
        error_box.setWindowTitle("Error")
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()

    # CREATES new PIXELMAP from two individual pixelmaps
    def combine_pixmap(self, pixmap1, pixmap2):
        print("combine")
        combined_pixmap = pixmap1.scaled(500, 500)  # Scale the pixmap to match the button size
        painter = QPainter(combined_pixmap)
        painter.drawPixmap(0, 0, pixmap2.scaled(500, 500))  # Scale the second pixmap and draw it on top of the first
        painter.end()
        return combined_pixmap

    # CHANGES the STATE of a SQUARE
    # Checks for BREAKING of GAME RULES before
    # TODO do not use exec / UNSAFE CODE / FIX LATER 
    # TODO use Switch and Case
    def set_square(self, y, x):
        global grid
        global beepo_rotation
        global grid_width
        global grid_height
        exec(f'self.square{y}_{x}.setMinimumHeight(self.SqareFrame.height()//{grid_height});self.square{y}_{x}.setMinimumWidth(self.SqareFrame.width()//{grid_width})')
        if grid[y][x][0] == "B":
            if grid[y][x][2] == "G":
                if beepo_rotation == "n":
                    exec(
                        f'self.square{y}_{x}.setIcon(QIcon(self.combine_pixmap(self.pixelmap_x_x_G_x_x, self.pixelmap_B_x_x_x_x_n)));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
                elif beepo_rotation == "o":
                    exec(
                        f'self.square{y}_{x}.setIcon(QIcon(self.combine_pixmap(self.pixelmap_x_x_G_x_x, self.pixelmap_B_x_x_x_x_o)));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
                elif beepo_rotation == "s":
                    exec(
                        f'self.square{y}_{x}.setIcon(QIcon(self.combine_pixmap(self.pixelmap_x_x_G_x_x, self.pixelmap_B_x_x_x_x_s)));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
                else:
                    exec(
                        f'self.square{y}_{x}.setIcon(QIcon(self.combine_pixmap(self.pixelmap_x_x_G_x_x, self.pixelmap_B_x_x_x_x_w)));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
            elif grid[y][x][4] == "B_np":
                if beepo_rotation == "n":
                    exec(
                        f'self.square{y}_{x}.setIcon(QIcon(self.combine_pixmap(self.pixelmap_x_x_x_x_B_np, self.pixelmap_B_x_x_x_x_n)));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
                elif beepo_rotation == "o":
                    exec(
                        f'self.square{y}_{x}.setIcon(QIcon(self.combine_pixmap(self.pixelmap_x_x_x_x_B_np, self.pixelmap_B_x_x_x_x_o)));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
                elif beepo_rotation == "s":
                    exec(
                        f'self.square{y}_{x}.setIcon(QIcon(self.combine_pixmap(self.pixelmap_x_x_x_x_B_np, self.pixelmap_B_x_x_x_x_s)));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
                else:
                    exec(
                        f'self.square{y}_{x}.setIcon(QIcon(self.combine_pixmap(self.pixelmap_x_x_x_x_B_np, self.pixelmap_B_x_x_x_x_w)));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')

            else:
                if beepo_rotation == "n":
                    exec(f'self.square{y}_{x}.setIcon(QIcon(self.pixelmap_B_x_x_x_x_n));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
                elif beepo_rotation == "o":
                    exec(f'self.square{y}_{x}.setIcon(QIcon(self.pixelmap_B_x_x_x_x_o));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
                elif beepo_rotation == "s":
                    exec(f'self.square{y}_{x}.setIcon(QIcon(self.pixelmap_B_x_x_x_x_s));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
                else:
                    exec(f'self.square{y}_{x}.setIcon(QIcon(self.pixelmap_B_x_x_x_x_w));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
        elif grid[y][x][2] == "G":
            exec(f'self.square{y}_{x}.setIcon(QIcon(self.pixelmap_x_x_G_x_x));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
        elif grid[y][x][4] == "B_np":
            exec(
                f'self.square{y}_{x}.setIcon(QIcon(self.pixelmap_x_x_x_x_B_np));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
        elif grid[y][x][4] == "B_p":
            exec(
                f'self.square{y}_{x}.setIcon(QIcon(self.pixelmap_x_x_x_x_B_p));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
        elif grid[y][x][1] == "W":
            exec(f'self.square{y}_{x}.setIcon(QIcon(self.pixelmap_x_W_x_x_x));self.square{y}_{x}.setIconSize(self.square{y}_{x}.size())')
        else:
            exec(f'self.square{y}_{x}.setIcon(QIcon(None))')

    # UPDATES EVERY SQUARE
    # UPDATES EVERY possibly changed VARIABLE
    # UPDATES the UI
    def update(self):
        global beepo_x
        global beepo_y
        global grid
        global gears_picked_up
        for row_count, row in enumerate(grid):
            for square_count, square in enumerate(row):
                self.set_square(row_count, square_count)
                QApplication.processEvents()
        self.GearCounter.setText(f"Gears: {gears_picked_up}")

    # UPDATES one SQUARE
    # UPDATES the UI
    def update_one_square(self, y, x):
        self.set_square(y, x)
        QApplication.processEvents()

    # UPDATES one VARIABLE
    def update_variables(self):
        self.GearCounter.setText(f"Gears: {gears_picked_up}")

    # CHANGES selected_piece
    def set_piece(self, piece):
        global selected_piece
        selected_piece = piece

    # PLACES the selected PIECE on pressed SQUAR
    # CHECKS for GAME RULES
    # TODO use Switch and Case
    def place_piece(self, y, x):
        global selected_piece
        global beepo_x
        global beepo_y
        if selected_piece == "B":            # TODO use Switch and Case
            grid[beepo_y][beepo_x][0] = "x"
            beepo_x = x
            beepo_y = y
            grid[y][x][1] = "x"
            grid[y][x][0] = "B"
            self.update()
        elif selected_piece == "W":
            if grid[y][x][1] == "W":
                grid[y][x][1] = "x"
            else:
                grid[y][x][0] = "x"
                grid[y][x][2] = "x"
                grid[y][x][3] = "x"
                grid[y][x][4] = "x"
                grid[y][x][1] = "W"
            self.update_one_square(y, x)
        elif selected_piece == "G":
            if grid[y][x][2] == "G":
                grid[y][x][2] = "x"
            else:
                grid[y][x][1] = "x"
                grid[y][x][3] = "x"
                grid[y][x][4] = "x"
                grid[y][x][2] = "G"
            self.update_one_square(y, x)
        elif selected_piece == "D":
            if grid[y][x][3] == "D":
                grid[y][x][3] = "x"
            else:
                grid[y][x][0] = "x"
                grid[y][x][1] = "x"
                grid[y][x][2] = "x"
                grid[y][x][4] = "x"
                grid[y][x][3] = "D"
            self.update_one_square(y, x)
        elif selected_piece == "B_np":
            if grid[y][x][4] == "B_np" or grid[y][x][4] == "B_p":
                grid[y][x][4] = "x"
            else:
                grid[y][x][2] = "x"
                grid[y][x][1] = "x"
                grid[y][x][4] = "B_np"
            self.update_one_square(y, x)

# BEEPO CLASS
# the robot that can be controlled by the user
class Robot:

    # MOVES ROBOT in the direction he is looking
    def move(self):
        global beepo_rotation
        global beepo_x
        global beepo_y
        global grid
        global error

        print("move", beepo_y, " ", beepo_x)
        if beepo_rotation == "n":
            if grid[beepo_y-1][beepo_x][1] == "W":
                error = "Beepo tried to run into a wall!"
                raise Exception
            grid[beepo_y][beepo_x][0] = "x"
            beepo_y -= 1
            grid[beepo_y][beepo_x][0] = "B"
            App.update()
        elif beepo_rotation == "o":
            if grid[beepo_y][beepo_x+1][1] == "W":
                error = "Beepo tried to run into a wall!"
                raise Exception
            grid[beepo_y][beepo_x][0] = "x"
            beepo_x += 1
            grid[beepo_y][beepo_x][0] = "B"
            App.update()
        elif beepo_rotation == "s":
            if grid[beepo_y+1][beepo_x][1] == "W":
                error = "Beepo tried to run into a wall!"
                raise Exception
            grid[beepo_y][beepo_x][0] = "x"
            beepo_y += 1
            grid[beepo_y][beepo_x][0] = "B"
            App.update()
        elif beepo_rotation == "w":
            if grid[beepo_y][beepo_x-1][1] == "W":
                error = "Beepo tried to run into a wall!"
                raise Exception
            grid[beepo_y][beepo_x][0] = "x"
            beepo_x -= 1
            grid[beepo_y][beepo_x][0] = "B"
            App.update()

    # TURNS ROBOT to the RIGHT by 90 degrees if no specific rotation is given
    def turn_right(self, i_rotation=1):
        global beepo_rotation
        if directions.index(beepo_rotation) + i_rotation > 3:
            beepo_rotation = directions[directions.index(beepo_rotation) + i_rotation - ((directions.index(beepo_rotation) + i_rotation)//4) * 4]
        else:
            beepo_rotation = directions[directions.index(beepo_rotation) + i_rotation]
        print(beepo_rotation)
        App.update()

    # TURNS ROBOT to the LEFT by 90 degrees if no specific rotation is given
    def turn_left(self, i_rotation=1):
        global beepo_rotation
        beepo_rotation = directions[directions.index(beepo_rotation) - i_rotation]
        print(beepo_rotation)
        App.update()

    # DELETES GEAR
    # CHANGES gears_picked_up by 1
    def pickup_gear(self):
        global gears_picked_up
        global error
        if grid[beepo_y][beepo_x][2] == "G":
            gears_picked_up += 1
            grid[beepo_y][beepo_x][2] = "x"
            App.update_variables()
            App.update()
        else:
            error = "tried to pick up gear with out standing on gear"
            raise Exception


    # CHANGES X and Y COORDINATES to given value
    def set_position(self, i_x, i_y):
        global beepo_x
        global beepo_y
        grid[beepo_y][beepo_x][0] = "x"
        beepo_x = i_x
        beepo_y = i_y
        grid[beepo_y][beepo_x][0] = "B"
        App.update()

    # CHANGES the robots ROTATION to given value
    def set_rotation(self, i_r):
        global beepo_rotation
        beepo_rotation = i_r
        App.update()

    # CHECKS if a WALL is in front  of the ROBOT
    def wall_front(self):
        global grid
        global beepo_x
        global beepo_y
        global beepo_rotation
        print("wall_front()")
        if beepo_rotation == "n":
            if grid[beepo_y-1][beepo_x][1] == "W":
                return True
        elif beepo_rotation == "o":
            if grid[beepo_y][beepo_x+1][1] == "W":
                return True
        elif beepo_rotation == "s":
            if grid[beepo_y+1][beepo_x][1] == "W":
                return True
        elif beepo_rotation == "w":
            if grid[beepo_y][beepo_x-1][1] == "W":
                return True

        return False

    # CHECKS if a WALL is on the LEFT of the ROBOT
    def wall_left(self):
        global grid
        global beepo_x
        global beepo_y
        global beepo_rotation
        # TODO use Switch and Case
        if beepo_rotation == "n":
            if grid[beepo_y][beepo_x-1][1] == "W":
                return True
        elif beepo_rotation == "o":
            if grid[beepo_y-1][beepo_x][1] == "W":
                return True
        elif beepo_rotation == "s":
            if grid[beepo_y][beepo_x+1][1] == "W":
                return True
        elif beepo_rotation == "w":
            if grid[beepo_y+1][beepo_x][1] == "W":
                return True
        else:
            return False

    # CHECKS if a WALL is on the RIGHT of the ROBOT
    def wall_right(self):
        global grid
        global beepo_x
        global beepo_y
        global beepo_rotation
        # TODO use Switch and Case
        if beepo_rotation == "n":
            if grid[beepo_y][beepo_x+1][1] == "W":
                return True
        elif beepo_rotation == "o":
            if grid[beepo_y+1][beepo_x][1] == "W":
                return True
        elif beepo_rotation == "s":
            if grid[beepo_y][beepo_x-1][1] == "W":
                return True
        elif beepo_rotation == "w":
            if grid[beepo_y-1][beepo_x][1] == "W":
                return True
        else:
            return False

    # CHECKS if the ROBOT is on a GEAR
    def on_gear(self):
        global grid
        global beepo_x
        global beepo_y
        if grid[beepo_y][beepo_x][2] == "G":
            return True
        else:
            return False

Beepo = Robot()

app = QApplication(sys.argv)
App = Ui_MainWindow()

App.generate_board(grid_height, grid_width)

App.show()
sys.exit(app.exec_())
