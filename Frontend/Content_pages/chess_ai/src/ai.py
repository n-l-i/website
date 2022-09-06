
from random import uniform
from .helper_functions import get_parameters
from .minimax import Minimax

class Ai():
    def __init__(self,name):
        self.colour = None
        a = uniform(0,1)
        self.weights = (a,1-a)
        self.name = f"{name} {self.weights}"
    
    def set_colour(self,colour):
        self.colour = colour

    def score_moves(self,board,depth):
        minimax = Minimax(board)
        scores = minimax.score(depth)
        scores = sorted(scores,key=lambda x: x[1],reverse=True)
        return scores
