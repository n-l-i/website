from random import sample,uniform
from chess import Board,BLACK,WHITE,SQUARES
import chess
from time import sleep,time
import signal
from hashlib import sha256
from .minmax_ai import score_moves_minmax as ai

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

class Ext_board(Board):
    def get_pieces(self):
        pieces = { WHITE:[],BLACK:[] }
        for square in SQUARES:
            if self.color_at(square) is not None:
                pieces[self.color_at(square)].append((square,self.piece_at(square)))
        return pieces
    
    def get_attacked_tiles(self):
        attacked_tiles = { WHITE:set(),BLACK:set() }
        for square in SQUARES:
            if self.color_at(square) is not None:
                for attacked_tile in self.attacks(square):
                    attacked_tiles[self.color_at(square)].add((attacked_tile,self.piece_at(square)))
        return attacked_tiles
    
    def leader(self):
        pieces = self.get_pieces()
        points = { WHITE:0,BLACK:0 }
        for colour in (WHITE,BLACK):
            for _,piece in pieces[colour]:
                if piece.piece_type == chess.PAWN:
                    points[colour] += 1
                if piece.piece_type == chess.KNIGHT:
                    points[colour] += 3
                if piece.piece_type == chess.BISHOP:
                    points[colour] += 3
                if piece.piece_type == chess.ROOK:
                    points[colour] += 5
                if piece.piece_type == chess.QUEEN:
                    points[colour] += 9
        if points[WHITE] > points[BLACK]:
            return WHITE
        if points[WHITE] < points[BLACK]:
            return BLACK
        return None

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
