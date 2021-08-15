# Tic-Tac-Toe game to play within the Python CLI.
def print_game(game_state_):
    print("---------")
    print(f"| {game_state_[0][0]} {game_state_[0][1]} {game_state_[0][2]} |")
    print(f"| {game_state_[1][0]} {game_state_[1][1]} {game_state_[1][2]} |")
    print(f"| {game_state_[2][0]} {game_state_[2][1]} {game_state_[2][2]} |")
    print("---------")


def has_won(game_state_, player):
    # check whether there are three X's or O's in a horizontal line
    for row in range(len(game_state_)):
        if game_state_[row].count(player) == 3:
            return True

    # check whether there are three X's or O's in a vertical line
    transposed_game_state_ = list(zip(*game_state_))
    for row in range(len(transposed_game_state_)):
        if transposed_game_state_[row].count(player) == 3:
            return True

    # check whether there are three X's or O's in diagonal lines (i.e. \ and /)
    # get diagonal vector: \
    aux_diagonal_vector = [game_state_[row_index][column_index] for row_index in range(3)
                           for column_index in range(3) if row_index == column_index]

    if aux_diagonal_vector.count(player) == 3:
        return True

    # get anti diagonal vector: /
    aux_anti_diagonal_vector = [game_state_[row_index][column_index] for row_index in range(3)
                                for column_index in range(3) if row_index + column_index == 2]

    if aux_anti_diagonal_vector.count(player) == 3:
        return True


def x_wins(game_state_):
    if has_won(game_state_, 'X'):
        return True
    else:
        return False


def o_wins(game_state_):
    if has_won(game_state_, 'O'):
        return True
    else:
        return False


def game_draw(game_state_):
    # check if game is done AND no winner.
    game_state_list = [element for row in game_state_ for element in row]
    if (x_wins(game_state_) is False) and (o_wins(game_state_) is False) and (game_state_list.count('_') == 0):
        return True
    else:
        return False


def game_is_done(game_state_):
    # not finished when neither side has three
    # in a row but the grid still has empty cells.
    # has empty_cells? no? return true
    game_state_list = [element for row in game_state_ for element in row]
    if (x_wins(game_state_) is False) and (o_wins(game_state_) is False) and (game_state_list.count('_') > 0):
        return False
    else:
        return True


def impossible_game(game_state_):
    # two winners, or with one player having made too many moves
    if x_wins(game_state_) and o_wins(game_state_):
        return True
    elif abs(sum(row.count('X') for row in game_state_)
             - sum(row.count('O') for row in game_state_)) > 1:
        return True
    else:
        return False


def is_game_state_valid(user_input_):
    # Check whether user input consists of valid characters and is 9-char length.
    valid_inputs = "XO_"
    if len(user_input_) == 9:
        for char in user_input_:
            if char in valid_inputs:
                continue
            else:
                return False
        return True
    else:
        return False


def is_move_valid(move_, game_state_):
    valid_inputs = [1, 2, 3]
    row, column = move_.split()
    if row.isnumeric() and column.isnumeric():
        row, column = int(row), int(column)
        if row in valid_inputs and column in valid_inputs:
            if game_state_[row - 1][column - 1] == '_':
                return True
            else:
                print("This cell is occupied! Choose another one!")
                return False
        else:
            print("Coordinates should be from 1 to 3!")
            return False
    else:
        print("You should enter numbers!")
        return False


def string_to_matrix(user_input_):
    # Convert 9-char length string to 3x3 matrix.
    list_ = list(user_input_)
    return [[list_[i], list_[i + 1], list_[i + 2]] for i in [0, 3, 6]]


def check_game_status(game_state_):
    if impossible_game(game_state_) is True:
        print("Impossible")
        return False
    elif game_is_done(game_state_):
        return True
    else:
        print("Game not finished")
        return False


# to run for test on JetBrains Academy
def main():
    user_input = "_________"  # e.g. XXXOO__O_ to enter a game state, exit to stop game.
    game_state = string_to_matrix(user_input)
    print_game(game_state)
    
    turn = "X"
    
    while True:
        user_input = input()
        if is_move_valid(user_input, game_state):
            row, column = [int(i) for i in user_input.split()]
            if turn == "X":
                game_state[row - 1][column - 1] = "X"
                turn = "O"
            elif turn == "O":
                game_state[row - 1][column - 1] = "O"
                turn = "X"
            print_game(game_state)
            if check_game_status(game_state):
                if x_wins(game_state):
                    print("X wins")
                    break
                elif o_wins(game_state):
                    print("O wins")
                    break
                elif game_draw(game_state):
                    print("Draw")
                    break


if __name__ == '__main__':
    main()
