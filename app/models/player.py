from app.utils.constants import KNIGHT_MOVES, ROWS, COLS
from app.models.match import CellType

class Player:
    def __init__(self, match):
        self.match = match
    
    def get_valid_moves(self, current_pos):
        """Retorna las posiciones válidas donde el jugador puede moverse"""
        valid_moves = []
        i_cur, j_cur = current_pos
        
        for (di, dj) in KNIGHT_MOVES:
            new_i, new_j = i_cur + di, j_cur + dj
            
            # Verificar límites del tablero
            if not (0 <= new_i < ROWS and 0 <= new_j < COLS):
                continue
            
            cell = self.match.board[new_i][new_j]
            
            # Verificar que la casilla no esté destruida, ni ocupada
            if cell.type not in (CellType.DESTROYED, CellType.COMPUTER, CellType.PLAYER):
                valid_moves.append((new_i, new_j))
        
        return valid_moves
    
    def get_path_to_square(self, current_pos, target_pos):
        """
        Retorna las casillas que forman el camino en L desde current_pos hasta target_pos
        """
        i_cur, j_cur = current_pos
        i_target, j_target = target_pos
        
        path = []
        
        # Calcular el delta
        di = i_target - i_cur
        dj = j_target - j_cur
        
        # Construir el camino en L
        if abs(di) == 2:  # Se mueve 2 casillas verticalmente
            step = 1 if di > 0 else -1
            path.append((i_cur + step, j_cur))
            path.append((i_cur + 2*step, j_cur))
            path.append((i_cur + 2*step, j_cur + dj))
            
        elif abs(dj) == 2:  # Se mueve 2 casillas horizontalmente
            step = 1 if dj > 0 else -1
            path.append((i_cur, j_cur + step))
            path.append((i_cur, j_cur + 2*step))
            path.append((i_cur + di, j_cur + 2*step))
        
        return path