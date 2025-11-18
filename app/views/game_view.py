import tkinter as tk
import os
from app.models.match import *
from app.utils.constants import *
from app.models.player import Player
import threading
from PIL import Image, ImageTk
import pygame

class GameView(tk.Frame):
    def __init__(self, parent, controller, match):
        super().__init__(parent)
        self.controller = controller
        self.match = match
        
        self.player = Player(match)
        self.valid_moves = []
        self.hover_labels = {}
        self.current_hover_path = []

        # Layout 20% / 80%
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=9)
        self.grid_rowconfigure(0, weight=1)

        # LEFT
        left_frame = tk.Frame(self, bg="#0B1F25")
        left_frame.grid(row=0, column=0, sticky="nsew")

        # RIGHT
        right_frame = tk.Frame(self, bg="#226d7c")
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        self.board_frame = tk.Frame(right_frame)
        self.board_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # ------- LEFT CONTENT -------
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        logo_path = os.path.join(base_path, "assets", "logo-sm.png")

        try:
            img_pil = Image.open(logo_path)
            self.logo = ImageTk.PhotoImage(img_pil)
            tk.Label(left_frame, image=self.logo, bg="#0B1F25").pack(pady=10)
        except:
            tk.Label(left_frame, text="SMART HORSES", bg="#0B1F25", fg="#ffc300",
                    font=("TkDefaultFont", 16, "bold")).pack(pady=10)

        # MARCADOR DE PUNTOS
        score_frame = tk.Frame(left_frame, bg="#0B1F25")
        score_frame.pack(pady=15)

        tk.Label(score_frame, text="PUNTUACIÓN", bg="#0B1F25", fg="white", 
                font=("TkDefaultFont", 14, "bold")).pack(pady=5)

        # Cargar iconos para los jugadores
        icons_path = os.path.join(base_path, "assets", "icons")
        
        try:
            self.icon_computer = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "robot.png")).resize((20, 20)))
            self.icon_player = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "user.png")).resize((20, 20)))
            icons_loaded = True
        except:
            icons_loaded = False

        # Computadora
        computer_frame = tk.Frame(score_frame, bg="#1a3a42", relief="raised", borderwidth=2)
        computer_frame.pack(fill="x", pady=5, padx=10)
        
        computer_header = tk.Frame(computer_frame, bg="#1a3a42")
        computer_header.pack(pady=2)
        
        if icons_loaded:
            tk.Label(computer_header, image=self.icon_computer, bg="#1a3a42").pack(side="left", padx=5)
        
        tk.Label(computer_header, text="Computadora", bg="#1a3a42", fg="#00ced1",
                font=("TkDefaultFont", 11, "bold")).pack(side="left")
        
        self.computer_score_label = tk.Label(computer_frame, text="0", bg="#1a3a42", 
                                             fg="white", font=("TkDefaultFont", 20, "bold"))
        self.computer_score_label.pack(pady=5)

        # Jugador
        player_frame = tk.Frame(score_frame, bg="#1a3a42", relief="raised", borderwidth=2)
        player_frame.pack(fill="x", pady=5, padx=10)
        
        player_header = tk.Frame(player_frame, bg="#1a3a42")
        player_header.pack(pady=2)
        
        if icons_loaded:
            tk.Label(player_header, image=self.icon_player, bg="#1a3a42").pack(side="left", padx=5)
        
        tk.Label(player_header, text="Jugador", bg="#1a3a42", fg="#ffc300",
                font=("TkDefaultFont", 11, "bold")).pack(side="left")
        
        self.player_score_label = tk.Label(player_frame, text="0", bg="#1a3a42", 
                                           fg="white", font=("TkDefaultFont", 20, "bold"))
        self.player_score_label.pack(pady=5)

        tk.Button(
            left_frame,
            text="REINICIAR",
            bg="#ffc300",
            fg="white",
            highlightbackground="#fffa85",
            relief="flat",
            font=("TkDefaultFont", 14, "bold"),
            activebackground="#fffcc5",
            activeforeground="#ffc300",
            command=lambda: [controller.music_player.play_sound("click"), controller.reset_game()],
            cursor="hand2"
        ).pack(pady=5, padx=10, fill="x")

        tk.Button(
            left_frame,
            text="MENÚ PRINCIPAL",
            bg="#00ced1",
            fg="white",
            highlightbackground="#8efff9",
            relief="flat",
            font=("TkDefaultFont", 12, "bold"),
            activebackground="#c6fffb",
            activeforeground="#00ced1",
            command=lambda: [controller.music_player.play_sound("click"), controller.show_view("home")],
            cursor="hand2"
        ).pack(pady=5, padx=10, fill="x")

        tk.Button(
            left_frame,
            text="SALIR",
            bg="#d63031",
            fg="white",
            highlightbackground="#fccccc",
            relief="flat",
            font=("TkDefaultFont", 14, "bold"),
            activebackground="#fde3e3",
            activeforeground="#d63031",
            command=self.master.destroy,
            cursor="hand2"
        ).pack(pady=5, padx=10, fill="x")

        human_path = os.path.join(base_path, "assets", "human.png")
        machine_path = os.path.join(base_path, "assets", "machine.png")

        try:
            img_human = Image.open(human_path)
            img_machine = Image.open(machine_path)
            self.human_img = ImageTk.PhotoImage(img_human)
            self.machine_img = ImageTk.PhotoImage(img_machine)
        except:
            self.human_img = None
            self.machine_img = None

        self.draw_board()
        self.update_scores()
        
        if self.match._turn == Turn.COMPUTER:
            self.after(1000, self._trigger_computer_move)

    def update_scores(self):
        """Actualiza los marcadores de puntos"""
        self.computer_score_label.config(text=str(self.match._computer_points))
        self.player_score_label.config(text=str(self.match._player_points))

    def show_game_over(self):
        """Muestra la pantalla de fin de juego"""
        WIDTH = 600
        HEIGHT = 500
        
        # Detener la música del juego
        self.controller.music_player.stop_music()
        
        # Reproducir sonido según resultado
        if self.match._winner == 'PLAYER':
            self.controller.music_player.play_sound("victory")
        elif self.match._winner == 'COMPUTER':
            self.controller.music_player.play_sound("defeat")
        
        game_over_window = tk.Toplevel(self.master)
        game_over_window.title("Fin del Juego")
        game_over_window.geometry(f"{WIDTH}x{HEIGHT}")
        game_over_window.configure(bg="#0B1F25")
        game_over_window.transient(self.master)
        
        game_over_window.update_idletasks()
        x = (game_over_window.winfo_screenwidth() // 2) - (WIDTH // 2)
        y = (game_over_window.winfo_screenheight() // 2) - (HEIGHT // 2)
        game_over_window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        icons_path = os.path.join(base_path, "assets", "icons")
        
        try:
            if self.match._winner == 'PLAYER':
                icon_img = Image.open(os.path.join(icons_path, "trophy.png")).resize((100, 100))
                title = "¡VICTORIA!"
                message = "¡Felicidades!\nHas derrotado a la computadora"
                color = "#00a36c"
            elif self.match._winner == 'COMPUTER':
                icon_img = Image.open(os.path.join(icons_path, "sad.png")).resize((100, 100))
                title = "DERROTA"
                message = "La computadora ha ganado\nSigue intentando"
                color = "#d63031"
            else:
                icon_img = Image.open(os.path.join(icons_path, "handshake.png")).resize((100, 100))
                title = "EMPATE"
                message = "¡Empate técnico!\nAmbos jugadores son iguales"
                color = "#ffc300"
            
            icon_photo = ImageTk.PhotoImage(icon_img)
            icon_label = tk.Label(game_over_window, image=icon_photo, bg="#0B1F25")
            icon_label.image = icon_photo
            icon_label.pack(pady=20)
        except:
            if self.match._winner == 'PLAYER':
                title = "¡VICTORIA!"
                message = "¡Felicidades!\nHas derrotado a la computadora"
                color = "#00a36c"
            elif self.match._winner == 'COMPUTER':
                title = "DERROTA"
                message = "La computadora ha ganado\nSigue intentando"
                color = "#d63031"
            else:
                title = "EMPATE"
                message = "¡Empate técnico!\nAmbos jugadores son iguales"
                color = "#ffc300"

        tk.Label(
            game_over_window,
            text=title,
            bg="#0B1F25",
            fg=color,
            font=("TkDefaultFont", 28, "bold")
        ).pack(pady=10)

        tk.Label(
            game_over_window,
            text=message,
            bg="#0B1F25",
            fg="white",
            font=("TkDefaultFont", 14),
            justify="center"
        ).pack(pady=10)

        score_frame = tk.Frame(game_over_window, bg="#1a3a42", relief="raised", borderwidth=3)
        score_frame.pack(pady=20, padx=40, fill="x")

        tk.Label(
            score_frame,
            text="PUNTUACIÓN FINAL",
            bg="#1a3a42",
            fg="white",
            font=("TkDefaultFont", 12, "bold")
        ).pack(pady=10)

        scores_text = f"Computadora: {self.match._computer_points}  |  Jugador: {self.match._player_points}"
        tk.Label(
            score_frame,
            text=scores_text,
            bg="#1a3a42",
            fg="white",
            font=("TkDefaultFont", 14, "bold")
        ).pack(pady=10)

        button_frame = tk.Frame(game_over_window, bg="#0B1F25")
        button_frame.pack(pady=25)

        # Función auxiliar para detener sonidos y cerrar ventana
        def on_play_again():
            pygame.mixer.stop()
            self.controller.music_player.play_sound("click")
            game_over_window.destroy()
            self.controller.reset_game()

        def on_menu():
            pygame.mixer.stop()
            self.controller.music_player.play_sound("click")
            game_over_window.destroy()
            self.controller.show_view("home")

        tk.Button(
            button_frame,
            text="JUGAR DE NUEVO",
            bg="#ffc300",
            fg="white",
            relief="flat",
            font=("TkDefaultFont", 12, "bold"),
            width=15,
            command=on_play_again,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="MENÚ PRINCIPAL",
            bg="#00ced1",
            fg="white",
            relief="flat",
            font=("TkDefaultFont", 12, "bold"),
            width=15,
            command=on_menu,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)

        game_over_window.update_idletasks()
        try:
            game_over_window.grab_set()
        except tk.TclError:
            game_over_window.after(100, lambda: game_over_window.grab_set())

    def draw_board(self):
        board = self.match.board
        
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.hover_labels = {}
        self.current_hover_path = []

        if self.match._turn == Turn.PLAYER:
            self.valid_moves = self.player.get_valid_moves(self.match._player_pos)
        else:
            self.valid_moves = []

        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                text = ""
                image = None
                bg = "#FFF0DD"

                if cell.type == CellType.EMPTY:
                    bg = "#FFF0DD"
                elif cell.type == CellType.COMPUTER:
                    image = self.machine_img if self.machine_img else None
                    text = "C" if not self.machine_img else ""
                    bg = "#FFF0DD"
                elif cell.type == CellType.PLAYER:
                    image = self.human_img if self.human_img else None
                    text = "J" if not self.human_img else ""
                    bg = "#FFF0DD"
                elif cell.type == CellType.SPECIAL:
                    text = f"+{cell.value}" if cell.value > 0 else str(cell.value)
                    if cell.value < 0:
                        bg = "#b22222"
                    elif cell.value > 0:
                        bg = "#00a36c"
                    else:
                        bg = "#e6e6e6"
                elif cell.type == CellType.DESTROYED:
                    bg = "#d63031"

                label = tk.Label(
                    self.board_frame,
                    text=text,
                    font=("TkDefaultFont", 14, "bold"),
                    fg="white",
                    image=image,
                    width=4,
                    height=2,
                    bg=bg,
                    borderwidth=2,
                    highlightbackground="#8C442B",
                    relief="raised",
                )

                label.image = image
                label.grid(row=i, column=j, sticky="nsew")
                
                label.original_bg = bg
                self.hover_labels[(i, j)] = label

                if (i, j) in self.valid_moves:
                    label.configure(cursor="hand2")
                    label.bind("<Enter>", lambda e, pos=(i, j): self.on_hover_enter(pos))
                    label.bind("<Leave>", lambda e, pos=(i, j): self.on_hover_leave(pos))
                    label.bind("<Button-1>", lambda e, pos=(i, j): self.on_cell_click(pos))

        for i in range(ROWS):
            self.board_frame.grid_rowconfigure(i, weight=1)
        for j in range(COLS):
            self.board_frame.grid_columnconfigure(j, weight=1)
    
    def on_hover_enter(self, pos):
        current_player_pos = self.match._player_pos
        path = self.player.get_path_to_square(current_player_pos, pos)
        self.current_hover_path = path + [current_player_pos]
        
        for path_pos in self.current_hover_path:
            label = self.hover_labels.get(path_pos)
            if label:
                label.configure(bg="#90EE90", relief="sunken")

    def on_hover_leave(self, pos):
        for path_pos in self.current_hover_path:
            label = self.hover_labels.get(path_pos)
            if label and hasattr(label, 'original_bg'):
                label.configure(bg=label.original_bg, relief="raised")
        self.current_hover_path = []

    def on_cell_click(self, pos):
        print(f"Jugador intenta moverse a: {pos}")
        
        cell = self.match.board[pos[0]][pos[1]]
        is_special = cell.type == CellType.SPECIAL
        
        success = self.match.play_turn(pos)
        
        if success:
            if is_special:
                self.controller.music_player.play_sound("special")
            else:
                self.controller.music_player.play_sound("move")
            
            print(f"Jugador se movio exitosamente")
            self.draw_board()
            self.update_scores()
            
            if self.match.check_game_over():
                self.after(500, self.show_game_over)
                return
            
            if self.match._turn == Turn.COMPUTER:
                print("Iniciando turno de la computadora...")
                self.after(500, self._trigger_computer_move)

    def _trigger_computer_move(self):
        t = threading.Thread(target=self._apply_machine_move, daemon=True)
        t.start()

    def _apply_machine_move(self):
        if self.match._game_over:
            return
        
        move = self.controller.machine.choose_game(self.match)
        
        def apply_move():
            if move is not None:
                print(f"Computadora se mueve a: {move}")
                
                cell = self.match.board[move[0]][move[1]]
                is_special = cell.type == CellType.SPECIAL
                
                success = self.match.play_turn(move)
                print(f"{'Exitoso' if success else 'Fallido'} movimiento")
                
                if success:
                    if is_special:
                        self.controller.music_player.play_sound("special")
                    else:
                        self.controller.music_player.play_sound("move")
                
                self.draw_board()
                self.update_scores()
                
                if self.match.check_game_over():
                    self.after(500, self.show_game_over)
            else:
                print("La computadora no tiene movimientos disponibles")
                if self.match.check_game_over():
                    self.after(500, self.show_game_over)
        
        self.after(0, apply_move)