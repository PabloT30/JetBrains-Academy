import random as rd

domino_set = []
stock_pieces = []
computer_pieces = []
player_pieces = []
status = ""
snake = []


def create_domino_set():
    return [[i, j] for i in range(7) for j in range(i, 7)]


def remove_from_domino_set(domino_set_, pieces_list_):
    return [domino for domino in domino_set_ if domino not in pieces_list_]


def distribute_domino_set(domino_set_):
    stock_pieces_ = domino_set_
    rd.shuffle(stock_pieces_)

    computer_pieces_ = rd.sample(stock_pieces_, k=7)
    stock_pieces_ = remove_from_domino_set(stock_pieces_, computer_pieces_)

    player_pieces_ = rd.sample(stock_pieces_, k=7)
    stock_pieces_ = remove_from_domino_set(stock_pieces_, player_pieces_)

    return stock_pieces_, computer_pieces_, player_pieces_


def get_domino_snake(computer_pieces_, player_pieces_):
    doubles_ = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]
    computer_pieces_doubles = sorted([domino for domino in doubles_ if domino in computer_pieces_], reverse=True)
    player_pieces_doubles = sorted([domino for domino in doubles_ if domino in player_pieces_], reverse=True)

    if any(computer_pieces_doubles) and any(player_pieces_doubles):
        if computer_pieces_doubles[0][0] > player_pieces_doubles[0][0]:
            return "computer", computer_pieces_doubles[0]
        else:
            return "player", player_pieces_doubles[0]
    elif any(computer_pieces_doubles):
        return "computer", computer_pieces_doubles[0]
    elif any(player_pieces_doubles):
        return "player", player_pieces_doubles[0]
    else:
        return False, False


def initiate_game():
    global domino_set
    global stock_pieces
    global computer_pieces
    global player_pieces
    global status
    global snake

    domino_set = create_domino_set()

    while True:
        stock_pieces, computer_pieces, player_pieces = distribute_domino_set(domino_set)
        domino_snake_owner, domino_snake = get_domino_snake(computer_pieces, player_pieces)
        if domino_snake_owner and domino_snake:
            break

    if domino_snake_owner == "player":
        player_pieces.remove(domino_snake)
        status = "computer"
    else:
        computer_pieces.remove(domino_snake)
        status = "player"

    snake = [domino_snake]


def show_playing_field(stock_pieces_, computer_pieces_, player_pieces_, snake_, status_):
    print("=" * 70)
    print(f"Stock size: {len(stock_pieces_)}")
    print(f"Computer pieces: {len(computer_pieces_)}")
    print()
    if len(snake_) <= 6:
        print(f"{''.join([str(i) for i in snake_])}")  # print list as a string to print without external []
    else:
        print(f"{''.join([str(i) for i in snake_[:3]])}...{''.join([str(i) for i in snake_[-3:]])}")
    print()
    print("Your pieces:")
    for i in range(len(player_pieces_)):
        print(f"{i + 1}:{player_pieces_[i]}")
    print()
    if status_ == "computer":
        print("Status: Computer is about to make a move. Press Enter to continue...")
    elif status_ == "player":
        print("Status: It's your turn to make a move. Enter your command.")
    elif status_ == "draw":
        print("Status: The game is over. It's a draw!")
    elif status_ == "computer_wins":
        print("Status: The game is over. The computer won!")
    elif status_ == "player_wins":
        print("Status: The game is over. You won!")


def is_move_valid(move_, status_, player_pieces_):
    if status_ == "player":
        if (move_.strip('-')).isnumeric() and int(move_) in list(range(-len(player_pieces_), len(player_pieces_) + 1)):
            return True
        else:
            return False
    elif status_ == "computer":
        if move_ == "":
            return True
        else:
            return False


def is_move_legal(snake_, move_, status_, computer_pieces_, player_pieces_):
    if status_ == "player":
        move_ = int(move_)
        if move_ > 0:
            return any([i == snake_[-1][1] for i in player_pieces_[move_ - 1]])
        else:
            return any([i == snake_[0][0] for i in player_pieces_[abs(move_) - 1]])
    elif status_ == "computer":
        if move_ > 0:
            return any([i == snake_[-1][1] for i in computer_pieces_[move_ - 1]])
        else:
            return any([i == snake_[0][0] for i in computer_pieces_[abs(move_) - 1]])


def get_hand_score(snake_, hand_):
    hand_score = {}
    count = {}

    # Count the number of 0's, 1's, 2's, etc., in hand, and in the snake.
    for i in range(7):
        count[i] = sum(domino.count(i) for domino in snake_) + sum(domino.count(i) for domino in hand_)

    # Score each domino in hand as the sum of appearances of each of its numbers.
    for domino in hand_:
        hand_score[str(domino)] = count[domino[0]] + count[domino[1]]

    return hand_score


