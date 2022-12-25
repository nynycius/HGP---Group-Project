from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard

class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
<<<<<<< HEAD
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        self.resize(800, 800)
=======

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.board = Board(self)
        self.scoreBoard = ScoreBoard()
        # self.setCentralWidget(self.board)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        #  TODO maybe not necessary, setting scoreBoard and board inside a main layout
        central_widget_layout = QHBoxLayout(central_widget)
        central_widget_layout.addWidget(self.board, 9)
        central_widget_layout.addWidget(self.scoreBoard, 2)

        # set min siz based on screen size
        screen = self.screen().availableGeometry()

        #  min size is half of screeen size
        self.setMinimumSize(int(screen.width() * 0.5), int(screen.height() * 0.5))

>>>>>>> 54dc38efff70c8075d58f81e409720057bf97d2e
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        #size = self.geometry()
        #self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)
