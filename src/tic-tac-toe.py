from typing import Union, List
import copy


class TicTacToeState:
    """ represents the state of a tic-tac-toe game: the board and which player's turn"""

    def __init__(self, board: list, player_turn: str):
        self.board = board
        self.player_turn = player_turn

    def __eq__(self, other):
        return all(item in self.board for item in other.board) and self.player_turn == other.player_turn

    def __str__(self):
        return f"board={self.board}, \n player turn={self.player_turn}"


class TicTacToeAction:
    """ represents an action in a tic-tac-toe game"""

    def __init__(self, row: int, col: int, player: str):
        self.row = row
        self.col = col
        self.player = player

    def __eq__(self, other_action):
        return self.row == other_action.row and self.col == other_action.col

    def __str__(self):
        return f"placing {self.player} at ({self.row}, {self.col})"


def utility(game_state: TicTacToeState) -> Union[None, int]:
    """ returns None if the game is not yet over, 0 if the game was a draw, 1 if X won, -1 if O won"""
    board = game_state.board
    top_left = board[0][0]
    top_middle = board[0][1]
    top_right = board[0][2]
    middle_left = board[1][0]
    middle_middle = board[1][1]
    middle_right = board[1][2]
    bottom_left = board[2][0]
    bottom_middle = board[2][1]
    bottom_right = board[2][2]
    x_winning_states = top_left == top_middle == top_right == 'X' \
                       or middle_left == middle_middle == middle_right == 'X' \
                       or bottom_left == bottom_middle == bottom_right == 'X' \
                       or top_right == middle_right == bottom_right == 'X' \
                       or top_middle == middle_middle == bottom_middle == 'X' \
                       or top_left == middle_left == bottom_left == 'X' \
                       or top_left == middle_middle == bottom_right == 'X' \
                       or top_right == middle_middle == bottom_left == 'X'

    o_winning_states = top_left == top_middle == top_right == 'O' \
                       or middle_left == middle_middle == middle_right == 'O' \
                       or bottom_left == bottom_middle == bottom_right == 'O' \
                       or top_right == middle_right == bottom_right == 'O' \
                       or top_middle == middle_middle == bottom_middle == 'O' \
                       or top_left == middle_left == bottom_left == 'O' \
                       or top_left == middle_middle == bottom_right == 'O' \
                       or top_right == middle_middle == bottom_left == 'O'

    full_board = True
    for row in board:
        for value in row:
            if value == -1:
                full_board = False

    if x_winning_states:
        return 1
    elif o_winning_states:
        return -1
    elif full_board:
        return 0
    else:
        return None


def possible_actions(state: TicTacToeState) -> List[TicTacToeAction]:
    """ returns all possible actions from the given state """
    possible_actions = []
    board = state.board
    for row in range(3):
        for col in range(3):
            if board[row][col] == -1:
                possible_actions.append(TicTacToeAction(row, col, state.player_turn))
    return possible_actions


def play(state: TicTacToeState, action: TicTacToeAction) -> TicTacToeState:
    """ returns the resulting state from playing the given action for the given state """
    board = copy.deepcopy(state.board)
    action_row = action.row
    action_col = action.col
    if board[action_row][action_col] == -1:
        board[action_row][action_col] = action.player

    if state.player_turn == 'X':
        new_player_state = 'O'
    else:
        new_player_state = 'X'

    return TicTacToeState(board, new_player_state)


def minimax_decision(state: TicTacToeState):
    action_utility_pairs = []
    for action in possible_actions(state):
        if state.player_turn == 'X':
            action_utility_pairs.append((action, min_value(play(state, action))))
        else:
            action_utility_pairs.append((action, max_value(play(state, action))))

    if state.player_turn == 'X':
        result = max(action_utility_pairs, key=lambda x: x[1])
    else:
        result = min(action_utility_pairs, key=lambda x: x[1])

    return result


