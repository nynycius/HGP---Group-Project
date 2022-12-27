from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, \
    QLabel, QPushButton  # TODO import additional Widget classes as desired
from PyQt6.QtCore import pyqtSlot


class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''


    def __init__(self):
        super().__init__()
        self.blackScore = 0
        self.whiteScore = 0
        self.turn = ""
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.setStyleSheet("background-color: #E1BF6D;"
                           "font-family: Arial;"
                           "font-size: 14px;")
        self.setFixedWidth(300)

        self.setWindowTitle('ScoreBoard')

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # create two labels which will be updated by signals
        self.label_turn = QLabel("Player1")
        self.label_pl1_score = QLabel("0")
        self.label_pl2_score = QLabel("0")

        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(QLabel("Turn: "))
        self.mainLayout.addWidget(self.label_turn)
        self.mainLayout.addWidget(QLabel("Player One's Score: "))
        self.mainLayout.addWidget(self.label_pl1_score)
        self.mainLayout.addWidget(QLabel("Player Two's Score: "))
        self.mainLayout.addWidget(self.label_pl2_score)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)

        # create skip button
        self.skip_button = QPushButton("Skip")
        self.mainLayout.addWidget(self.skip_button)

        self.reset_button = QPushButton("Reset")
        self.mainLayout.addWidget(self.reset_button)


        self.setWidget(self.mainWidget)
        self.show()


    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

        board.updatePlayer1ScoreSignal.connect(self.setBlackScore)
        board.updatePlayer2ScoreSignal.connect(self.setWhiteScore)


    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining:" + str(timeRemainng)
        self.label_timeRemaining.setText(update)
        print('slot ' + update)
        # self.redraw()

    def getBlackScore(self):
        return self.blackScore

    def setBlackScore(self, score):
        self.label_pl1_score.setText(str(score))


    def getWhiteScore(self):
        return self.whiteScore

    def setWhiteScore(self, score):
        self.label_pl2_score.setText(str(score))
