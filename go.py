from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QDockWidget
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard

class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.board = Board(self)
        self.scoreBoard = ScoreBoard()
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''

        main_widget = QWidget()

        self.setCentralWidget(main_widget)

        self.scoreBoard.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        self.setStyleSheet("background-color: #F7F1ED")

        layout = QHBoxLayout(main_widget)
        layout.addWidget(self.board)
        layout.addWidget(self.scoreBoard)

        self.scoreBoard.make_connection(self.board)

        screen = self.screen().availableGeometry()

        self.setMinimumWidth(int(screen.width()*0.8))
        self.setMinimumHeight(int(screen.height() * 0.88))

        self.setWindowTitle('Go')
        self.show()

        # -------------Game Logic-----------
        self.scoreBoard.skip_button.clicked.connect(self.board.skip)
        self.scoreBoard.reset_button.clicked.connect(self.board.resetGame)

