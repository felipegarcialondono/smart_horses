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
        self._turn = Turn.PLAYER
        self._destroyed_squares = set()
        self._board, self._computer_pos, self._player_pos, self._special_squares = self._initialize_board()

        self._computer_points = 0
        self._player_points = 0

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