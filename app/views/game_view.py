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

        self.base_font = ("Segoe UI", 11)
        self.title_font = ("Segoe UI", 12, "bold")
        self.big_font = ("Segoe UI", 14, "bold")

        self.player = Player(match)
        self.valid_moves = []
        self.hover_labels = {}
        self.current_hover_path = []

        self.input_locked = False

        self.turn_label = None
        self.coords_label = None
        self.level_label = None
        self.thinking_label = None

        # Layout 20% / 80%
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=9)
        self.grid_rowconfigure(0, weight=1)

        # LEFT 
        left_frame = tk.Frame(self, bg="#08151A")
        left_frame.grid(row=0, column=0, sticky="nsew")

        # RIGHT
        right_frame = tk.Frame(self, bg="#1f6f74")
        right_frame.grid(row=0, column=1, sticky="nsew")

        self.board_frame = tk.Frame(right_frame, bg="#e9efe9")
        self.board_frame.pack(expand=True, fill="both", padx=12, pady=12)

        # ------- LEFT CONTENT -------
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        logo_path = os.path.join(base_path, "assets", "logo-sm.png")

        # --- NIVEL DE DIFICULTAD ---
        level_frame = tk.Frame(left_frame, bg="#08151A")
        level_frame.pack(pady=(12,6), fill="x")

        tk.Label(
            level_frame,
            text="DIFICULTAD",
            bg="#08151A",
            fg="#E6F7F6",
            font=self.title_font
        ).pack()

        # Determinar nombre y profundidad desde controller.difficulty (constantes)
        try:
            diff = getattr(self.controller, "difficulty", None)
        except Exception:
            diff = None

        level_name = "AMATEUR"
        depth = "?"
        if diff == BEGGINER:
            level_name = "PRINCIPIANTE"
            depth = 2
        elif diff == AMATEUR:
            level_name = "AMATEUR"
            depth = 4
        elif diff == EXPERT:
            level_name = "EXPERTO"
            depth = 6
        else:
            level_name = getattr(self.match, "level_name", level_name)
            depth = getattr(self.match, "depth", depth)

        self.level_label = tk.Label(
            level_frame,
            text=f"{level_name} (profundidad {depth})",
            bg="#08151A",
            fg="#FFC857",
            font=self.base_font
        )
        self.level_label.pack()

        # POSICIONES (coordenadas)
        coords_frame = tk.Frame(left_frame, bg="#08151A")
        coords_frame.pack(pady=(8,6), fill="x")

        tk.Label(
            coords_frame,
            text="POSICIONES",
            bg="#08151A",
            fg="#E6F7F6",
            font=self.title_font
        ).pack()

        self.coords_label = tk.Label(
            coords_frame,
            text="",
            bg="#08151A",
            fg="#FFC857",
            font=self.base_font,
        )
        self.coords_label.pack()

        # TURNOS
        turn_frame = tk.Frame(left_frame, bg="#08151A")
        turn_frame.pack(pady=(8,6), fill="x")

        tk.Label(
            turn_frame,
            text="TURNO ACTUAL",
            bg="#08151A",
            fg="#E6F7F6",
            font=self.title_font
        ).pack()

        self.turn_label = tk.Label(
            turn_frame,
            text="",
            bg="#08151A",
            fg="#7FE3D7",
            font=self.base_font,
        )
        self.turn_label.pack()

        self.thinking_label = tk.Label(
            left_frame,
            text="",
            bg="#08151A",
            fg="#FFD66B",
            font=("Segoe UI", 10, "italic")
        )
        self.thinking_label.pack(pady=6)

        try:
            img_pil = Image.open(logo_path)
            max_size = (100, 100)
            img_pil.thumbnail(max_size, Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(img_pil)

            logo_label = tk.Label(left_frame, image=self.logo, bg="#08151A")
            logo_label.pack(pady=(6,8))
        except Exception:
            tk.Label(left_frame, text="SMART HORSES", bg="#08151A", fg="#FFC857",
                     font=("Segoe UI", 18, "bold")).pack(pady=(6,8))

        # MARCADOR DE PUNTOS
        score_frame = tk.Frame(left_frame, bg="#08151A")
        score_frame.pack(pady=(4,12), fill="x")

        tk.Label(score_frame, text="PUNTUACIÓN", bg="#08151A", fg="#E6F7F6",
                font=self.big_font).pack(pady=6)

        icons_path = os.path.join(base_path, "assets", "icons")

        try:
            self.icon_computer = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "robot.png")).resize((22, 22)))
            self.icon_player = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "user.png")).resize((22, 22)))
            icons_loaded = True
        except Exception:
            icons_loaded = False

        # Computadora
        computer_frame = tk.Frame(score_frame, bg="#0f3b3e", relief="flat", borderwidth=0)
        computer_frame.pack(fill="x", pady=6, padx=8)

        computer_header = tk.Frame(computer_frame, bg="#0f3b3e")
        computer_header.pack(fill="x", pady=2)

        if icons_loaded:
            tk.Label(computer_header, image=self.icon_computer, bg="#0f3b3e").pack(side="left", padx=6)

        tk.Label(computer_header, text="Computadora", bg="#0f3b3e", fg="#7FE3D7",
                font=self.base_font).pack(side="left")

        self.computer_score_label = tk.Label(computer_frame, text="0", bg="#0f3b3e",
                                             fg="#E6F7F6", font=self.big_font)
        self.computer_score_label.pack(pady=6)

        # Jugador
        player_frame = tk.Frame(score_frame, bg="#0f3b3e", relief="flat", borderwidth=0)
        player_frame.pack(fill="x", pady=6, padx=8)

        player_header = tk.Frame(player_frame, bg="#0f3b3e")
        player_header.pack(fill="x", pady=2)

        if icons_loaded:
            tk.Label(player_header, image=self.icon_player, bg="#0f3b3e").pack(side="left", padx=6)

        tk.Label(player_header, text="Jugador", bg="#0f3b3e", fg="#FFC857",
                font=self.base_font).pack(side="left")

        self.player_score_label = tk.Label(player_frame, text="0", bg="#0f3b3e",
                                           fg="#E6F7F6", font=self.big_font)
        self.player_score_label.pack(pady=6)

        def make_round_button(parent, text, bg_color, fg_color, command, font=None):
            font = font or self.base_font
            canvas = tk.Canvas(parent, height=44, bg=parent.cget("bg"), highlightthickness=0)
            def draw_rect(event=None):
                w = canvas.winfo_width() or 200
                h = canvas.winfo_height() or 44
                radius = 10
                canvas.delete("all")
                x0, y0, x1, y1 = 4, 4, w-4, h-4
                canvas.create_arc(x0, y0, x0+2*radius, y0+2*radius, start=90, extent=90, fill=bg_color, outline=bg_color)
                canvas.create_arc(x1-2*radius, y0, x1, y0+2*radius, start=0, extent=90, fill=bg_color, outline=bg_color)
                canvas.create_arc(x0, y1-2*radius, x0+2*radius, y1, start=180, extent=90, fill=bg_color, outline=bg_color)
                canvas.create_arc(x1-2*radius, y1-2*radius, x1, y1, start=270, extent=90, fill=bg_color, outline=bg_color)
                canvas.create_rectangle(x0+radius, y0, x1-radius, y1, fill=bg_color, outline=bg_color)
                canvas.create_rectangle(x0, y0+radius, x1, y1-radius, fill=bg_color, outline=bg_color)
                canvas.create_text(w//2, h//2, text=text, fill=fg_color, font=font)
            canvas.bind("<Configure>", draw_rect)

            def on_enter(e):
                canvas.configure(cursor="hand2")
                draw_rect()

            def on_leave(e):
                canvas.configure(cursor="")
                draw_rect()

            canvas.bind("<Enter>", on_enter)
            canvas.bind("<Leave>", on_leave)

            def on_click(e):
                try:
                    command()
                except Exception:
                    # si command es una lista/tuple (lambda de varios), intentar ejecutar element-wise
                    try:
                        if isinstance(command, (list, tuple)):
                            for c in command:
                                c()
                    except Exception:
                        pass
            canvas.bind("<Button-1>", on_click)
            return canvas

        btn_frame = tk.Frame(left_frame, bg="#08151A")
        btn_frame.pack(pady=8, padx=10, fill="x")

        restart_cmd = lambda: [controller.music_player.play_sound("click"), controller.reset_game()]
        menu_cmd = lambda: [controller.music_player.play_sound("click"), controller.show_view("home")]

        def exit_cmd():
            try:
                pygame.mixer.stop()
            except Exception:
                pass
            try:
                controller.music_player.play_sound("click")
            except Exception:
                pass
            
            try:
                top = self.winfo_toplevel()
                top.destroy()
            except Exception:
                try:
                    self.master.destroy()
                except Exception:
                    pass

        btn1 = make_round_button(btn_frame, "REINICIAR", "#FFC857", "#08151A", restart_cmd, font=("Segoe UI",12,"bold"))
        btn1.pack(fill="x", pady=6)

        btn2 = make_round_button(btn_frame, "MENÚ PRINCIPAL", "#7FE3D7", "#08151A", menu_cmd, font=("Segoe UI",11,"bold"))
        btn2.pack(fill="x", pady=6)

        btn3 = make_round_button(btn_frame, "SALIR", "#D64545", "#FFFFFF", exit_cmd, font=("Segoe UI",12,"bold"))
        btn3.pack(fill="x", pady=6)

        human_path = os.path.join(base_path, "assets", "human.png")
        machine_path = os.path.join(base_path, "assets", "machine.png")

        try:
            img_human = Image.open(human_path).resize((36,36), Image.LANCZOS)
            img_machine = Image.open(machine_path).resize((36,36), Image.LANCZOS)
            self.human_img = ImageTk.PhotoImage(img_human)
            self.machine_img = ImageTk.PhotoImage(img_machine)
        except Exception:
            self.human_img = None
            self.machine_img = None

        self.draw_board()
        self.update_scores()
        self.update_turn_label()
        self.update_coordinates()
        self.update_level_label()

        # Si la máquina empieza, disparar su turno con bloqueo y pequeña pausa
        if self.match._turn == Turn.COMPUTER:
            self._show_thinking(True)
            self.after(700, self._trigger_computer_move)

    # ------------------------------ Helpers ------------------------------
    def update_scores(self):
        """Actualiza los marcadores de puntos"""
        self.computer_score_label.config(text=str(self.match._computer_points))
        self.player_score_label.config(text=str(self.match._player_points))

    def update_coordinates(self):
        player = getattr(self.match, "_player_pos", None)
        comp = getattr(self.match, "_computer_pos", None)
        text = f"Jugador: {player}\nComputadora: {comp}"
        if self.coords_label:
            self.coords_label.config(text=text)

    def update_turn_label(self):
        if not self.turn_label:
            return
        try:
            if self.match._turn == Turn.PLAYER:
                self.turn_label.config(text="Jugador")
            else:
                self.turn_label.config(text="Computadora")
        except Exception:
            self.turn_label.config(text="?")

    def update_level_label(self):
        if not self.level_label:
            return
        diff = getattr(self.controller, "difficulty", None)
        level_name = getattr(self.match, "level_name", None)
        depth = getattr(self.match, "depth", None)

        if diff == BEGGINER or (level_name and str(level_name).lower().startswith("p")):
            self.level_label.config(text="PRINCIPIANTE (profundidad 2)")
        elif diff == AMATEUR or (level_name and str(level_name).lower().startswith("a")):
            self.level_label.config(text="AMATEUR (profundidad 4)")
        elif diff == EXPERT or (level_name and str(level_name).lower().startswith("e")):
            self.level_label.config(text="EXPERTO (profundidad 6)")
        elif depth:
            self.level_label.config(text=f"PROFUNDIDAD {depth}")
        else:
            self.level_label.config(text=self.level_label.cget("text"))

    def _show_thinking(self, show=True):
        """Muestra u oculta el label 'Computadora pensando...'"""
        if not self.thinking_label:
            return
        if show:
            self.thinking_label.config(text="Computadora pensando...")
        else:
            self.thinking_label.config(text="")

    # ------------------------------ Game Over ------------------------------
    def show_game_over(self):
        """Muestra la pantalla de fin del juego con íconos y colores"""
        WIDTH = 600
        HEIGHT = 500
        try:
            self.controller.music_player.stop_music()
        except Exception:
            pass

        try:
            if self.match._winner == 'PLAYER':
                self.controller.music_player.play_sound("victory")
            elif self.match._winner == 'COMPUTER':
                self.controller.music_player.play_sound("defeat")
        except Exception:
            pass

        game_over_window = tk.Toplevel(self.master)
        game_over_window.title("Fin del Juego")
        game_over_window.geometry(f"{WIDTH}x{HEIGHT}")
        game_over_window.configure(bg="#08151A")
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
            icon_label = tk.Label(game_over_window, image=icon_photo, bg="#08151A")
            icon_label.image = icon_photo
            icon_label.pack(pady=20)
        except Exception:
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
            bg="#08151A",
            fg=color,
            font=("Segoe UI", 28, "bold")
        ).pack(pady=6)

        tk.Label(
            game_over_window,
            text=message,
            bg="#08151A",
            fg="#E6F7F6",
            font=("Segoe UI", 13),
            justify="center"
        ).pack(pady=8)

        score_frame = tk.Frame(game_over_window, bg="#0f3b3e", relief="raised", borderwidth=3)
        score_frame.pack(pady=14, padx=40, fill="x")

        tk.Label(
            score_frame,
            text="PUNTUACIÓN FINAL",
            bg="#0f3b3e",
            fg="#E6F7F6",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=10)

        scores_text = f"Computadora: {self.match._computer_points}  |  Jugador: {self.match._player_points}"
        tk.Label(
            score_frame,
            text=scores_text,
            bg="#0f3b3e",
            fg="#E6F7F6",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        button_frame = tk.Frame(game_over_window, bg="#08151A")
        button_frame.pack(pady=18)

        def on_play_again():
            
            pygame.mixer.stop()
            self.controller.music_player.play_sound("click")
            try:
                self.controller.music_player.play_music("game")
                self.controller.music_player.load_sounds()
            except Exception as e:
                print("Error reactivando música:", e)
            game_over_window.destroy()
            self.controller.reset_game()

        def on_menu():
            try:
                pygame.mixer.stop()
                self.controller.music_player.play_sound("click")
            except Exception:
                pass
            game_over_window.destroy()
            self.controller.show_view("home")

        tk.Button(
            button_frame,
            text="JUGAR DE NUEVO",
            bg="#FFC857",
            fg="#08151A",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            width=15,
            command=on_play_again,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="MENÚ PRINCIPAL",
            bg="#7FE3D7",
            fg="#08151A",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            width=15,
            command=on_menu,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)

        game_over_window.update_idletasks()
        try:
            game_over_window.grab_set()
        except tk.TclError:
            game_over_window.after(100, lambda: game_over_window.grab_set())

    # ------------------------------ Board ------------------------------
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

        light_cell = "#F2E8DF"
        dark_cell = "#D9CFC6"
        special_pos = "#00a36c"
        special_neg = "#b22222"
        destroyed_bg = "#121212"

        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                text = ""
                image = None
                # alternar colores tipo tablero
                bg = light_cell if (i + j) % 2 == 0 else dark_cell
                fg = "#1b1b1b"

                if cell.type == CellType.EMPTY:
                    pass
                elif cell.type == CellType.COMPUTER:
                    image = self.machine_img if self.machine_img else None
                    text = "C" if not self.machine_img else ""
                elif cell.type == CellType.PLAYER:
                    image = self.human_img if self.human_img else None
                    text = "J" if not self.human_img else ""
                elif cell.type == CellType.SPECIAL:
                    text = f"+{cell.value}" if cell.value > 0 else str(cell.value)
                    if cell.value < 0:
                        bg = special_neg
                        fg = "white"
                    elif cell.value > 0:
                        bg = special_pos
                        fg = "white"
                    else:
                        bg = "#e6e6e6"
                elif cell.type == CellType.DESTROYED:
                    bg = destroyed_bg
                    text = "X"
                    fg = "white"

                label = tk.Label(
                    self.board_frame,
                    text=text,
                    font=("Segoe UI", 12, "bold"),
                    fg=fg,
                    image=image,
                    width=4,
                    height=2,
                    bg=bg,
                    borderwidth=1,
                    highlightbackground="#8C442B",
                    relief="raised",
                )

                label.image = image
                label.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)

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

        self.update_turn_label()
        self.update_coordinates()
        self.update_level_label()

    def on_hover_enter(self, pos):
        if self.input_locked:
            return

        current_player_pos = self.match._player_pos
        path = self.player.get_path_to_square(current_player_pos, pos)
        self.current_hover_path = path + [current_player_pos]

        for path_pos in self.current_hover_path:
            label = self.hover_labels.get(path_pos)
            if label:
                try:
                    label.configure(bg="#7CFC9A", relief="sunken")
                except Exception:
                    pass

    def on_hover_leave(self, pos):
        for path_pos in self.current_hover_path:
            label = self.hover_labels.get(path_pos)
            if label and hasattr(label, 'original_bg'):
                try:
                    label.configure(bg=label.original_bg, relief="raised")
                except Exception:
                    pass
        self.current_hover_path = []

    def on_cell_click(self, pos):
        if self.input_locked:
            return

        print(f"Jugador intenta moverse a: {pos}")

        cell = self.match.board[pos[0]][pos[1]]
        is_special = cell.type == CellType.SPECIAL

        success = self.match.play_turn(pos)

        if success:
            try:
                if is_special:
                    self.controller.music_player.play_sound("special")
                else:
                    self.controller.music_player.play_sound("move")
            except Exception:
                pass

            print(f"Jugador se movio exitosamente")
            self.draw_board()
            self.update_scores()

            if self.match.check_game_over():
                self.after(500, self.show_game_over)
                return

            self.update_coordinates()
            self.update_turn_label()

            if self.match._turn == Turn.COMPUTER:
                self._show_thinking(True)
                self.after(700, lambda: [self._trigger_computer_move()])

    def _trigger_computer_move(self):
        self.input_locked = True
        self.update_turn_label()
        self._show_thinking(True)

        t = threading.Thread(target=self._apply_machine_move, daemon=True)
        t.start()

    def _apply_machine_move(self):
        if self.match._game_over:
            self.input_locked = False
            self._show_thinking(False)
            self.update_turn_label()
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
                    try:
                        if is_special:
                            self.controller.music_player.play_sound("special")
                        else:
                            self.controller.music_player.play_sound("move")
                    except Exception:
                        pass

                self.draw_board()
                self.update_scores()

                if self.match.check_game_over():
                    self.after(500, self.show_game_over)
            else:
                print("La computadora no tiene movimientos disponibles")
                if self.match.check_game_over():
                    self.after(500, self.show_game_over)

            self.input_locked = False
            self._show_thinking(False)
            self.update_turn_label()
            self.update_coordinates()
            self.draw_board()


        self.after(0, apply_move)
