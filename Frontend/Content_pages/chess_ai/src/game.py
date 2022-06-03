from random import sample,uniform
from chess import Board,BLACK,WHITE,SQUARES
import chess
from time import sleep,time
import signal
from hashlib import sha256
from .minmax_ai import score_moves_minmax as ai
from .ext_board import Ext_board

def alarm_handler(signum, frame):
    raise TimeoutExpired

def push_move(board,move,):
    move = chess.Move.from_uci(move)
    if move not in board.legal_moves:
        raise ValueError
    board.push(move)
    return board

def get_ai_move(board):
    scored_moves = ai(board)
    ai_move = choose_move(scored_moves)
    return ai_move

def choose_move(scored_moves):
    moves = []
    accumulative_score = 0
    for score,move in scored_moves[:3]:
        accumulative_score += score
        moves.append([accumulative_score,move])
    n = uniform(0,accumulative_score)
    for score,move in moves:
        if score >= n:
            return move
    raise Exception
