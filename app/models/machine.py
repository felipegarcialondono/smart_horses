from app.models.node import Node, NodeType, State
from app.models.game import Game
from app.models.match import Turn
from app.utils.constants import *
import math

class Machine:
    def __init__(self, difficulty=AMATEUR):
        if difficulty == BEGGINER:
            self.max_depth = 2
        elif difficulty == AMATEUR:
            self.max_depth = 4
        else:
           self.max_depth = 6
        
        self.game = Game(None)

    def _build_root(self, match):
        """Para construir el nodo raiz a partir del Match, se toma la máquina como MAX"""
        state = State(
            pts_min= match._player_points,
            pts_max=match._computer_points,
            pos_min=match._player_pos,
            pos_max=match._computer_pos,
            destroyed_squares=frozenset(match._destroyed_squares),
            special_squares= match._special_squares
        )

        root = Node(
            type=NodeType.MAX if match._turn == Turn.COMPUTER else NodeType.MIN,
            parent=None,
            state=state,
            depth=0,
            utility=0
        )
        return root
    
    def choose_game(self,match):
        """devuelve la posicion (i,j) para la maquina, si no hay mov legales devuelve None"""
        root = self._build_root(match)
        self.game = Game(root.state)

        best_val = -math.inf
        best_move = None

        for child in self.game.operators(root):
            val = self._min_value(child, -math.inf, math.inf)
            #child.state._pos_max es la nueva posicion maxima
            # si child.type fue MIN significa que el mov fue hecho por MAX quedo guardada en child.state.pos_max
            if val > best_val:
                best_val = val
                if root.type == NodeType.MAX:
                    best_move = child.state.pos_max
                else:
                    best_move = child.state.pos_min

        return best_move
    
    def _max_value(self, node:Node, alpha, beta):

        v = -math.inf
        for child in self.game.operators(node):
            v = max(v, self._min_value(child, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha,v)
        return v
    
    def _min_value(self, node:Node, alpha, beta):

        v = math.inf
        for child in self.game.operators(node):
            v = min(v, self._max_value(child, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
