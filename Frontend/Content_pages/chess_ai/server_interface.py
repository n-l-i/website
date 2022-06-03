from .src.game import Ext_board,push_move,get_ai_move
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

def select_colour(colour):
    global board
    board = Ext_board()
    if colour not in ("black","white"):
        return {"success": False,"message":"Not a valid colour."},400
    if colour != "white":
        return {"success": True,"data":{"board":get_board(board),"legal_moves":[]}},200
    legal_moves = sorted([move.uci() for move in board.legal_moves])
    return {"success": True,"data":{"board":get_board(board),"legal_moves":legal_moves}},200

def make_move(move):
    global board
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
    return {"success": True,"data":{"move":move,"board":get_board(board),"legal_moves":[]}},200

def let_ai_make_move():
    global board
    start_time = time()
    try:
        ai_move = get_ai_move(board).uci()
        push_move(board,ai_move)
    except:
        return {"success": False,"message":"Internal server error."+str(e)},500
    if board.outcome() is not None:
        return {"success": True,"data":str(outcome)},200
    legal_moves = sorted([move.uci() for move in board.legal_moves])
    print("Took time:",time()-start_time)
    return {"success": True,"data":{"move":ai_move,"board":get_board(board),"legal_moves":legal_moves}},200
