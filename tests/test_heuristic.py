import sys
import os

# Asegurar que el directorio del proyecto esté en sys.path para importar el paquete `app`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.game import Game
from app.models.node import State
from app.utils.constants import KNIGHT_MOVES, ROWS, COLS


def block_moves_for(pos):
    blocked = set()
    for di, dj in KNIGHT_MOVES:
        ni, nj = pos[0] + di, pos[1] + dj
        if 0 <= ni < ROWS and 0 <= nj < COLS:
            blocked.add((ni, nj))
    return blocked


def print_case(desc, state):
    g = Game(state)
    print('---')
    print(desc)
    print('State:', state)
    print('Utility:', g._utility(state))
    print()


def main():
    special = {(2, 2): 5, (4, 4): -3, (3, 1): 2}
    destroyed = frozenset({(0, 0)})

    # Caso base: posiciones separadas, algunas casillas especiales
    s1 = State(pts_min=0, pts_max=0, pos_min=(0, 1), pos_max=(7, 7), destroyed_squares=destroyed, special_squares=special)
    print_case('Initial (no penalties)', s1)

    # Caso: máquina bloqueada (debe recibir penalización -4)
    destroyed2 = set(destroyed)
    destroyed2.update(block_moves_for((0, 0)))
    s2 = State(pts_min=0, pts_max=0, pos_min=(7, 7), pos_max=(0, 0), destroyed_squares=frozenset(destroyed2), special_squares=special)
    print_case('Machine blocked (expect machine penalty)', s2)

    # Caso: jugador bloqueado (debe recibir penalización -4)
    destroyed3 = set(destroyed)
    destroyed3.update(block_moves_for((7, 7)))
    s3 = State(pts_min=0, pts_max=0, pos_min=(7, 7), pos_max=(0, 0), destroyed_squares=frozenset(destroyed3), special_squares=special)
    print_case('Player blocked (expect player penalty)', s3)


if __name__ == '__main__':
    main()
