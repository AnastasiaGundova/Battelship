import random
import copy


class BoardOutException(Exception):
    pass


class BlockCoordinate(Exception):
    pass


class SamePointException(Exception):
    pass


class GameEnd(Exception):
    pass


class CouldntPlaceShip(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x  # row
        self.y = y  # column

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, length, start_point, direction):
        self.length = length
        self.start_point = start_point
        self.direction = direction
        self.hp = self.length

    def dots(self):
        dots_list = []
        for item in range(self.length):
            if self.direction == "vertical":
                ship_coordinates = Dot(self.start_point.x, self.start_point.y + item)
                dots_list.append(ship_coordinates)
            elif self.direction == "horizontal":
                ship_coordinates = Dot(self.start_point.x + item, self.start_point.y)
                dots_list.append(ship_coordinates)
        return dots_list


class Board:
    def __init__(self, hid):
        self.hid = hid
        self.state_board = [["○" for _ in range(6)] for _ in range(6)]
        self.ship_list = []
        self.alive_ships = 0

    def add_ship(self, ship):
        for dot in ship.dots():
            try:
                if dot.x > 6 or dot.x <= 0 or dot.y > 6 or dot.y <= 0:
                    raise BoardOutException()
                elif self.state_board[dot.x - 1][dot.y - 1] == "-":
                    raise BlockCoordinate()
                elif self.state_board[dot.x - 1][dot.y - 1] == "■":
                    raise SamePointException()
            except BlockCoordinate as e:
                return False
            except BoardOutException as e:
                return False
            except SamePointException as e:
                return False
        for dot in ship.dots():
            self.state_board[dot.x - 1][dot.y - 1] = "■"

        self.ship_list.append(ship)
        self.contour(ship)
        self.alive_ships += 1
        return True

    @staticmethod
    def handle_starting_point(dot: Dot, direction: str):
        if direction == "vertical":
            return [Dot(dot.x, dot.y - 1), Dot(dot.x + 1, dot.y), Dot(dot.x - 1, dot.y)]
        if direction == "horizontal":
            return [Dot(dot.x - 1, dot.y), Dot(dot.x, dot.y + 1), Dot(dot.x, dot.y - 1)]

    @staticmethod
    def handle_end_point(dot: Dot, direction: str):
        if direction == "vertical":
            return [Dot(dot.x, dot.y + 1), Dot(dot.x + 1, dot.y), Dot(dot.x - 1, dot.y)]
        if direction == "horizontal":
            return [Dot(dot.x + 1, dot.y), Dot(dot.x, dot.y + 1), Dot(dot.x, dot.y - 1)]

    @staticmethod
    def handle_middle_point(dot: Dot, direction: str):
        if direction == "vertical":
            return [Dot(dot.x + 1, dot.y), Dot(dot.x - 1, dot.y)]
        if direction == "horizontal":
            return [Dot(dot.x, dot.y + 1), Dot(dot.x, dot.y - 1)]

    def contour(self, ship: Ship):
        dot_list = ship.dots()
        direction = ship.direction
        starting_point = ship.start_point
        end_point = dot_list[-1]
        if len(dot_list) == 1:
            dot = dot_list[0]
            dot_to_delete = [Dot(dot.x + 1, dot.y), Dot(dot.x - 1, dot.y), Dot(dot.x, dot.y + 1), Dot(dot.x, dot.y - 1)]
            for dot in dot_to_delete:
                if not self.out(dot):
                    self.state_board[dot.x - 1][dot.y - 1] = "-"

        else:
            dot_to_delete = []
            for dot in dot_list:
                if dot.__eq__(starting_point):
                    dot_to_delete.append(self.handle_starting_point(dot, direction))

                elif dot.__eq__(end_point):
                    dot_to_delete.append(self.handle_end_point(dot, direction))
                else:
                    dot_to_delete.append(self.handle_middle_point(dot, direction))
            flatter_list = sum(dot_to_delete, [])
            for dot in flatter_list:
                if not self.out(dot):
                    self.state_board[dot.x - 1][dot.y - 1] = "-"

    def clean_board(self):
        new_board = copy.deepcopy(self.state_board)
        for i, x in enumerate(new_board):
            for j, y in enumerate(x):
                if y == '■' or y == '-':
                    new_board[i][j] = '○'
        return new_board

    def clean_countor(self):
        new_board = copy.deepcopy(self.state_board)
        for i, x in enumerate(new_board):
            for j, y in enumerate(x):
                if y == '-':
                    new_board[i][j] = '○'
        return new_board

    def display_board(self):
        if self.hid:
            board_to_display = self.clean_board()
            print('  | 1 | 2 | 3 | 4 | 5 | 6 \n')
            for i in range(len(board_to_display)):
                print(i + 1, *board_to_display[i], sep=" | ")
                print()
        else:
            board_to_display_2 = self.clean_countor()
            print('  | 1 | 2 | 3 | 4 | 5 | 6 \n')
            for i in range(len(board_to_display_2)):
                print(i + 1, *board_to_display_2[i], sep=" | ")
                print()

    @staticmethod
    def out(dot):
        if dot.x > 6 or dot.x <= 0 or dot.y > 6 or dot.y <= 0:
            return True
        else:
            return False

    def get_ship(self, dot: Dot):
        for ship in self.ship_list:
            if dot in ship.dots():
                return ship

    def shoot(self, dot):
        x = dot.x  # get x
        y = dot.y  # get y
        if self.out(dot):
            print("Вы не можете стрелять за пределами игрового поля")
            return True
        if self.state_board[x - 1][y - 1] == "■":
            print("\n Попадание! \n")
            self.state_board[x - 1][y - 1] = "X"
            ship = self.get_ship(dot)
            ship.hp -= 1
            if ship.hp == 0:
                print("Корабль убит!")
                self.alive_ships -= 1
            return True

        if self.state_board[x - 1][y - 1] == "T":
            print("\n Вы уже стреляли в эту ячейку \n")
            return True
        if self.state_board[x - 1][y - 1] == "X":
            print("\n Вы уже стреляли в эту ячейку \n")
            return True
        if self.state_board[x - 1][y - 1] == "○":
            print("\n Промах! \n")
            self.state_board[x - 1][y - 1] = "T"
            return False
        if self.state_board[x - 1][y - 1] == "-":
            print("\n Промах! \n")
            self.state_board[x - 1][y - 1] = "T"
            return False


