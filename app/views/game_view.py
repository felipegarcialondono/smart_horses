import tkinter as tk
import os
from app.models.match import *
from app.utils.constants import *
from app.models.player import Player

class GameView(tk.Frame):
    def __init__(self, parent, controller, match):
        super().__init__(parent)
        self.controller = controller
        self.match = match
        
        # Añadir estos atributos
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
        
        # Aquí creamos el contenedor del tablero
        self.board_frame = tk.Frame(right_frame)
        self.board_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # ------- LEFT CONTENT -------
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        logo_path = os.path.join(base_path, "assets", "logo-sm.png")

        self.logo = tk.PhotoImage(file=logo_path)
        
        tk.Label(left_frame, image=self.logo, bg="#0B1F25").pack()

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
            command=controller.reset_game
        ).pack(pady=5)

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
            command=self.master.destroy
        ).pack(pady=5)

        human_path = os.path.join(base_path, "assets", "human.png")
        machine_path = os.path.join(base_path, "assets", "machine.png")

        self.human_img = tk.PhotoImage(file=human_path)
        self.machine_img = tk.PhotoImage(file=machine_path)

        self.draw_board()

    def draw_board(self):
        board = self.match.board

        # Borrar tablero anterior
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.hover_labels = {}
        self.current_hover_path = []

        # Calcular movimientos válidos si es turno del jugador
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
                    image = self.machine_img
                    bg = "#FFF0DD"

                elif cell.type == CellType.PLAYER:
                    image = self.human_img
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
                
                # Guardar referencia y color original
                label.original_bg = bg
                self.hover_labels[(i, j)] = label

                
                # HOVER Y CLICK solo en las casillas DESTINO
                if (i, j) in self.valid_moves:
                    label.configure(cursor="hand2")
                    label.bind("<Enter>", lambda e, pos=(i, j): self.on_hover_enter(pos))
                    label.bind("<Leave>", lambda e, pos=(i, j): self.on_hover_leave(pos))
                    label.bind("<Button-1>", lambda e, pos=(i, j): self.on_cell_click(pos))

        # Ajuste de filas/columnas
        for i in range(ROWS):
            self.board_frame.grid_rowconfigure(i, weight=1)

        for j in range(COLS):
            self.board_frame.grid_columnconfigure(j, weight=1)

    def on_hover_enter(self, pos):
        """Cuando el mouse entra en una casilla válida - mostrar el path completo"""
        # Obtener el path hacia esta casilla
        current_player_pos = self.match._player_pos
        path = self.player.get_path_to_square(current_player_pos, pos) 

        self.current_hover_path = path + [current_player_pos] 
        self.current_hover_path = path 
        
        
        
        # Pintar todas las casillas del path de verde
        for path_pos in path:
            label = self.hover_labels.get(path_pos)
            if label:
                label.configure(bg="#90EE90", relief="sunken")

    def on_hover_leave(self, pos):
        """Cuando el mouse sale de una casilla válida - restaurar colores"""
        # Restaurar todas las casillas del path anterior
        for path_pos in self.current_hover_path:
            label = self.hover_labels.get(path_pos)
            if label and hasattr(label, 'original_bg'):
                label.configure(bg=label.original_bg, relief="raised")
        
        self.current_hover_path = []

    

    def on_cell_click(self, pos):
        """Cuando se hace click en una casilla válida"""
        success = self.match.play_turn(pos)
        
        if success:
            self.draw_board()