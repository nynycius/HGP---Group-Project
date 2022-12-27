from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QPushButton, QSizePolicy, QApplication


# TODO: Add more functions as needed for your Pieces
class Piece(QPushButton):
    NoPiece = 0
    White = 1
    Black = 2
    Status = 0 # default to nopiece
    liberties = 0 # default no liberties
    x = -1
    y = -1
    icon = QIcon()
    def __init__(self, board, x, y):  #constructor
        super().__init__()
        self.Status = 0
        self.liberties = 0  # starting with 0 liberty as default, must set right liberty when placed
        self.x = x
        self.y = y
        #  comment out the next line to see button border
        self.setStyleSheet("background-color: rgba(255,255,255,0);border: 0px; padding: 0px")  # background and border transparent
        self.setIcon(QIcon("./icons/blank.png"))  # must be changed to blank.png
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pressed.connect(self.piece_color)

        # create a board instance to verifiy turn
        self.board = board



    # Small test to change the icons, must be changed based on players turn if Status == 0 (blank) only
    def piece_color(self):

        print(f"pressed: {self.getPiece()}, x and y: {self.get_x_and_y()}")
        # if piece is in a given state change to the next one
        # if the piece is blank it is allowed to change
        if self.Status == 0:
            # change the button color based on how player is playing
            if self.board.clicker() % 2 == 0:
                self.setIcon(QIcon("./icons/black.png"))
                self.Status = 1

            else:
                self.setIcon(QIcon("./icons/white.png"))
                self.Status = 2

            # print board state after each play
            self.board.printBoardArray()

    def getPiece(self):# return piece value
        return self.Status

    def getLiberties(self): # return Liberties
        self.libs = self.liberties
        return self.libs

    def setLiberties(self, liberties):  # set Liberties
        self.liberties = liberties

    # used to set the right position of the piece in the board
    def set_x_and_y(self, x, y):
        self.x = x
        self.y = y

    def get_x_and_y(self):
        return self.x, self.y

    def resizeEvent(self, event):  # guarantee that icon resizes based on the button size

        self.setIconSize(QSize(self.height(), self.width()))

