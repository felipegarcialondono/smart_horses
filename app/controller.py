import tkinter as tk
from app.views.home_view import HomeView
from app.views.difficulty_view import DifficultyView
from app.views.game_view import GameView
from app.models.match import Match, Turn
from app.models.machine import Machine
from app.utils.constants import AMATEUR, BEGGINER, EXPERT
from app.utils.music_player import MusicPlayer


class Controller:
    def __init__(self):
        self.root = tk.Tk() 
        self.root.title("Smart Horses")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0B1F25")

        self.model = None
        self.machine = None
        self.difficulty = AMATEUR
        
        # Inicializar reproductor de música
        self.music_player = MusicPlayer()

        # Diccionario de vistas
        self.views = {
            "home": HomeView(self.root, self),
            "difficulty": DifficultyView(self.root, self)
        }

        self.show_view("home")
        
        # Reproducir música del menú
        self.music_player.play_music("menu")
    
    def show_view(self, name):
        """Oculta todas las vistas y muestra la seleccionada"""
        for view in self.views.values():
            view.pack_forget()

        self.views[name].pack(fill="both", expand=True)
        
        # Cambiar música según la vista
        if name == "home" or name == "difficulty":
            self.music_player.play_music("menu")

    def start_game(self, difficulty_str):
        """Inicia el juego con la dificultad seleccionada"""
        print(f"🎯 [CONTROLLER] start_game llamado con difficulty_str: '{difficulty_str}' (tipo: {type(difficulty_str).__name__})")
        
        # Convertir string a constante
        if difficulty_str == "BEGGINER":
            self.difficulty = BEGGINER
            print(f"✅ [CONTROLLER] Dificultad asignada: BEGGINER (valor: {BEGGINER})")
        elif difficulty_str == "AMATEUR":
            self.difficulty = AMATEUR
            print(f"✅ [CONTROLLER] Dificultad asignada: AMATEUR (valor: {AMATEUR})")
        else:
            self.difficulty = EXPERT
            print(f"✅ [CONTROLLER] Dificultad asignada: EXPERT (valor: {EXPERT})")

        # Crear nuevo modelo y máquina
        self.model = Match()
        self.machine = Machine(difficulty=self.difficulty)
        print(f"🤖 [CONTROLLER] Máquina creada con dificultad: {self.difficulty} (max_depth: {self.machine.max_depth})")

        # Si ya existe la vista de juego, destruirla primero
        if "game" in self.views:
            self.views["game"].destroy()
        
        # Crear vista de juego
        self.views["game"] = GameView(self.root, self, self.model)
        self.show_view("game")
        
        # Cambiar a música de juego
        self.music_player.play_music("game")

    def reset_game(self):
        """Reinicia el juego con la misma dificultad"""
        # Crear nuevo modelo y máquina
        self.model = Match()
        self.machine = Machine(difficulty=self.difficulty)
        
        # Destruir la vista anterior completamente
        if "game" in self.views:
            self.views["game"].destroy()
        
        # Crear nueva vista de juego
        self.views["game"] = GameView(self.root, self, self.model)
        self.show_view("game")
        
        # Asegurar que suena música de juego
        self.music_player.play_music("game")

    def run(self):
        self.root.mainloop()