from .src.game import push_move,get_ai_move
from chess import Board
from time import time
from ...database_requests import (
    is_valid_token,
    create_chessgame,
    update_chessgame,
    delete_chessgame,
    select_chessgame
)

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

def new_chessgame(token,mode=None,colour=None):
    successful,token_is_valid = is_valid_token(token)
    if not successful:
        return {}, 500
    if not token_is_valid:
        return {"success": False,
                "message": "Valid access token needs to be provided.",
                "data": {}
                },400
    if mode not in ("ai_vs_human","human_vs_human","ai_vs_ai",None):
        return {"success": False,
                "message":"Not a valid game mode.",
                "data":{}
                },400
    if colour not in ("black","white",None):
        return {"success": False,
                "message":"Not a valid colour.",
                "data":{}
                },400
    if None in (mode,colour):
        _,previous_game = select_chessgame(token)
        if previous_game is None:
            previous_game = {"mode":"ai_vs_human","colour":"white"}
        if mode is None:
            mode = previous_game["mode"]
        if colour is None:
            colour = previous_game["colour"]
    mode = mode.lower()
    colour = colour.lower()
    board = Board()
    game = {"board":board.fen(),"mode":mode,"colour":colour}
    success,_ = create_chessgame(token,game["board"],game["mode"],game["colour"])
    assert success
    if game["mode"] == "ai_vs_ai" or (game["mode"] == "ai_vs_human" and game["colour"] == "black"):
        legal_moves = []
    else:
        legal_moves = sorted([move.uci() for move in board.legal_moves])
    print(game["mode"])
    _,game = select_chessgame(token)
    print(game["mode"])
    return {"success": True,
            "message":None,
            "data":{"board":get_board(board),"legal_moves":legal_moves}
            },200

def make_move(move,token):
    _,game = select_chessgame(token)
    if game is None:
        return {"success": False,
                "message":"No game started.",
                "data":{}
                },400
    board = Board(game["board"])
    try:
        push_move(board,move)
        update_chessgame(token,board.fen())
    except ValueError:
        return {"success": False,
                "message":"Not a valid move.",
                "data":{}
                },400
    except:
        return {},500
    if board.outcome() is not None:
        delete_chessgame(token)
        end_reason = str(board.outcome().termination).replace("Termination.","")
        end_reason = end_reason[0].upper()+end_reason[1:].lower()
        colours = {True:"White",False:"Black",None:"Draw"}
        winner = colours[board.outcome().winner]
        return {"success": True,
                "message":None,
                "data":{"move":move,"board":get_board(board),"legal_moves":[],"game_is_over":True,"end_reason":end_reason,"winner":winner}
                },200

    if game["mode"] == "human_vs_human":
        legal_moves = sorted([mover.uci() for mover in board.legal_moves])
    else:
        legal_moves = []
    return {"success": True,
            "message":None,
            "data":{"move":move,"board":get_board(board),"legal_moves":legal_moves}
            },200

def let_ai_make_move(thinking_time,token):
    successful,token_is_valid = is_valid_token(token)
    if not successful:
        return {}, 500
    if not token_is_valid:
        return {"success": False,
                "message": "Valid access token needs to be provided.",
                "data": {}
                },400
    _,game = select_chessgame(token)
    if game is None:
        return {"success": False,
                "message":"No game started.",
                "data":{}
                },400
    board = Board(game["board"])
    try:
        ai_move = get_ai_move(board,thinking_time).uci()
        push_move(board,ai_move)
        update_chessgame(token,board.fen())
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
    if game["mode"] != "ai_vs_ai":
        legal_moves = sorted([move.uci() for move in board.legal_moves])
    else:
        legal_moves = []
    return {"success": True,
            "message":None,
            "data":{"move":ai_move,"board":get_board(board),"legal_moves":legal_moves}
            },200
