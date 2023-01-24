from .src.game import push_move,get_ai_move
from chess import Board
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

def select_mode(new_mode,session):
    if "board" not in session:
        session["board"] = Board().fen()
    if "mode" not in session:
        session["mode"] = "ai_vs_human"
    board = Board(session["board"])
    if new_mode not in ("ai_vs_human","human_vs_human","ai_vs_ai"):
        return {"success": False,
                "message":"Not a valid game mode.",
                "data":{}
                },400
    session["mode"] = new_mode
    return {"success": True,
            "message":None,
            "data":{}
            },200

def select_colour(colour,session):
    if "mode" not in session:
        session["mode"] = "ai_vs_human"
    session["board"] = Board().fen()
    board = Board(session["board"])
    if colour not in ("black","white"):
        return {"success": False,
                "message":"Not a valid colour.",
                "data":{}
                },400
    if session["mode"] == "ai_vs_ai" or (session["mode"] == "ai_vs_human" and colour == "black"):
        legal_moves = []
    else:
        legal_moves = sorted([move.uci() for move in board.legal_moves])
    return {"success": True,
            "message":None,
            "data":{"board":get_board(board),"legal_moves":legal_moves}
            },200

def make_move(move,session):
    if "board" not in session:
        session["board"] = Board().fen()
    if "mode" not in session:
        session["mode"] = "ai_vs_human"
    board = Board(session["board"])
    try:
        push_move(board,move)
        session["board"] = board.fen()
    except ValueError:
        return {"success": False,
                "message":"Not a valid move.",
                "data":{}
                },400
    except:
        return {},500
    if board.outcome() is not None:
        end_reason = str(board.outcome().termination).replace("Termination.","")
        end_reason = end_reason[0].upper()+end_reason[1:].lower()
        colours = {True:"White",False:"Black",None:"Draw"}
        winner = colours[board.outcome().winner]
        return {"success": True,
                "message":None,
                "data":{"move":move,"board":get_board(board),"legal_moves":[],"game_is_over":True,"end_reason":end_reason,"winner":winner}
                },200

    if session["mode"] == "human_vs_human":
        legal_moves = sorted([mover.uci() for mover in board.legal_moves])
    else:
        legal_moves = []
    return {"success": True,
            "message":None,
            "data":{"move":move,"board":get_board(board),"legal_moves":legal_moves}
            },200

def let_ai_make_move(thinking_time,session):
    if "board" not in session:
        session["board"] = Board().fen()
    if "mode" not in session:
        session["mode"] = "ai_vs_human"
    board = Board(session["board"])
    try:
        ai_move = get_ai_move(board,thinking_time).uci()
        push_move(board,ai_move)
        session["board"] = board.fen()
    except:
        return {},500
    if board.outcome() is not None:
        end_reason = str(board.outcome().termination).replace("Termination.","")
        end_reason = end_reason[0].upper()+end_reason[1:].lower()
        colours = {True:"White",False:"Black",None:"Draw"}
        winner = colours[board.outcome().winner]
        return {"success": True,
                "message":None,
                "data":{"move":ai_move,"board":get_board(board),"legal_moves":[],"game_is_over":True,"end_reason":end_reason,"winner":winner}
                },200

    if session["mode"] != "ai_vs_ai":
        legal_moves = sorted([move.uci() for move in board.legal_moves])
    else:
        legal_moves = []
    return {"success": True,
            "message":None,
            "data":{"move":ai_move,"board":get_board(board),"legal_moves":legal_moves}
            },200
