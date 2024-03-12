"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


class InvalidMoveError(Exception):
    """
    Raise an error when an invalid move is made in a game.
    """
    def __init__(self, message):
        super().__init__(message)


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    
    # Count number of X and O in board
    count_X = sum(row.count('X') for row in board)
    count_O = sum(row.count('O') for row in board)

    if count_O < count_X:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    # Check for EMPTY cells in board
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.add((i,j))

    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]
    valid_moves = [0, 1, 2]

    ## Check if a move is valid
    if i not in valid_moves or j not in valid_moves:
        raise InvalidMoveError('The move is not valid. The index is out of range.')
    elif board[i][j] != EMPTY:
        raise InvalidMoveError('The move is not valid. The cell is already taken.')

    # Create a deepcopy of board
    board_dp = copy.deepcopy(board)

    # Make the move
    board_dp[i][j] = player(board)

    return board_dp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Verify if there was a winner horizontally
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O
    
    # Verify if there was a winner vertically
    for j in range(len(board)):
        column = []
        for row in board:
            column.append(row[j])
        if column.count(X) == 3:
            return X
        elif column.count(O) == 3:
            return O

    # Verify if there was a winner on the diagonal
    first_diagonal = [board[i][i] for i in range(len(board))]
    second_diagonal = [board[i][len(board) - 1 - i] for i in range(len(board))]

    if first_diagonal.count(X) == 3 or second_diagonal.count(X) == 3:
        return X
    elif first_diagonal.count(O) == 3 or second_diagonal.count(O) == 3:
        return O
    
    # If there was no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    elif sum(row.count(EMPTY) for row in board) == 0:
        return True
    else:
        return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    

def max_value(board):

    v = float('-inf')

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v

def min_value(board):

    v = float('inf')

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        highest_value = float('-inf')
        for possible_action in actions(board):
            min_result =  min_value(result(board, possible_action))
            if min_result > highest_value:
                highest_value = min_result
                action =  possible_action
        
        return action
    
    else:
        lowest_value = float('inf')
        for possible_action in actions(board):
            max_result =  max_value(result(board, possible_action))
            if max_result < lowest_value:
                lowest_value = max_result
                action =  possible_action
        
        return action
    