def get_move(snake_, status_, computer_pieces_, player_pieces_):
    hand_score = get_hand_score(snake_, computer_pieces_)
    hand_score = sorted(hand_score, key=hand_score.get, reverse=True)  # get key values from reversed sorted dict
    hand_score = [[int(x) for x in domino.strip('][').split(', ')] for domino in hand_score]  # to list
    for i, domino in enumerate(hand_score):
        if is_move_legal(snake_, i + 1, status_, hand_score, player_pieces_):
            return computer_pieces_.index(domino) + 1
        elif is_move_legal(snake_, -i - 1, status_, hand_score, player_pieces_):
            return -computer_pieces_.index(domino) - 1
    return 0


def prompt_for_move(snake_, status_, computer_pieces_, player_pieces_):
    while True:
        move_ = input()
        if is_move_valid(move_, status_, player_pieces_):
            if status_ == "computer":
                move_ = get_move(snake_, status_, computer_pieces_, player_pieces_)
            if is_move_legal(snake_, move_, status_, computer_pieces_, player_pieces_) or int(move_) == 0:
                break
            else:
                if status_ == "player":
                    print("Illegal move. Please try again.")
        else:
            print("Invalid input. Please try again.")
    return move_


def update_playing_field(status_, move_):
    global stock_pieces
    global computer_pieces
    global player_pieces
    global status
    global snake

    if status_ == "computer":
        if move_ == 0:
            if not stock_pieces:
                pass
            else:
                computer_pieces.append(rd.choice(stock_pieces))
                stock_pieces.remove(computer_pieces[-1])
        else:
            if move_ > 0:
                if snake[-1][1] == computer_pieces[move_ - 1][0]:
                    snake.append(computer_pieces[move_ - 1])
                    del computer_pieces[move_ - 1]
                else:
                    computer_pieces[move_ - 1] = computer_pieces[move_ - 1][::-1]
                    snake.append(computer_pieces[move_ - 1])
                    computer_pieces[move_ - 1] = computer_pieces[move_ - 1][::-1]
                    del computer_pieces[move_ - 1]
            else:
                if snake[0][0] == computer_pieces[abs(move_) - 1][1]:
                    snake.insert(0, computer_pieces[abs(move_) - 1])
                    del computer_pieces[abs(move_) - 1]
                else:
                    computer_pieces[abs(move_) - 1] = computer_pieces[abs(move_) - 1][::-1]
                    snake.insert(0, computer_pieces[abs(move_) - 1])
                    computer_pieces[abs(move_) - 1] = computer_pieces[abs(move_) - 1][::-1]
                    del computer_pieces[abs(move_) - 1]
        status = "player"
    elif status_ == "player":
        move_ = int(move_)
        if move_ == 0:
            if not stock_pieces:
                pass
            else:
                player_pieces.append(rd.choice(stock_pieces))
                stock_pieces.remove(player_pieces[-1])
        else:
            if move_ > 0:
                if snake[-1][1] == player_pieces[move_ - 1][0]:
                    snake.append(player_pieces[move_ - 1])
                    del player_pieces[move_ - 1]
                else:
                    player_pieces[move_ - 1] = player_pieces[move_ - 1][::-1]
                    snake.append(player_pieces[move_ - 1])
                    player_pieces[move_ - 1] = player_pieces[move_ - 1][::-1]
                    del player_pieces[move_ - 1]
            else:
                if snake[0][0] == player_pieces[abs(move_) - 1][1]:
                    snake.insert(0, player_pieces[abs(move_) - 1])
                    del player_pieces[abs(move_) - 1]
                else:
                    player_pieces[abs(move_) - 1] = player_pieces[abs(move_) - 1][::-1]
                    snake.insert(0, player_pieces[abs(move_) - 1])
                    player_pieces[abs(move_) - 1] = player_pieces[abs(move_) - 1][::-1]
                    del player_pieces[abs(move_) - 1]
        status = "computer"


def game_is_over(snake_, computer_pieces_, player_pieces_):
    if not computer_pieces_:
        return "computer_wins"
    elif not player_pieces_:
        return "player_wins"
    elif snake_[0][0] == snake_[-1][1]:
        if [j for i in snake_ for j in i].count(snake_[0][0]) == 8:  # snake_[0][0] is 8 times in snake_
            return "draw"
    else:
        return False


def main():
    global status
    initiate_game()

    while True:
        show_playing_field(stock_pieces, computer_pieces, player_pieces, snake, status)
        move = prompt_for_move(snake, status, computer_pieces, player_pieces)
        update_playing_field(status, move)
        game_status = game_is_over(snake, computer_pieces, player_pieces)
        if game_status == "draw":  # if somebody wins or game draw
            status = game_status
            show_playing_field(stock_pieces, computer_pieces, player_pieces, snake, status)
            break
        elif game_status == "computer_wins":
            status = game_status
            show_playing_field(stock_pieces, computer_pieces, player_pieces, snake, status)
            break
        elif game_status == "player_wins":
            status = game_status
            show_playing_field(stock_pieces, computer_pieces, player_pieces, snake, status)
            break


if __name__ == "__main__":
    main()
