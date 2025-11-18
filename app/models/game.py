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

            # ✅ Verificar que la nueva posición no esté destruida ni ocupada por algún jugador
            if (0 <= new_i < ROWS and 
                0 <= new_j < COLS and 
                (new_i, new_j) not in destroyed_squares and
                (new_i, new_j) != state.pos_max and  # ✅ No moverse a la posición del MAX
                (new_i, new_j) != state.pos_min):    # ✅ No moverse a la posición del MIN
                
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
                    utility=self._utility(new_state),
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

    def _utility(self, state):
        # Pesos (se pueden modificar para cambiar la "personalidad" de la IA)
        W_SCORE = 1.0
        W_POTENTIAL = 0.5  # Menos importante que el score actual
        W_MOVILITY = 0.1  # Menos importante que el score
        
        # Componente 1: Puntuación Actual
        C1 = state.pts_max - state.pts_min
        
        # Componente 2: Potencial de Puntuación
        machine_potential = 0
        human_potential = 0
        
        for square_pos, points in state.special_squares.items():
            # Verificar si la casilla está activa (no destruida)
            if square_pos not in state.destroyed_squares:
                # Verificar si la máquina puede saltar a esta casilla
                if self._can_jump_to(state.pos_max, square_pos, state.destroyed_squares):
                    if points > 0:
                        machine_potential += points
                
                # Verificar si el humano puede saltar a esta casilla
                if self._can_jump_to(state.pos_min, square_pos, state.destroyed_squares):
                    if points > 0:
                        human_potential += points
        
        C2 = machine_potential - human_potential
        
        # Componente 3: Movilidad
        machine_moves = self._count_valid_moves(state.pos_max, state.destroyed_squares)
        human_moves = self._count_valid_moves(state.pos_min, state.destroyed_squares)
        C3 = machine_moves - human_moves
        
        # Resultado Final
        total_heuristic = (W_SCORE * C1) + (W_POTENTIAL * C2) + (W_MOVILITY * C3)
        
        return int(total_heuristic)
    
    def _can_jump_to(self, from_pos, to_pos, destroyed_squares):
        """Verifica si desde from_pos se puede hacer un movimiento de caballo válido a to_pos"""
        from_i, from_j = from_pos
        to_i, to_j = to_pos
        
        # Calcular el delta del movimiento
        delta = (to_i - from_i, to_j - from_j)
        
        # Verificar si es un movimiento válido de caballo
        if delta not in KNIGHT_MOVES:
            return False
        
        # Verificar que la casilla destino no esté destruida
        if to_pos in destroyed_squares:
            return False
        
        # Verificar que esté dentro de los límites del tablero
        if not (0 <= to_i < ROWS and 0 <= to_j < COLS):
            return False
        
        return True
    
    def _count_valid_moves(self, pos, destroyed_squares):
        """Cuenta cuántos movimientos válidos hay desde una posición"""
        i, j = pos
        count = 0
        
        for (di, dj) in KNIGHT_MOVES:
            new_i, new_j = i + di, j + dj
            
            # Verificar que esté dentro de los límites y no esté destruida
            if 0 <= new_i < ROWS and 0 <= new_j < COLS and (new_i, new_j) not in destroyed_squares:
                count += 1
        
        return count