class Player:
    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    def ask(self):
        return Dot(0, 0)

    def move(self):
        shot_dot: Dot = self.ask()
        while True:
            try:
                extra_shoot = self.enemy_board.shoot(shot_dot)
                print("Точка выстрела: ", shot_dot.x, shot_dot.y)
                return extra_shoot
            except BoardOutException as e:
                print("Вы выстрелили за пределы игрового поля, попробуйте еще раз")
                return True
            except SamePointException:
                print("Вы уже выстрелили в данную клетку")
                return True
            except GameEnd:
                print("Игра окончена")
                return False


class AI(Player):
    def ask(self):
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        return Dot(x, y)


class User(Player):
    def ask(self):
        while True:
            try:
                row = input("Введите номер строки для выстрела:")
                if len(row) != 1 or not row.isdigit():
                    raise ValueError("\n<<<Требуется одно число от 1 до 6>>>\n")

                column = input("Введите номер столбца для выстрела: ")
                if len(column) != 1 or not column.isdigit():
                    raise ValueError("\n<<<Требуется одно число от 1 до 6>>>\n")

                x = int(row)
                y = int(column)
                if x < 1 or x > 6 or y < 1 or y > 6:
                    raise BoardOutException("\n<<<Введенные координаты находятся вне диапазона от 1 до 6>>>\n")

                return Dot(x, y)
            except BoardOutException as e:
                print(e)
            except ValueError as ve:
                print(ve)


class Game:
    def __init__(self):
        self.user_board = self.random_board(False)
        self.ai_board = self.random_board(True)

        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    @staticmethod
    def can_add(board: Board, ship):
        for dot in ship.dots():
            x = dot.x
            y = dot.y
            if (x <= 0 or x > 6) or (y <= 0 or y > 6):
                return False
            if board.state_board[x - 1][y - 1] != "○":
                return False
        return True

    @staticmethod
    def random_board(hid: bool):
        board = Board(hid)
        ship_lengths = [1, 1, 1, 1, 2, 2, 3]
        for i in ship_lengths:
            while True:
                try:
                    direction = random.choice(["vertical", "horizontal"])
                    start_point = Dot(random.randint(1, 6), random.randint(1, 6))
                    ship = Ship(i, start_point, direction)
                    if board.add_ship(ship):
                        break
                except CouldntPlaceShip as e:
                    print()
        return board

    @staticmethod
    def greet():
        print("\nДобро пожаловать в игру Морской Бой!\n")

    def loop(self):
        self.greet()

        while True:
            while True:
                print("---- 🤖 Доска Врага 🤖 -----")
                self.ai_board.display_board()
                print("- - - - - - - - - - - - - - -")
                print("Ваш ход: ")
                if self.check_game_over():
                    print("Вы Победили!")
                    break
                if not self.user.move():
                    break
            if self.check_game_over():
                break
            while True:
                print("- - - - - - - - - - - - - - -")
                print("Ход врага: ")
                if self.check_game_over():
                    print("Противник Победил!")
                    break
                if not self.ai.move():
                    print("---- ⭐️ Ваша Доска ⭐️ -----")
                    self.user_board.display_board()
                    break

    def check_game_over(self):
        if self.user.enemy_board.alive_ships == 0:
            return True
        elif self.ai.enemy_board.alive_ships == 0:
            return True
        return False


if __name__ == "__main__":
    game = Game()
    game.loop()
