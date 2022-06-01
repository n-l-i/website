from .src.game import Ext_board,push_move,get_ai_move

def get_board(board):
    str_board = str(board)
    new_str_board = "<pre>    A B C D E F G H\n"
    for i,line in enumerate(str_board.split("\n")):
        new_str_board += f"\n{8-i}   {line}   {8-i}"
    new_str_board += "\n\n    A B C D E F G H</pre>"
    for i,move in enumerate(board.move_stack):
        if i%2==0:
            new_str_board += "\nWhite: "
        else:
            new_str_board += ", Black: "
        new_str_board += move.uci()
    return new_str_board

def select_colour(colour):
    global board
    board = Ext_board()
    if colour not in ("black","white"):
        return {"success": False,"message":"Not a valid colour."},400
    if colour != "white":
        try:
            ai_move = get_ai_move(board).uci()
            push_move(board,ai_move)
        except:
            return {"success": False,"message":"Internal server error."},500
    legal_moves = sorted([move.uci() for move in board.legal_moves])
    return {"success": True,"data":{"board":get_board(board).replace("\n","<br>"),"legal_moves":legal_moves}},200

def make_move(move):
    global board
    try:
        push_move(board,move)
    except ValueError:
        return {"success": False,"message":"Not a valid move."},200
    except Exception as e:
        return {"success": False,"message":"Internal server error."+str(e)},500
    try:
        ai_move = get_ai_move(board).uci()
        push_move(board,ai_move)
    except Exception as e:
        return {"success": False,"message":"Internal server error."+str(e)},500
    if board.outcome() is not None:
        return {"success": True,"data":str(outcome)},200
    legal_moves = sorted([move.uci() for move in board.legal_moves])
    return {"success": True,"data":{"board":get_board(board).replace("\n","<br>"),"legal_moves":legal_moves}},200
