from enum import Enum
from app.utils.constants import *
import random
from dataclasses import dataclass

class Turn(Enum):
    COMPUTER = 1
    PLAYER = 2

class CellType(Enum):
    EMPTY = 0
    COMPUTER = 1
    PLAYER = 2
    DESTROYED = 3
    SPECIAL = 4

@dataclass
class Cell:
    type: CellType
    value: int | None = None

class Match():
    def __init__(self):
        self._turn = Turn.COMPUTER
        self._destroyed_squares = set()
        self._board, self._computer_pos, self._player_pos, self._special_squares = self._initialize_board()

        self._computer_points = 0
        self._player_points = 0

        self._finished = False
        self._winner = None

    def _initialize_board(self):
        board = [[Cell(CellType.EMPTY) for _ in range(COLS)] for _ in range(ROWS)]

        unique_squares = random.sample([(r, c) for r in range(ROWS) for c in range(COLS)], len(VALUES_SQUARES) + 2)

        computer_pos, player_pos, *special_positions = unique_squares

        i, j = computer_pos
        board[i][j] = Cell(CellType.COMPUTER)
        
        i, j = player_pos
        board[i][j] = Cell(CellType.PLAYER)

        special_squares = {pos: value for pos, value in zip(special_positions, VALUES_SQUARES)}

        for pos, value in special_squares.items():
            i, j = pos
            board[i][j] = Cell(CellType.SPECIAL, value)
        
        return board, computer_pos, player_pos, special_squares
    
    @property
    def board(self):
        return self._board
    

    def play_turn(self, pos:tuple[int]):
        i, j = pos
        i_cur, j_cur = self._computer_pos if self._turn == Turn.COMPUTER else self._player_pos

        cell: Cell = self._board[i][j]

        if not (0 <= i < ROWS and 0 <= j < COLS):
                return False
            
        if cell.type in (CellType.DESTROYED, CellType.COMPUTER, CellType.PLAYER):
            return False
        
        delta = (i - i_cur, j - j_cur)

        if delta not in KNIGHT_MOVES:
            return False

        self._destroyed_squares.add((i_cur, j_cur))
        self._board[i_cur][j_cur] = Cell(CellType.DESTROYED)

        if cell.type == CellType.SPECIAL:
            if self._turn == Turn.COMPUTER:
                self._computer_points += cell.value
            else:
                self._player_points += cell.value

        if self._turn == Turn.COMPUTER:
            self._computer_pos = pos
            self._board[i][j] = Cell(CellType.COMPUTER)
            self._turn = Turn.PLAYER
        else:
            self._player_pos = pos
            self._board[i][j] = Cell(CellType.PLAYER)
            self._turn = Turn.COMPUTER
    
        return True
    
    def available_moves_from(self, pos):
        """Lista de todas las posiciones legales no destruidas"""
        moves = []
        for (di,dj) in KNIGHT_MOVES:
            new_i, new_j = pos[0] + di, pos[1] + dj
            if 0 <= new_i < ROWS and 0 <= new_j < COLS and (new_i,new_j) not in self._destroyed_squares:
                cell = self.board[new_i][new_j]
                if cell.type not in (CellType.DESTROYED, CellType.COMPUTER, CellType.PLAYER):
                    moves.append((new_i, new_j))
        return moves
    
    def _check(self):
        """
        1. Si el jugador en turno NO tiene mov legales pierde, el que si tenga mov legales
        posibles gana.
        2. Si no hay casillas disponibles
        """

        moves_computer = self.available_moves_from(self._computer_pos)
        moves_player = self.available_moves_from(self._player_pos)

        if not moves_computer and not moves_player:
            self._finished = True
            if self._computer_points > self._player_points:
                self._winner = Turn.COMPUTER
            elif self._player_points > self._computer_points:
                self._winner = Turn.PLAYER
            else:
                self._winner = None
            return
        
        if self._turn == Turn.COMPUTER and not moves_computer:
            self._finished = True
            self._winner = Turn.PLAYER
            return
        elif self._turn == Turn.PLAYER and not moves_player:
            self._finished = True
            self._winner = Turn.COMPUTER
            return
    
    def is_finished(self):
        return self._finished
    
    def is_winner(self):
        return self._winner
    
    @property
    def computer_points(self):
        return self.computer_points
    
    @property
    def player_points(self):
        return self._player_points
    
    @property
    def computer_pos(self):
        return self.computer_pos
    
    @property
    def player_pos(self):
        return self.player_pos
    
    @property
    def turn(self):
        return self._turn