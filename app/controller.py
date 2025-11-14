
import tkinter as tk
from app.views.home_view import HomeView
from app.views.game_view import GameView
from app.models.match import Match, Turn
from app.models.machine import Machine
from app.utils.constants import AMATEUR
import threading


class Controller:
    def __init__(self):
        self.root = tk.Tk() 
        self.root.title("Smart horses")
        self.root.geometry("1000x700")

        self.model = Match()
        self.machine = Machine(difficulty=AMATEUR)

        # Diccionario de vistas
        self.views = {
            "home": HomeView(self.root, self),
            "game": GameView(self.root, self, self.model)
        }

        self.show_view("home")
    
    def show_view(self, name):
        # Ocultar todas
        for view in self.views.values():
            view.pack_forget()

        # Mostrar la seleccionada
        self.views[name].pack(fill="both", expand=True)

    def start_game(self):
        self.show_view("game")

        if self.model._turn == Turn.COMPUTER:
            t = threading.Thread(target=self._apply_machineM, daemon=True)
            t.start()

    def _apply_machineM(self):
        move = self.machine.choose_game(self.model)
        
        def apply_move():
            if move is not None:
                self.model.play_turn(move)
                self.views["game"].draw_board()
        self.root.after(0, apply_move)

    def reset_game(self):
        self.model = Match()
        self.show_view("home")
        self.views["game"] = GameView(self.root, self, self.model)

    def run(self):
        self.root.mainloop()