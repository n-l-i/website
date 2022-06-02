import chess
from .multi_execute import multiprocess

def get_score(board,colour):
    if board.is_stalemate():
        return 0
    if board.is_checkmate():
        if board.outcome().winner == colour:
            return 100
        else:
            return -100
    score = 0
    pieces = board.get_pieces()
    for tile,piece in pieces[colour]:
        score += len(board.attacks(tile))/200
        if piece.piece_type == chess.PAWN:
            score += 1
        if piece.piece_type == chess.KNIGHT:
            score += 3
        if piece.piece_type == chess.BISHOP:
            score += 3
        if piece.piece_type == chess.ROOK:
            score += 5
        if piece.piece_type == chess.QUEEN:
            score += 9
    for tile,piece in pieces[not colour]:
        score -= len(board.attacks(tile))/50
        if piece.piece_type == chess.PAWN:
            score -= 1
        if piece.piece_type == chess.KNIGHT:
            score -= 3
        if piece.piece_type == chess.BISHOP:
            score -= 3
        if piece.piece_type == chess.ROOK:
            score -= 5
        if piece.piece_type == chess.QUEEN:
            score -= 9
    return score

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
    parameters = []
    for move in board.legal_moves:
        board.push(move)
        parameters.append({"board":board,"colour":not board.turn,"n_moves":2,"previous_move":move})
        board.pop()
    moves = multiprocess(minmax_score,parameters,10)
    # Normalise scores
    return normalise(moves)

def minmax_score(board,colour,n_moves,previous_move):
    if n_moves == 0 or board.is_stalemate() or board.is_checkmate():
        return (get_score(board,colour),previous_move)
    best_score = None
    #moves = []
    #for move in board.pseudo_legal_moves:
        #board.push(move)
        #score = get_score(board,colour)
        #board.pop()
        #moves.append([score,move])
    #moves = sorted(moves,key=lambda x: x[0],reverse=board.turn==colour)[:n_moves+1]
    for move in board.legal_moves:
        board.push(move)
        score,_ = minmax_score(board,colour,n_moves-1,previous_move)
        board.pop()
        if best_score is None:
            best_score = score
        if board.turn != colour and score < best_score:
            best_score = score
        if board.turn == colour and score > best_score:
            best_score = score
    return (best_score,previous_move)
