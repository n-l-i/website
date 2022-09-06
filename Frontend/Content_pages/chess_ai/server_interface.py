from .src.game import Board,push_move,get_ai_move
from time import time

def get_board(board):
    str_board = {}
    rows = "87654321"
    cols = "abcdefgh"
    for i,line in enumerate(str(board).split("\n")):
        row = rows[i]
        for j,tile in enumerate(line.replace(" ","")):
            col = cols[j]
            if tile == ".":
                continue
            str_board[col+row] = tile
    return str_board

def select_mode(new_mode):
    global board, mode
    board = Board()
    if new_mode not in ("ai_vs_human","human_vs_human","ai_vs_ai"):
        return {"success": False,"message":"Not a valid game mode."},400
    mode = new_mode
    return {"success": True},200

def select_colour(colour):
    global board, mode
    board = Board()
    if colour not in ("black","white"):
        return {"success": False,"message":"Not a valid colour."},400
    if mode == "ai_vs_ai" or (mode == "ai_vs_human" and colour == "black"):
        legal_moves = []
    else:
        legal_moves = sorted([move.uci() for move in board.legal_moves])
    return {"success": True,"data":{"board":get_board(board),"legal_moves":legal_moves}},200

def make_move(move):
    global board,mode
    try:
        push_move(board,move)
    except ValueError:
        return {"success": False,"message":"Not a valid move."},200
    except:
        return {"success": False,"message":"Internal server error."+str(e)},500
    if board.outcome() is not None:
        end_reason = str(board.outcome().termination).replace("Termination.","")
        end_reason = end_reason[0].upper()+end_reason[1:].lower()
        colours = {True:"White",False:"Black",None:"Draw"}
        winner = colours[board.outcome().winner]
        return {"success": True,"data":{"move":move,"board":get_board(board),"legal_moves":[],"game_is_over":True,"end_reason":end_reason,"winner":winner}},200

    if mode == "human_vs_human":
        legal_moves = sorted([mover.uci() for mover in board.legal_moves])
    else:
        legal_moves = []
    return {"success": True,"data":{"move":move,"board":get_board(board),"legal_moves":legal_moves}},200

def let_ai_make_move():
    global board
    start_time = time()
    try:
        ai_move = get_ai_move(board).uci()
        push_move(board,ai_move)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False,"message":"Internal server error."+str(e)},500
    if board.outcome() is not None:
        end_reason = str(board.outcome().termination).replace("Termination.","")
        end_reason = end_reason[0].upper()+end_reason[1:].lower()
        colours = {True:"White",False:"Black",None:"Draw"}
        winner = colours[board.outcome().winner]
        return {"success": True,"data":{"move":ai_move,"board":get_board(board),"legal_moves":[],"game_is_over":True,"end_reason":end_reason,"winner":winner}},200

    if mode != "ai_vs_ai":
        legal_moves = sorted([move.uci() for move in board.legal_moves])
    else:
        legal_moves = []
    return {"success": True,"data":{"move":ai_move,"board":get_board(board),"legal_moves":legal_moves}},200
