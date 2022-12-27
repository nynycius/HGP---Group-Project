from PyQt6.QtWidgets import QFrame, QLabel, QGridLayout, QPushButton, QSizePolicy, QApplication, QMessageBox, QApplication
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QSize
from PyQt6.QtGui import QPainter, QPen, QIcon
from PyQt6.uic.properties import QtGui
from PyQt6.uic.uiparser import QtWidgets

from piece import Piece


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    updatePlayer1ScoreSignal = pyqtSignal(int)
    updatePlayer2ScoreSignal = pyqtSignal(int)



    # TODO set the board width and height to be square
    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7  #

    timerSpeed = 1000  # the timer updates every 1 millisecond

    counter = 10  # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)

        #  parent is go, board is declared in go file using self as parameter
        self.go = parent

        self.timer = QBasicTimer()  # create a timer for the game

        self.isStarted = False  # game is not currently started

        self.setStyleSheet("background-color: #CD950C;")

        self.setContentsMargins(0, 0, 0, 0)

        self.turn_counter = 1

        # self.piece = Piece(Piece.NoPiece, 0, 0)

        self.boardArray = [[0 for cell in range(self.boardWidth)] for row in range(self.boardHeight)]

        self.piecesArray = []

        self.printBoardArray()

        self.grid = QGridLayout()

        self.grid.setSpacing(0)

        # keeps track of number of count's in a row
        self.skip_count = 0

        self.player1Score = 0

        self.player2Score = 0


        self.initBoard()

    def initBoard(self):
        '''initiates board'''

        self.start()  # start the game which will start the timer

        # board 7x7 has 6x6 squares
        # TODO - create a 2d int/Piece array to store the state of the game
        # initializing array

        # self.printBoardArray()

        for row in range(self.boardWidth):
            pieces_row = []
            for col in range(self.boardHeight):
                piece = Piece(self, row, col)
                pieces_row.append(piece)
                self.grid.addWidget(piece, row, col)  # adding piece to the equivalent position in the grid

            # add piece rows to pieces array
            self.piecesArray.append(pieces_row)

        # add layout with right pieces
        self.setLayout(self.grid)
        # print board again to check if pieces are right based on its x and y
        self.printBoardArray()

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        # print value of piece (0, 1 or 2)
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell.getPiece()) for cell in row]) for row in self.piecesArray]))

        # printing x and y of each piece (it index)
        print("boardArray x and y:")
        print('\n'.join(['\t'.join([str(cell.get_x_and_y()) for cell in row]) for row in self.piecesArray]))

    def squareWidth(self):
        '''returns the width of one square in the board'''
        # return as int to make work easier with the other methods
        return int(self.contentsRect().width() / (self.boardWidth + 1))

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return int(self.contentsRect().height() / (self.boardHeight + 1))

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        # self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
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
        for row in self.piecesArray:
            for p in row:
                p.setPiece(0)
                p.setLiberties(0)

        self.turn_counter = 1


    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    # drawBoardSaqueres will be changed
    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # TODO set the default colour of the brush

        painter.setPen(QPen(Qt.GlobalColor.black, 3, Qt.PenStyle.SolidLine))

        #  take the square size to calculate drawn position
        square_width = self.squareWidth()

        initial_position = square_width

        final_position = square_width * self.boardWidth

        for i in range(1, self.boardWidth + 1):
            # determine the position of the line
            position = square_width * i

            #  row
            painter.drawLine(initial_position, position, final_position, position)
            #  colum
            painter.drawLine(position, initial_position, position, final_position)

    def resizeEvent(self, event):
        # print(f"height: {self.height()}, wight: {self.width()}")
        # print(f"Butom height: {self.piece.height()}, wight: {self.piece.width()}")
        self.setFixedWidth(self.height())

        top = int(self.squareHeight() * 0.5)
        bottom = int(self.squareWidth() * 0.5)
        left = int(self.squareHeight() * 0.5)
        right = int(self.squareWidth() * 0.5)

        self.grid.setContentsMargins(top, left, right, bottom)

    # increment the turn_counter every time a stone is positioned
    def clicker(self):
        self.turn_counter += 1

        # reset skip count to zero
        self.skip_count = 0

        return self.turn_counter

    def skip(self):
        # on skip increment counter to move to the next turn
        self.turn_counter += 1

        # if skip occurs twice in a row
        if(self.skip_count == 1):
            skip_message = QMessageBox.question(self, "Game Over", "Game is over, Restart?")
            # if response is yes reset game
            if skip_message == skip_message.Yes:
                self.resetGame()
            # if response is no quit game
            else:
                QApplication.quit()
        # increment skip count on each skip click
        self.skip_count += 1

        # if black skipped add one two score of white as piece is given to white
        if self.turn_counter % 2 == 0:
            self.player2Score += 1
            print(self.player2Score)
            self.updatePlayer2ScoreSignal.emit(self.player2Score)
        # if white skipped add one two score of white as piece is given to white
        else:
            self.player1Score += 1
            print(self.player1Score)
            self.updatePlayer1ScoreSignal.emit(self.player1Score)





