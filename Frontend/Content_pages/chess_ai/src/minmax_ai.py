import chess
from .multi_execute import multiprocess
from multiprocessing import current_process
from copy import deepcopy as copy
from functools import lru_cache as cache
from .ext_board import Ext_board

@cache(maxsize=131072)
def get_score(board_fen,colour):
    board = Ext_board(board_fen)
    if board.is_stalemate():
        return 0
    if board.is_checkmate():
        if board.outcome().winner == colour:
            return 100
        else:
            return -100
    piece_values = {chess.PAWN:1,
                    chess.KNIGHT:3,
                    chess.BISHOP:3,
                    chess.ROOK:5,
                    chess.QUEEN:9,
                    chess.KING:0
                   }
    score = 0
    pieces = board.get_pieces()
    for tile,piece in pieces[colour]:
        score += piece_values[piece.piece_type]
    for tile,piece in pieces[not colour]:
        score -= piece_values[piece.piece_type]
    attacked_tiles = board.get_attacked_tiles()
    for _,piece in attacked_tiles[colour]:
        score += piece_values[piece.piece_type]/128
    for _,piece in attacked_tiles[not colour]:
        score += piece_values[piece.piece_type]/64
    return round(score,8)

def normalise(scored_moves):
    moves = sorted(scored_moves,key=lambda x: x[0],reverse=True)
    for i,move in enumerate(moves):
        moves[i] = [move[0]-moves[-1][0],move[1]]
    total = sum([score for score,_ in moves])
    if total == 0:
        total = 1
    for i in range(len(moves)):
        moves[i][0] = moves[i][0]/total
    return moves

def score_moves_minmax(board):
    # Give every move a random score
    colour = board.turn
    parameters = []
    for move in board.legal_moves:
        board.push(move)
        parameters.append([move,{"board_fen":board.board_fen(),"colour":colour,"n_moves":4}])
        board.pop()
    moves = multiprocess(minmax_score,parameters,10)
    # Normalise scores
    return normalise(moves)

@cache(maxsize=131072)
def minmax_score(board_fen,colour,n_moves):
    if n_moves == 0:
        return get_score(board_fen,colour)
    board = Ext_board(board_fen)
    if board.is_stalemate() or board.is_checkmate():
        return get_score(board_fen,colour)
    moves = []
    for move in board.legal_moves:
        board.push(move)
        score = get_score(board.board_fen(),colour)
        board.pop()
        moves.append([score,move])
    moves = sorted(moves,key=(lambda x: x[0]),reverse=board.turn==colour)[:max(3,int(len(moves)/5))]
    moves = [move for _,move in moves]
    max_score = None
    min_score = None
    for move in moves:
        board.push(move)
        score = minmax_score(board.board_fen(),colour,n_moves-1)
        board.pop()
        if min_score is None or score < min_score:
            min_score = score
        if max_score is None or score > max_score:
            max_score = score
    if board.turn == colour:
        best_score = min_score
    if board.turn != colour:
        best_score = max_score
    return best_score
