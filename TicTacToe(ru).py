from itertools import cycle as itercycle
from random import randint

def bot(game):
    while True:
        row_bot = randint(0, game_size-1)
        column_bot = randint(0, game_size-1)
        if game[row_bot][column_bot] == 0:
            print("Выбор бота: {} {}".format(row_bot+1, column_bot+1))
            return row_bot, column_bot

def input_errors(inp, len_inp, size=None):
    inp = inp.split()
    try:
        inp = tuple(map(int, inp))
    except:
        print("Входящие значения должны быть целочисленными", end='\n\n')
        return False, None
    if len(inp) != len_inp:
        print("Количество входящих значений должно быть {}, полученно {}".format(len_inp, len(inp)), end='\n\n')
        return False, None
    if len_inp == 1:
        if inp[0] < 3:
            print("Размер игрового поля не может  быть меньше минимального", end='\n\n')
            return False, None
    else:
        for i in inp:
            if i < 1:
                print("Входящие значения должны быть больше нуля", end='\n\n')
                return False, None
            if size != None:
                if i > size:
                    print ("Входящие значения не должны превышать размера игрового поля", end='\n\n')
                    return False, None
    return True, inp 


def game_board(game_map, player=0, row=0, column=0):
    
    if game_map[row][column] != 0:
        print ("Эта ячейка уже сыграла, выберите несыгравшую ячейку", end='\n\n')
        return game_map, False
    if player != 0:
        game_map[row][column] = player
    print("   "+"  ".join([str(i+1) for i in range(len(game_map))]))
    for item, row in enumerate(game_map):
        game_string = ""
        for simbol in row:
            if simbol == 0:
                game_string += " . "
            if simbol == 1:
                game_string += " X "
            if simbol == 2:
                game_string += " O "
        print(item + 1, game_string)
    print()

    return game_map, True


def win(current_game, current_player):

    current_game_t = [[row[i] for row in current_game] for i in range(len(current_game[0]))]
    diagonal_f = [[current_game[i][i] for i in range(len(current_game))]]*3
    diagonal_r = [[current_game[i][v] for i, v in enumerate(reversed(range(len(current_game))))]]*3

    game_table = (current_game, current_game_t, diagonal_f, diagonal_r)
    break_flag = False
    for item_game, view_game in enumerate(game_table):
        for item, row in enumerate(view_game):
            if row.count(row[0]) == len(row) and row[0] != 0:
                win_line = ('строке', 'столбце', 'прямой диагонали', 'обратной диагонали')
                winner = ('Игрок 1', 'Бот') if single_mode else ('Игрок 1', 'Игрок 2')
                if item_game < 2:
                    print("{} выиграл в {} {}"
                          .format(winner[int(current_player)-1], item+1, win_line[item_game]), end='\n\n')
                if item_game >= 2:
                    print("{} выиграл на {}"
                          .format(winner[int(current_player)-1], win_line[item_game]), end='\n\n')
                return True
    return False

'''def standoff(current_game):
    for row in current_game:
        for simbol in row:
            if simbol == 0: return False
    print("В этой игре нет победителя. Ничья", end='\n\n')
    return True'''

def standoff(current_game):
    if any(any(j == 0 for j in i) for i in current_game):
        return False
    print("В этой игре нет победителя. Ничья", end='\n\n')
    return True

while True:
    single_mode = input("Выберите режим игры. Одиночный(по умолманию), совместный(m): ")
    single_mode = True if single_mode.lower() != 'm' and single_mode.lower() != 'ь' else False

    while True:
        game_size = input("Введите размер игрового поля. 3 размер по умолчанию - минимальный размер: ")
        if game_size != '':
            if not input_errors(game_size, 1)[0]: continue
        game_size = 3 if game_size == '' else int(game_size)
        game = [[0]*game_size for i in range(game_size)]

        players = itercycle([1, 2])

        game = game_board(game)[0]

        while True:
            player = next(players)

            while True:
                if single_mode and player == 2:
                    bot_choice = bot(game)
                    game, played = game_board(game, player, *bot_choice)
                else:
                    choice = input_errors(input('Введите через пробел номер строки и столбца играющей ячейки, игрок {}: '
                                                .format(player)), 2, game_size) 
                    if  not choice[0]:
                        continue
                    choice = [i-1 for i in choice[1]]
                    game, played = game_board(game, player, *choice)
                if played: break
            if win(game, player) or standoff(game):
                play_again = input("Игра окончена, сыграть снова? Да(значение по умолчанию), Изменить режим игры(n), Выйти(e): ")
                print(end='\n\n')
                break
        if play_again == 'n'.lower() or play_again == 'т'.lower(): break
        if play_again == 'e'.lower() or play_again == 'у'.lower(): break
    if play_again == 'e'.lower() or play_again == 'у'.lower(): break
