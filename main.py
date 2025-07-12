from game import TicTacToe
from gui import start_game

if __name__ == '__main__':
    start_game()

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(f"{letter} makes a move to square {square}")
                game.print_board()
                print('')  # Empty line

            if game.current_winner:
                if print_game:
                    print(f"{letter} wins!")
                return letter

            letter = 'O' if letter == 'X' else 'X'

        # Slow down for better UX
        import time
        time.sleep(0.8)

    if print_game:
        print("It's a tie.")

if __name__ == '__main__':
    x_player = HumanPlayer('X')
    o_player = GeniusComputerPlayer('O')  # Or RandomComputerPlayer
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
