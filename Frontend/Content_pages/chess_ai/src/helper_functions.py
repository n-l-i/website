from random import uniform
import chess

def get_parameters(board,colour):
    parameters = {}
    pieces = get_pieces(board)
    parameters["friend_pieces"] = 0
    for _,piece in pieces[colour]:
        if piece.piece_type == chess.PAWN:
            parameters["friend_pieces"] += 1
        if piece.piece_type == chess.KNIGHT:
            parameters["friend_pieces"] += 3
        if piece.piece_type == chess.BISHOP:
            parameters["friend_pieces"] += 3
        if piece.piece_type == chess.ROOK:
            parameters["friend_pieces"] += 5
        if piece.piece_type == chess.QUEEN:
            parameters["friend_pieces"] += 9
    parameters["enemy_pieces"] = 0
    for _,piece in pieces[not colour]:
        if piece.piece_type == chess.PAWN:
            parameters["enemy_pieces"] += 1
        if piece.piece_type == chess.KNIGHT:
            parameters["enemy_pieces"] += 3
        if piece.piece_type == chess.BISHOP:
            parameters["enemy_pieces"] += 3
        if piece.piece_type == chess.ROOK:
            parameters["enemy_pieces"] += 5
        if piece.piece_type == chess.QUEEN:
            parameters["enemy_pieces"] += 9
    attacked_tiles = get_attacked_tiles(board)
    parameters["friend_attacked_tiles"] = len(attacked_tiles[colour])
    parameters["friend_attacked_pieces"] = 0
    for _,piece in attacked_tiles[colour]:
        if piece is None:
            continue
        if piece.piece_type == chess.PAWN:
            parameters["friend_attacked_pieces"] += 1
        if piece.piece_type == chess.KNIGHT:
            parameters["friend_attacked_pieces"] += 3
        if piece.piece_type == chess.BISHOP:
            parameters["friend_attacked_pieces"] += 3
        if piece.piece_type == chess.ROOK:
            parameters["friend_attacked_pieces"] += 5
        if piece.piece_type == chess.QUEEN:
            parameters["friend_attacked_pieces"] += 9
    parameters["enemy_attacked_tiles"] = len(attacked_tiles[not colour])
    parameters["enemy_attacked_pieces"] = 0
    for _,piece in attacked_tiles[not colour]:
        if piece is None:
            continue
        if piece.piece_type == chess.PAWN:
            parameters["enemy_attacked_pieces"] += 1
        if piece.piece_type == chess.KNIGHT:
            parameters["enemy_attacked_pieces"] += 3
        if piece.piece_type == chess.BISHOP:
            parameters["enemy_attacked_pieces"] += 3
        if piece.piece_type == chess.ROOK:
            parameters["enemy_attacked_pieces"] += 5
        if piece.piece_type == chess.QUEEN:
            parameters["enemy_attacked_pieces"] += 9
    parameters["friend_centre"] = 0
    for square,_ in pieces[colour]:
        file_factor = chess.square_file(square)
        if file_factor > 3:
            file_factor = 7-file_factor
        rank_factor = chess.square_rank(square)
        if rank_factor > 3:
            rank_factor = 7-rank_factor
        parameters["friend_centre"] += file_factor*rank_factor
    parameters["enemy_centre"] = 0
    for square,_ in pieces[not colour]:
        file_factor = chess.square_file(square)
        if file_factor > 3:
            file_factor = 7-file_factor
        rank_factor = chess.square_rank(square)
        if rank_factor > 3:
            rank_factor = 7-rank_factor
        parameters["enemy_centre"] += file_factor*rank_factor
    return parameters

def get_pieces(self):
    pieces = { chess.WHITE:[],chess.BLACK:[] }
    for square in chess.SQUARES:
        if self.color_at(square) is not None:
            pieces[self.color_at(square)].append((square,self.piece_at(square)))
    return pieces

def get_attacked_tiles(self):
    attacked_tiles = { chess.WHITE:set(),chess.BLACK:set() }
    for square in chess.SQUARES:
        if self.color_at(square) is not None:
            for attacked_tile in self.attacks(square):
                attacked_tiles[self.color_at(square)].add((attacked_tile,self.piece_at(square)))
    return attacked_tiles

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

