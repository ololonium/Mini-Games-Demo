from random import randint
from time import sleep


class BoardException(Exception):
    pass


class OutOfBoard(BoardException):
    def __str__(self):
        return 'Выстрел за пределы поля!'


class UsedDot(BoardException):
    def __str__(self):
        return 'Сюда уже стреляли, выберите другие координаты!'


class ShipPlacement(BoardException):
    pass


class Dot:
    '''Класс точка, сравнение и возврат координат'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return self.x, self.y


class Ship:
    '''Класс корабль, начало корабля, размер, ориентация в пространстве, по горизонтали или вертикали'''
    def __init__(self, head, long, orient):
        self.head = head
        self.long = long
        self.orient = orient
        self.lives = long

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.long):
            current_x = self.head.x
            current_y = self.head.y
            if self.orient == 0:
                current_x += i
            elif self.orient == 1:
                current_y += i
            ship_dots.append(Dot(current_x, current_y))
        return ship_dots


class Board:
    '''Класс игровая доска, объект которого хранит поле, список кораблей,
    список совершенных выстрелов, счетчик подбитых кораблей, отвечает за
    расположение кораблей на доске...'''# дополнить описание
    def __init__(self, hide=False, size=6):
        self.hide = hide
        self.size = size
        self.field = [['-'] * size for _ in range(size)]#само поле
        self.count = 0
        self.ships = []#расположение кораблей
        self.used_dots = []#сделанные выстрелы

    def __str__(self):
        position = ''
        position += '  | 1 | 2 | 3 | 4 | 5 | 6 | '
        for a, b in enumerate(self.field):
            position += f'\n\t\t\t\t\t {a + 1} | ' + ' | '.join(b) + ' | '
        if self.hide:
            position = position.replace('T', '-')
        return position

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot) or dot in self.used_dots:
                raise ShipPlacement()
        for dot in ship.dots:
            self.field[dot.x][dot.y] = 'T'
            self.used_dots.append(dot)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        around = [
            (1, 1), (1, 0), (0, 1),
            (0, 0), (-1, 0), (0, -1),
            (-1, -1), (1, -1), (-1, 1)
        ]
        for dot in ship.dots:
            for dot_x, dot_y in around:
                current = Dot(dot.x + dot_x, dot.y + dot_y)
                if not (self.out(current)) and current not in self.used_dots:
                    if verb:
                        self.field[current.x][current.y] = '*'
                    self.used_dots.append(current)

    def out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):
        if self.out(dot):
            raise OutOfBoard()
        if dot in self.used_dots:
            raise UsedDot()
        self.used_dots.append(dot)
        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.field[dot.x][dot.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('\nКорабль пошел ко дну!')
                    return False
                else:
                    print('Кораблю нанесен урон, но он еще на плаву!')
                    return True
        self.field[dot.x][dot.y] = '*'
        print('\tНе попал!')
        return False

    def begin(self):
        self.used_dots = []


class Player:
    '''Класс Игрок'''
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def move(self):
        while True:
            try:
                target = self.ask()
                ask_shot = self.enemy.shot(target)
                return ask_shot
            except BoardException as error:
                print(error)

    def ask(self):
        raise NotImplementedError()


class AI(Player):
    '''Класс ИИ от Игрок'''
    def ask(self):
        dot = Dot(randint(0, 5), randint(0, 5))#позже доработать ИИ, нужно переписать и объединить с логикой расстановки корабля
        print(f'Ход адмирала Василия: {dot.x + 1} {dot.y + 1}')
        return dot


class User(Player):
    '''Класс пользователь от Игрок'''
    def ask(self):
        while True:
            coordinates = input('Введите X и Y: ').split()
            if len(coordinates) != 2:
                print('\tВведите "X"(строку) и "Y"(столбец) через пробел: ')
                continue
            x, y = coordinates
            if not (x.isdigit()) or not (y.isdigit()):#строка из чисел?
                print('\t"X"(строка) и "Y"(столбец) должны быть числами от 1 до 6: ')
                continue
            x, y = int(x), int(y)#числа из строки в инт
            return Dot(x - 1, y - 1)


class Game:
    '''Класс Игра(движок), правила, расположение, основной цикл'''
    def __init__(self, size=6):#создать поле, скрыть поле ИИ
        self.size = size
        player = self.random_board()
        computer = self.random_board()
        computer.hide = True
        self.ai = AI(computer, player)
        self.user = User(player, computer)

    def greet(self):#описание игры
        print('''\n\t\tДобро пожаловать в легендарную игру "Морской бой"!
        Вам предстоит сразиться с чудом компьютерной мысли,
        искусственным интелектом - адмиралом Василием, он
        постарается быть более гуманным, и дать вам фору, но
        помните - он все же довольно коварен и хитер! Удачи!''')
        print('''\n\t\tДля того, чтобы совершить ход вам необходимо ввести
        две координаты "X" и "Y": 
        "X" - координата по горизонтали(строка) 
        "Y" - координата по вертикали(столбец)\n''')

    def placement_ship(self):#логика расположения корабля
        lens = [3, 2, 2, 1, 1, 1, 1]#размеры кораблей
        board = Board(size=self.size)
        position = 0
        for long in lens:#рядом корабль - не распологать еще один в радиусе одной точки
            while True:
                position += 1
                if position > 1000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), long, randint(0, 1))#корабль(точка(х, у)размер, ориентация)
                try:
                    board.add_ship(ship)
                    break
                except ShipPlacement:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.placement_ship()
        return board

    def loop(self):#цикл смены хода
        priority = 0
        while True:
            sleep(1)
            print('\t' * 5, '*' * 27)
            print('\t' * 5, '\t\t Ваше поле:')
            print('\t' * 5, '-' * 27)
            print('\t' * 5, self.user.board)
            print('\t' * 5, '-' * 27)
            print('\t' * 5, '*' * 27)
            print('\t' * 5, '\tПоле адмирала Василия:')
            print('\t' * 5, '-' * 27)
            print('\t' * 5, self.ai.board)

            if priority % 2 == 0:
                sleep(1)
                print('\t' * 5, '-' * 27)
                print('\t' * 5, 'Ваш черед!')
                sleep(1)
                change = self.user.move()
            else:
                sleep(1)
                print('\t' * 5, '-' * 27)
                print('\t' * 5, 'Ходит адмирал Василий!')
                sleep(1)
                change = self.ai.move()
            if change:
                priority -= 1

            if self.ai.board.count == 7:
                print('\t' * 5, '-' * 27)
                print('\t' * 5, 'Победа ваша, Василий рукоплещет вам!')
                break
            elif self.user.board.count == 7:
                print('\t' * 5, '-' * 27)
                print('\t' * 5, 'Василий победил, он все еще лучший!')
                break
            priority += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
