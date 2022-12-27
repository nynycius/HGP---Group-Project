from builtins import len, print

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QPushButton, QSizePolicy, QApplication


# TODO: Add more functions as needed for your Pieces
class Piece(QPushButton):
    # NoPiece = 0
    # White = 1
    # Black = 2
    # status = 0  # default to nopiece
    # liberties = 0  # default no liberties
    # x = -1
    # y = -1
    # icon = QIcon()
    black_move = []
    white_move = []

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

        # create a board instance to verify turn
        self.board = board

        #   list for liberties
        self.adjacentPiece = []
        self.adjacentLiberties = []

        # variable to keep track on player last move for KO rule


    # Small test to change the icons, must be changed based on players turn if Status == 0 (blank) only
    def piece_color(self):

        # if the movement is not a self capture, stone can be placed, also check if a capture can be made
        if self.suicide(self.getAdjacentPieces(), self.captureSinglePiece(self.getOpponentPiece())):
            # if piece is in a given state change to the next one
            # if the piece is blank it is allowed to change
            if self.status == 0:
                # change the button color based on how player is playing
                if self.board.clicker() % 2 == 0:  # only change turn when piece can be placed
                    self.setIcon(QIcon("./icons/black.png"))
                    self.status = 1
                    #  check if move is not equal to last move
                    self.KO(self.get_x_and_y())
                    # if movement is different store new move
                    self.black_move.append(self.get_x_and_y())

                else:
                    self.setIcon(QIcon("./icons/white.png"))
                    self.status = 2
                    #  check if move is not equal to last move
                    self.KO(self.get_x_and_y())
                     # if movement is different store new move
                    self.white_move.append(self.get_x_and_y())


            # print("black", self.black_move)
            # print("white", self.white_move)
            # print(f"pressed: {self.getPiece()}, x and y: {self.get_x_and_y()}")
         #   print(self.getAdjacentPieces())
            for adjacent in self.adjacentPiece:
                print(str(adjacent.get_x_and_y()), adjacent.getLiberties())
            print("Amount of enemies around", len(self.getOpponentPiece()))
            self.captureSinglePiece(self.getOpponentPiece())

    def getPiece(self):  # return PieceType
        return self.status

    def setPiece(self, p):
        self.status = p
        self.liberties = 0
        self.setIcon(QIcon("./icons/blank.png"))

    def getLiberties(self):  # return Liberties
        self.liberties = 0
        for adjacent_piece in self.adjacentPiece:
            if adjacent_piece.getPiece() > 0:
                self.liberties += 1
        return self.liberties

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

    def getAdjacentPieces(self):
        # creating list to store adjacent values
        self.adjacentPiece = []

        # creating reference to board piece Array
        pieces_arr = self.board.piecesArray

        #  creating reference of x and y form the current piece being placed
        x = self.x
        y = self.y

        #  if one of the conditions bellows happens, them the index is out of boundaries,
        if y + 1 != len(pieces_arr):
            self.adjacentPiece.append(pieces_arr[self.x][self.y + 1])
        if x + 1 != len(pieces_arr):
            self.adjacentPiece.append(pieces_arr[self.x + 1][self.y])

        if y - 1 != -1:
            self.adjacentPiece.append(pieces_arr[self.x][self.y - 1])

        if x - 1 != -1:
            self.adjacentPiece.append(pieces_arr[self.x - 1][self.y])

        return self.adjacentPiece

    def suicide(self, adjacent, capture):  # pass list of adjacent positions to check movement is valid

        #  set dataStructure doesn't allow repetitive values, so if it len equals to 1, all elements are the same
        same_values = 0
        adjacent_len = len(adjacent)
        if capture:
            return True
        for i in range(adjacent_len):
            # check if all values are the same
            if adjacent[0].getPiece() == adjacent[i].getPiece():
                same_values += 1

        turn = self.board.turn_counter % 2
        #  if the same_values are equals to the length of adjacent, them all values are the same
        if same_values == adjacent_len:
            # if all elements are the same, check if it is 0, 1 or 2
            if (adjacent[0].getPiece() == 0
                    or adjacent[0].getPiece() == 1 and turn == 1
                    or adjacent[0].getPiece() == 2 and turn == 0):
                # if it is 0 the position is valid
                return True
            #  else, the movement is invalid return false
            else:
                print(f"{str(self.get_x_and_y())} The movement is not valid, self capture detected ")
                return False
        else:
            return True

    def getOpponentPiece(self):
        # if self.status == 0:
            # raise Exception("This piece is empty")
        # store opponents in a list
        opponent = []
        # take all pieces adjacent to the current one
        for adjacent in self.adjacentPiece:
            if adjacent.getPiece() != 0 and adjacent.getPiece != self.status:
                    opponent.append(adjacent)

        return opponent


    def captureSinglePiece(self, opponent):

        surrounded_by_enemies = False

        # for i in opponent:
        #     print(f"opponents around: {i.get_x_and_y()}")
        # if there is more than one enemy around, check both
        for i in opponent:
            enemies_around = 0
            piece = i
            # print("target opponet", piece.get_x_and_y())
            # print("adjacent pieces", len(piece.getAdjacentPieces()))
            for a in piece.getAdjacentPieces():
                # print(f"Oponents {a.get_x_and_y()}, value {a.getPiece()}")
                if a.getPiece() != piece.getPiece() and a.getPiece() != 0:
                    enemies_around += 1
                    # print("enemies around:", enemies_around)

            # Check if enemies surrounding match to the size os the adjacent spaces
            if enemies_around == len(piece.getAdjacentPieces()):
                surrounded_by_enemies = True
                # print("enemies around:", enemies_around)

            # if the is true and the same size of the adjacent pieces erase piece
            if surrounded_by_enemies and piece.liberties == len(piece.getAdjacentPieces()):
                piece.setPiece(0)
                # print(f"captured {piece.get_x_and_y()}")
                # set surrounded_by_enemies to false again for the next interation
                return True
    def KO(self, move):  # not working properly

        # printing for debug
        # print(">>>>> checking move <<<")
        # print(f"last move, black: {self.black_move}, white {self.white_move}"
        #       f"\n new move: {move}")
        if move == self.black_move or move == self.white_move:
            #  print for debbug
            # print(">>>>>> GOT IN <<<<")
            # if the move are the same, decrement turn and erase last move
            self.board.turn_counter -= 1
            self.setPiece(0)
            # printing for debug
            # print(f"last move, black: {self.black_move[-1]}, white {self.white_move[-1]}"
            #       f"\n new move: {move}")


