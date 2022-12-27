from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QDockWidget, QMessageBox
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("./icons/go.png"))
        self.board = Board(self)
        self.scoreBoard = ScoreBoard()
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''

        menu_bar = self.menuBar()  # create a menu bar
        menu_bar.setNativeMenuBar(True)
        #  create rule option and populate
        rules = menu_bar.addMenu("Rules")

        # basic rules
        basic_rules_action = QAction(QIcon("./icons/basic.png"), "Basic Rules", self)
        basic_rules_action.setShortcut("ctrl+b")
        rules.addAction(basic_rules_action)  # add to the bar
        basic_rules_action.triggered.connect(self.rules)

        # suicide rule
        suicide_rule_action = QAction(QIcon("./icons/suicide.png"), "Suicide Rule", self)
        suicide_rule_action.setShortcut("ctrl+s")
        rules.addAction(suicide_rule_action)
        suicide_rule_action.triggered.connect(self.suicide)

        # Ko rule
        KO_rule_action = QAction(QIcon("./icons/KO.png"), "Ko Rules", self)
        KO_rule_action.setShortcut("ctrl+k")
        rules.addAction(KO_rule_action)
        KO_rule_action.triggered.connect(self.KO)

        main_widget = QWidget()

        self.setCentralWidget(main_widget)

        self.scoreBoard.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        self.setStyleSheet("background-color: #F7F1ED")

        layout = QHBoxLayout(main_widget)
        layout.addWidget(self.board)
        layout.addWidget(self.scoreBoard)

        self.scoreBoard.make_connection(self.board)

        screen = self.screen().availableGeometry()

        self.setMinimumWidth(int(screen.width() * 0.8))
        self.setMinimumHeight(int(screen.height() * 0.88))

        self.setWindowTitle('Go')
        self.show()

        # -------------Game Logic-----------
        self.scoreBoard.skip_button.clicked.connect(self.board.skip)
        self.scoreBoard.reset_button.clicked.connect(self.board.resetGame)

    #  display basic rules
    def rules(self):
        msg = QMessageBox(
            text="Basic Rules\n"
                 "\nA game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces "
                 "(called stones), one taking the black stones, the other taking white. \nThe main object of the game is "
                 "to use your stones to form territories by surrounding vacant areas of the board. It is also possible "
                 "to capture your opponent's stones by completely surrounding them. \nPlayers take turns, placing one of "
                 "their stones on a vacant point at each turn, with Black playing first. \n*Note that stones are placed on"
                 " the intersections of the lines rather than in the squares and once played stones are not moved. "
                 "\nHowever they may be captured, in which case they are removed from the board, and kept by the capturing "
                 "player as prisoners",
            parent=self)
        # button to clog messagebox
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg.show()

    # display suicide rules
    def suicide(self):
        msg = QMessageBox(text="Suicide Rule\n"
                               "\nA player cannot place a stone between their opponent one, in a position that"
                               " it would cause a self capture", parent=self)
        # button to clog messagebox
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg.show()

    # display KO rule
    def KO(self):
        msg = QMessageBox(text="KO Rule \n"
                               "\nIt is forbidden to capture a stone that just capture another one, causing a game to "
                               "going on endlessly."
                               "\nIn other words, a player cannot play two consecutive turns in the same position", parent=self)
        # button to clog messagebox
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)
        msg.show()

