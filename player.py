import math
import random

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class GeniusComputerPlayer(Player):
    def get_move(self, game):
        if len(game.available_moves()) == 9:
            return random.choice(game.available_moves())
        return self.minimax(game, self.letter)['position']

    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {
                'position': None,
                'score': 1 * (state.num_empty_squares() + 1)
                if other_player == max_player else -1 * (state.num_empty_squares() + 1)
            }
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for move in state.available_moves():
            state.make_move(move, player)
            sim_score = self.minimax(state, other_player)
            state.board[move] = ' '
            state.current_winner = None
            sim_score['position'] = move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best
