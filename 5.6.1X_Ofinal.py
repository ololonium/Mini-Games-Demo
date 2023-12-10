# Игра крестики-нолики
# Объяснить правила
print('\n\t\tЗдравствуй, "дорогой друг", сейчас мы проверим,\n'
      '\t\tсможешь ли ты выиграть хоть одну партию,\n'
      '\t\tв легендарную игру "крестики-нолики"?! Начнем!\n')
print('\t\tЭто наше поле для самого сильного разочарования в твоей жизни!\n'
      '\t\tЧисло в ячейке соответствует позиции на доске, то есть чтобы\n'
      '\t\tзанять ячейку, необходимо писать соответствующую ей цифру!\n')

# Создать список позиций на доске доске
board = [1,2,3,
         4,5,6,
         7,8,9]

# Выигрышные комбинации
win_combo = [[0,1,2],
             [3,4,5],
             [6,7,8],
             [0,3,6],
             [1,4,7],
             [2,5,8],
             [0,4,8],
             [2,4,6]]

# Создадим и выведем доску на экран
def create_board():
    print('\t\t\t\t\t', '-' * 13)
    print('\t\t\t\t\t', '|', board[0], '|', board[1], '|', board[2], '|')
    print('\t\t\t\t\t', '-' * 13)
    print('\t\t\t\t\t', '|', board[3], '|', board[4], '|', board[5], '|')
    print('\t\t\t\t\t', '-' * 13)
    print('\t\t\t\t\t', '|', board[6], '|', board[7], '|', board[8], '|')
    print('\t\t\t\t\t', '-' * 13)


# Сохраним код в ячейку
def step_board(step, position):
    pos_id = board.index(step)
    board[pos_id] = position

# Текущий результат
def print_board():
    winner = ''
    for i in win_combo:
        if board[i[0]] == 'X' and board[i[1]] == 'X' and board[i[2]] == 'X':
            winner = 'X'
        if board[i[0]] == 'O' and board[i[1]] == 'O' and board[i[2]] == 'O':
            winner = 'O'
    return winner

# поиск линии с нужным количеством X и O
def line_check(in_line_O, in_line_X):
    step = ''
    for line in win_combo:
        o = 0
        x = 0
        for j in range(0, 3):
            if board[line[j]] == 'O':
                o = o + 1
            if board[line[j]] == 'X':
                x = x + 1
        if o == in_line_O and x == in_line_X:
            for j in range(0, 3):
                if board[line[j]] != 'O' and board[line[j]] != 'X':
                    step = board[line[j]]

    return step

# Ход ИИ
# Если есть 2 в ряд, нужно поставить 3
# Если центр открыт, нужно его занять, иначе занять ячейку 1
def ai_step():
    step = ''
    step = line_check(2, 0)
    if step =='':
        step = line_check(0, 2)
    if step == '':
        step = line_check(1, 0)
    if step =='':
        if board[4] != 'X' and board[4] != 'O':
            step = 5
    if step == '':
        if board[0] != 'X' and board[0] != 'O':
            step = 1
    return step

# Игровой процесс
game_over = False
human = True
while game_over == False:
    create_board()
    if human == True:
        position = 'X'
        step = int(input('Ходи, кожаный: '))
    else:
        print('Непобедимый наступает: ')
        position = 'O'
        step = ai_step()

    if step != '':
        step_board(step, position)
        winner = print_board()
        if winner != '':
            game_over = True
        else:
            game_over = False
    else:
        print('Неплохо кожаный, но это не победа!')
        game_over = True
        winner = 'Ничья!'
    human = not(human)

create_board()
print(winner)
print(input('\nНажмите Enter, чтобы выйти.'))
