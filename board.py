from PyQt6.QtWidgets import QFrame, QLabel, QGridLayout, QPushButton, QSizePolicy, QApplication
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QSize
from PyQt6.QtGui import QPainter, QPen, QIcon
from PyQt6.uic.properties import QtGui
from PyQt6.uic.uiparser import QtWidgets

from piece import Piece

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7  #
    timerSpeed = 1000  # the timer updates every 1 millisecond
    counter = 10  # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)

        #  parent is go, board is declared in go file using self as parameter
        self.go = parent
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        self.piece = Piece(0, 0, 0)
        # board 7x7 has 8x8 pieces positions on it
        # TODO - create a 2d int/Piece array to store the state of the game
        # initializing array
        self.boardArray = [[self.piece for cell in range(8)]for row in range(8)]
        self.printBoardArray()

        self.grid = QGridLayout()
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                piece1 = Piece(0, row, col)
                # piece1.setSizePolicy(QSizePolicy.Polic)
                self.grid.addWidget(piece1, row, col)  # adding piece to the equivalent position in the grid
                self.boardArray[row][col] = piece1  # adding piece to the right position


        # add layout with right pieces
        self.setLayout(self.grid)
        # print board again to check if pieces are right based on its x and y
        self.printBoardArray()

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        # print value of piece (0, 1 or 2)
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell.getPiece()) for cell in row]) for row in self.boardArray]))

        # printing x and y of each piece (it index)
        print("boardArray x and y:")
        print('\n'.join(['\t'.join([str(cell.get_x_and_y()) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            # self.counter -= 1
            # print('timerEvent()', self.counter)
            # self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        # self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location [" + str(event.position().x()) + "," + str(
            event.position().y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)
        self.printBoardArray()

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    # drawBoardSaqueres will be changed
    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # TODO set the default colour of the brush
        # painter.setPen(QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine))  will be used to do a the board in a different way

        painter.setBrush(Qt.GlobalColor.darkYellow)
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth() * col  # TODO set this value equal the transformation in the column direction
                rowTransformation = self.squareHeight() * row  # TODO set this value equal the transformation in the row direction
                painter.translate(colTransformation, rowTransformation)
                # if col == 0:
                #     painter.setBrush(Qt.GlobalColor.blue)
                #     painter.fillRect(row, col, int(self.squareWidth()), int(self.squareHeight()),
                #                      painter.brush())
                painter.fillRect(row, col, int(self.squareWidth()), int(self.squareHeight()),
                                 painter.brush())  # TODO provide the required arguments
                painter.restore()
                if painter.brush() == Qt.GlobalColor.darkYellow:
                    painter.setBrush(Qt.GlobalColor.black)
                else:
                    painter.setBrush(Qt.GlobalColor.darkYellow)

                # TODO change the colour of the brush so that a checkered board is drawn

    #  Probably will be deleted as grid take care of this job
    # def drawPieces(self, painter):
    #     '''draw the prices on the board'''
    #     colour = Qt.GlobalColor.transparent  # empty square could be modeled with transparent pieces
    #     for row in range(0, len(self.boardArray)):
    #         for col in range(0, len(self.boardArray[0])):
    #             painter.save()
    # x and y position,
    #             painter.translate()
    #
    #             # TODO draw some the pieces as ellipses
    #             # TODO choose your colour and set the painter brush to the correct colour
    #             radius = self.squareWidth() / 4
    #             center = QPointF(radius, radius)
    #             painter.drawEllipse(center, radius, radius)
    #             painter.restore()

    def resizeEvent(self, event):

        print(f"height: {self.height()}, wight: {self.width()}")
        print(f"Butom height: {self.piece.height()}, wight: {self.piece.width()}")

        # self.setFixedSize(self.go.width(), self.go.height())

        # self.update()

        # top = 200 - self.squareHeight()/2

        # self.grid.setContentsMargins(20, top, 20, 20)



