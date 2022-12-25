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

    def __init__(self, Piece, x, y):  #constructor
        super().__init__()
        self.Status = Piece
        self.liberties = 0  # starting with 0 liberty as default, must set right liberty when placed
        self.x = x
        self.y = y
        #  comment out the next line to see button border
        # self.setStyleSheet("background-color: rgba(255,255,255,0);border: 0px; padding: 0px")  # background and border transparent
        # self.setIcon(QIcon("./icons/white.png"))  # must be changed to blank.png
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pressed.connect(self.piece_color)

    # Small test to change the icons, must be changed based on players turn if Status == 0 (blank) only
    def piece_color(self):

        print("pressed: ", self.getPiece())
        # if piece is in a given state change to the next one
        if self.getPiece() == 0:
            self.setIcon(QIcon("./icons/black.png"))
            self.Status = 1

        elif self.getPiece() == 1:
            self.setIcon(QIcon("./icons/white.png"))
            self.Status = 2

        elif self.getPiece() == 2:
            self.setIcon(QIcon("./icons/blank.png"))
            self.Status = 0

    def getPiece(self): # return PieceType
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

    def resizeEvent(self, event):

        self.setIconSize(QSize(self.height(), self.width()))

