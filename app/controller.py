
import tkinter as tk
from app.views.home_view import HomeView
from app.views.game_view import GameView
from app.models.match import Match

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart horses")
        self.root.geometry("1000x700")

        self.model = Match()

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

    def reset_game(self):
        self.model = Match()
        self.show_view("home")
        self.views["game"] = GameView(self.root, self, self.model)

    def run(self):
        self.root.mainloop()