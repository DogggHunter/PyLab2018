from gui import *
import random

tile_colors = {'9': "background-color: rgb(237, 224, 200);",
               '27': "background-color: rgb(242, 177, 121);",
               '81': "background-color: rgb(245, 149, 99);",
               '243': "background-color: rgb(246, 124, 95);",
               '729': "background-color: rgb(246, 94, 59);",
               '2187': "background-color: rgb(237, 207, 114);",
               '6561': "background-color: rgb(237, 204, 97);",
               '19683': "background-color: rgb(237, 200, 80);",
               '59049': "background-color: rgb(237, 197, 63);",
               '177147': "background-color: rgb(237, 194, 46);"}


class TileWidget(QtWidgets.QLabel):
    def __init__(self, parent=None, _score=None, _tiles=None, _x=0, _y=0, _step=2):
        QtWidgets.QLabel.__init__(self, parent=parent)

        self.score = _score
        self.tiles = _tiles

        self.anim = QtCore.QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(10)

        self.matrix_x = _x
        self.matrix_y = _y
        self.step = _step

    def can_move(self, next_tiles, mod, identical, x, y, with_move):
        """
        :param next_tiles: list of tiles that go after the current tile in the chosen direction.
        :param mod: used to determine the direction of movement of the tile in matrix and UI grid. -1 for move_down()
        and move_right(), 1 for move_up() and move_left(). -1 means that tile move on 1 cell down or right and 1 means
        that tile move on 1 cell up or left.
        :param identical: used to determine the existence of 4 identical tiles in a column or row.
        :param x: used to move on x coordinate in matrix and y coordinate in UI grid.
        :param y: used to move on y coordinate in matrix and x coordinate in UI grid.
        :param with_move: used for determination of necessity of moving of tiles.
        """

        can_move = False
        for next_tile in next_tiles:
            if next_tile:
                if int(self.text()) == int(next_tile.text()):
                    if with_move:
                        next_tile.setText(str(3 ** int(self.step)))

                        if int(next_tile.text()) == 177147:
                            self.show_end_message('win')

                        self.score.setText(str(int(self.score.text()) + int(next_tile.text())))
                        next_tile.step += 1
                        color = ""
                        if int(next_tile.text()) > 9:
                            color = "color: white;"
                        next_tile.setStyleSheet(next_tile.styleSheet() + tile_colors[next_tile.text()] + color)
                        self.tiles[self.matrix_x][self.matrix_y] = 0
                        self.deleteLater()
                    return True
                else:
                    return any([False, can_move])
            elif not identical:
                can_move = True
                if with_move:
                    self.anim.setStartValue(QtCore.QRect(self.geometry()))
                    self.anim.setEndValue(QtCore.QRect(self.x() - (110 * (mod * y)), self.y() - (100 * (mod * x)), 100, 90))
                    self.anim.start()
                    self.move(self.x() - (110 * (mod * y)), self.y() - (100 * (mod * x)))
                    self.tiles[self.matrix_x][self.matrix_y] = 0
                    self.matrix_y -= 1 * mod * y
                    self.matrix_x -= 1 * mod * x
                    self.tiles[self.matrix_x][self.matrix_y] = self
        return True

    def move_up(self, identical, with_move):
        if self.y() == 10:
            return False
        else:
            next_tiles = reversed(list(zip(*self.tiles))[self.matrix_y][:self.matrix_x])
            return self.can_move(next_tiles, 1, identical, 1, 0, with_move)

    def move_down(self, identical, with_move):
        if self.y() == 310:
            return False
        else:
            next_tiles = list(zip(*self.tiles))[self.matrix_y][self.matrix_x + 1:]
            return self.can_move(next_tiles, -1, identical, 1, 0, with_move)

    def move_right(self, identical, with_move):
        if self.x() == 340:
            return False
        else:
            next_tiles = self.tiles[self.matrix_x][self.matrix_y + 1:]
            return self.can_move(next_tiles, -1, identical, 0, 1, with_move)

    def move_left(self, identical, with_move):
        if self.x() == 10:
            return False
        else:
            next_tiles = reversed(self.tiles[self.matrix_x][:self.matrix_y])
            return self.can_move(next_tiles, 1, identical, 0, 1, with_move)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)

        self.end_game = False
        self.msg = None
        self.tiles = [[0 for _ in range(4)] for _ in range(4)]

        self.new_game_button.clicked.connect(self.start_new_game)

    def key_release(self, e, check_all=False, with_move=True):
        step = []
        if e.key() == QtCore.Qt.Key_Down or check_all:
            for col in zip(*self.tiles):
                identical = len(list((filter(None, col)))) == 4 \
                            and all(map(lambda elem: elem.text() == col[0].text(), col))
                for tile in list(filter(None, col))[::-1]:
                    step.append(tile.move_down(identical, with_move))
        if e.key() == QtCore.Qt.Key_Right or check_all:
            for row in self.tiles:
                identical = len(list((filter(None, row)))) == 4 \
                            and all(map(lambda elem: elem.text() == row[0].text(), row))
                for tile in list(filter(None, row))[::-1]:
                    step.append(tile.move_right(identical, with_move))
        if e.key() == QtCore.Qt.Key_Left or check_all:
            for row in self.tiles:
                identical = len(list((filter(None, row)))) == 4 \
                            and all(map(lambda elem: elem.text() == row[0].text(), row))
                for tile in list(filter(None, row)):
                    step.append(tile.move_left(identical, with_move))
        if e.key() == QtCore.Qt.Key_Up or check_all:
            for col in zip(*self.tiles):
                identical = len(list((filter(None, col)))) == 4 \
                            and all(map(lambda elem: elem.text() == col[0].text(), col))
                for tile in filter(None, col):
                    step.append(tile.move_up(identical, with_move))
        return step

    def keyReleaseEvent(self, e):
        if not e.isAutoRepeat():
            if self.end_game:
                return

        step = self.key_release(e)

        if any(step):
            self.add_new_tile()
        elif len(step) != 0:
            if not any(self.key_release(e, True, False)):
                self.show_end_message('lose')

    def show_end_message(self, _type):
        text = ""
        if _type == 'lose':
            text = "Unfortunately you lose, try again."
        elif _type == 'win':
            text = "Congratulations, you have reached tile 177147!!!"

        self.end_game = True
        self.msg = QtWidgets.QMessageBox(self)
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText(text)
        self.msg.setWindowTitle("Information window")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.show()

    def start_new_game(self):
        self.score.setText('0')
        for row in self.tiles:
            for tile in filter(None, row):
                self.tiles[tile.matrix_x][tile.matrix_y] = 0
                tile.deleteLater()
        self.initialize_game()
        self.end_game = False

    def add_new_tile(self):
        # check empty cells and random choice for add tile to this position
        empty_cells = [(x, y) for x in range(4) for y in range(4) if self.tiles[x][y] == 0]
        cell = empty_cells[random.randint(0, len(empty_cells) - 1)]

        if not empty_cells:
            return

        step = 2
        tile_weight = 3
        background_color = "background-color: rgb(238, 228, 218);"

        if random.random() > 0.9090909:
            step = 3
            tile_weight = 9
            background_color = "background-color: rgb(237, 224, 200);"

        tile = TileWidget(self.game_frame, self.score, self.tiles, cell[0], cell[1], step)
        tile.setGeometry(QtCore.QRect(cell[1]*110+10, cell[0]*100+10, 100, 90))
        tile.setMaximumSize(QtCore.QSize(100, 90))

        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(26)
        tile.setFont(font)
        tile.setStyleSheet(background_color + "color: rgb(119, 110, 101);")
        tile.setText(str(tile_weight))
        tile.setAlignment(QtCore.Qt.AlignCenter)
        tile.show()

        self.tiles[cell[0]][cell[1]] = tile

    def initialize_game(self):
        for _ in range(2):
            self.add_new_tile()


