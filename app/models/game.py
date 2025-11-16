from abc import ABC, abstractmethod
from app.utils.constants import *
from app.models.node import *

class Game():
    def __init__(self, state_initial):
        self._state_initial = state_initial

    def state_initial(self):
        return self._state_initial

    def operators(self, node: Node):
        state = node.state
        type = node.type
        destroyed_squares = state.destroyed_squares
        special_squares = state.special_squares

        pos, points = (state.pos_max, state.pts_max) if type == NodeType.MAX else (state.pos_min, state.pts_min)
        i, j = pos

        next_nodes = []

        for (di, dj) in KNIGHT_MOVES:
            new_i, new_j = i + di, j + dj

            if 0 <= new_i < ROWS and 0 <= new_j < COLS and (new_i, new_j) not in destroyed_squares:
                new_pos = (new_i, new_j)

                square_points = state.special_squares.get(new_pos, 0)

                new_pts = points + square_points

                new_state = State(
                    pts_min=new_pts if type == NodeType.MIN else state.pts_min,
                    pts_max=new_pts if type == NodeType.MAX else state.pts_max,
                    pos_min=new_pos if type == NodeType.MIN else state.pos_min,
                    pos_max=new_pos if type == NodeType.MAX else state.pos_max,
                    destroyed_squares=destroyed_squares | {pos},
                    special_squares=special_squares
                )
        
                new_node = Node(
                    type=NodeType.MAX if type == NodeType.MIN else NodeType.MIN,
                    parent=node,
                    state=new_state,
                    depth=node.depth + 1,
                    utility=self._utility(new_state),  # ✅ Cambiar state por new_state
                )

                next_nodes.append(new_node)
        
        return next_nodes

    def is_terminal(self, node: Node) -> bool:
        """
        Verifica si el nodo es terminal (no hay más movimientos posibles para el jugador actual)
        """
        # Determinar qué jugador debe moverse
        pos = node.state.pos_max if node.type == NodeType.MAX else node.state.pos_min
        destroyed = node.state.destroyed_squares

        # Verificar si existe al menos un movimiento legal
        for (di, dj) in KNIGHT_MOVES:
            new_i, new_j = pos[0] + di, pos[1] + dj
            if 0 <= new_i < ROWS and 0 <= new_j < COLS and (new_i, new_j) not in destroyed: 
                return False  # Hay al menos un movimiento legal
            
        return True  # No hay movimientos legales, es terminal

    def _utility(self, state: State) -> int:
        """
        Función de utilidad: diferencia de puntos desde la perspectiva de MAX (computadora)
        """
        return state.pts_max - state.pts_min