def max_value(state: TicTacToeState) -> int:
    utility_value = utility(state)
    if utility_value is not None:
        return utility_value

    v = float("-inf")
    for action in possible_actions(state):
        v = max(v, min_value(play(state, action)))

    return v


def min_value(state: TicTacToeState) -> int:
    utility_value = utility(state)
    if utility_value is not None:
        return utility_value

    v = float("inf")
    for action in possible_actions(state):
        v = min(v, max_value(play(state, action)))

    return v


# TESTS!

# ---- CONSTANTS from ASSIGNMENT
s1_board = [[-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, 'X']]
s1 = TicTacToeState(s1_board, 'O')

s2_board = [['O', -1, -1],
            [-1, -1, -1],
            [-1, -1, 'X']]
s2 = TicTacToeState(s2_board, 'X')

s3_board = [['O', -1, -1],
            ['X', -1, -1],
            [-1, -1, 'X']]
s3 = TicTacToeState(s3_board, 'O')

s4_board = [['O', 'O', -1],
            ['X', -1, -1],
            [-1, -1, 'X']]
s4 = TicTacToeState(s4_board, 'X')

s5_board = [['O', 'O', 'X'],
            ['X', -1, -1],
            [-1, -1, 'X']]
s5 = TicTacToeState(s5_board, 'O')

s6_board = [['O', 'O', 'X'],
            ['X', -1, 'O'],
            [-1, -1, 'X']]
s6 = TicTacToeState(s6_board, 'X')

# ---- CONSTANTS
# A game that has not yet started
empty_game_board = [[-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1]]
empty_game_state = TicTacToeState(empty_game_board, 'X')

# A game that is unfinished
unfinished_game_board = [['X', 'O', 'X'],
                         [-1, 'X', -1],
                         [-1, -1, 'O']]
unfinished_game_state = TicTacToeState(unfinished_game_board, 'O')

# A game where X won
x_win_game_board = [['X', 'O', -1],
                    [-1, 'X', -1],
                    [-1, 'O', 'X']]
x_win_game_state = TicTacToeState(x_win_game_board, 'O')

# A game where O won
o_win_game_board = [['X', 'O', -1],
                    [-1, 'O', -1],
                    [-1, 'O', 'X']]
o_win_game_state = TicTacToeState(o_win_game_board, 'X')

# A game where the players tied
draw_game_board = [['O', 'X', 'O'],
                   ['X', 'O', 'O'],
                   ['X', 'O', 'X']]
draw_game_state = TicTacToeState(draw_game_board, 'X')

# ---- TESTING UTILITY
assert utility(empty_game_state) is None
assert utility(unfinished_game_state) is None
assert utility(x_win_game_state) == 1
assert utility(o_win_game_state) == -1
assert utility(draw_game_state) == 0

# ---- TESTING POSSIBLE ACTIONS
assert possible_actions(empty_game_state) \
       == [TicTacToeAction(0, 0, 'X'), TicTacToeAction(0, 1, 'X'), TicTacToeAction(0, 2, 'X'),
           TicTacToeAction(1, 0, 'X'), TicTacToeAction(1, 1, 'X'), TicTacToeAction(1, 2, 'X'),
           TicTacToeAction(2, 0, 'X'), TicTacToeAction(2, 1, 'X'), TicTacToeAction(2, 2, 'X')]

assert possible_actions(unfinished_game_state) == [TicTacToeAction(1, 0, 'O'), TicTacToeAction(1, 2, 'O'),
                                                   TicTacToeAction(2, 0, 'O'), TicTacToeAction(2, 1, 'O')]

assert possible_actions(draw_game_state) == []

# ---- TESTING PLAY
assert play(empty_game_state, TicTacToeAction(0, 0, 'X')) == TicTacToeState([[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
                                                                            'O')

assert play(unfinished_game_state, TicTacToeAction(2, 0, 'O')) \
       == TicTacToeState([['X', 'O', 'X'], [-1, 'X', -1], ['O', -1, 'O']], 'X')