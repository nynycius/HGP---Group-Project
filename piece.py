from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QPushButton, QSizePolicy, QApplication


# TODO: Add more functions as needed for your Pieces
class Piece(QPushButton):
    NoPiece = 0
    White = 1
    Black = 2
    status = 0  # default to nopiece
    liberties = 0  # default no liberties
    x = -1
    y = -1
    icon = QIcon()

    def __init__(self, board, x, y):  # constructor
        super().__init__()
        self.status = 0
        self.liberties = 0  # starting with 0 liberty as default, must set right liberty when placed
        self.x = x
        self.y = y
        #  comment out the next line to see button border
        self.setStyleSheet(
            "background-color: rgba(255,255,255,0);border: 0px; padding: 0px")  # background and border transparent
        self.setIcon(QIcon("./icons/blank.png"))  # must be changed to blank.png
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pressed.connect(self.piece_color)

        self.board = board

        self.adjacentPiece = []

    # Small test to change the icons, must be changed based on players turn if Status == 0 (blank) only
    def piece_color(self):
        #
        # self.board.player
        print(f"pressed: {self.getPiece()}, x and y: {self.get_x_and_y()}")
        # if piece is in a given state change to the next one

        # if the piece is blank it is allowed to change
        if self.status == 0:
            if self.board.clicker() % 2 == 0:
                self.setIcon(QIcon("./icons/black.png"))
                self.status = 1
                self.board.printBoardArray()


            else:
                self.setIcon(QIcon("./icons/white.png"))
                self.status = 2

        print(self.getAdjacentPieces())

    def getPiece(self):  # return PieceType
        return self.status

    def setPiece(self, p):
        self.status = p
        self.setIcon(QIcon("./icons/blank.png"))

    def getLiberties(self):  # return Liberties
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

    def getAdjacentPieces(self):
        self.adjacentPiece = []
        pieces_arr = self.board.piecesArray
        if 0 <= self.x < len(pieces_arr)-1 and 0 <= self.y < len(pieces_arr)-1:
            self.adjacentPiece.append(pieces_arr[self.x][self.y + 1].getPiece())
            self.adjacentPiece.append(pieces_arr[self.x + 1][self.y].getPiece())
            self.adjacentPiece.append(pieces_arr[self.x][self.y - 1].getPiece())
            self.adjacentPiece.append(pieces_arr[self.x - 1][self.y].getPiece())

        return self.adjacentPiece
