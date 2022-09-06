import chess
from .ai import Ai
from random import choice

def push_move(board,move,):
    move = chess.Move.from_uci(move)
    if move not in board.legal_moves:
        raise ValueError
    board.push(move)
    return board

def get_ai_move(board):
    ai = Ai("ai")
    ai.set_colour(board.turn)
    depth = choice((3,))
    scored_moves = ai.score_moves(board,depth)
    ai_move = choose_move(scored_moves)
    return ai_move

def choose_move(scored_moves):
    scored_moves = sorted(scored_moves,key=lambda x: x[1],reverse=True)
    # If there are only five moves or fewer, always pick the best move
    if len(scored_moves) <= 5:
        return scored_moves[0][0]
    # Keep only the best third of all moves
    scored_moves = scored_moves[:int(len(scored_moves)/3)]
    # Normalise all scores to start from zero
    lowest_score = scored_moves[-1][1]
    scored_moves = [(move,score-lowest_score) for (move,score) in scored_moves]
    highest_score = scored_moves[0][1]
    # Maybe all moves are equally good, if so pick a random one
    if highest_score == 0:
        return choice(scored_moves)[0]
    # Normalise all scores to be in the range 0-1
    scored_moves = [(move,score/highest_score) for (move,score) in scored_moves]
    # Make sure all moves have a score that is at least 1% of the best
    scored_moves = [(move,score*0.99+0.01) for (move,score) in scored_moves]
    # Pick a move based on their scores, higher scores = more likely picked
    moves = []
    accumulative_score = 0
    for move,score in scored_moves:
        accumulative_score += score
        moves.append([move,accumulative_score])
    n = uniform(0,accumulative_score)
    for move,score in moves:
        if score >= n:
            return move
    raise Exception
