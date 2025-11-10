import tkinter as tk
import os
from app.models.match import *
from app.utils.constants import *

class GameView(tk.Frame):
    def __init__(self, parent, controller, match):
        super().__init__(parent)
        self.controller = controller
        self.match = match

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
        

        # ✅ Aquí creamos el contenedor del tablero
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

        for i, row in enumerate(board):
            for j, cell in enumerate(row):

                # Valores por defecto
                text = ""
                image = None

                if cell.type == CellType.EMPTY:
                    bg = "#FFF0DD"

                elif cell.type == CellType.COMPUTER:
                    image = self.machine_img
                    bg = "#FFF0DD"

                elif cell.type == CellType.PLAYER:
                    image = self.human_img
                    bg = "#FFF0DD"

                elif cell.type == CellType.SPECIAL:
                    # Texto visible
                    text = f"+{cell.value}" if cell.value > 0 else str(cell.value)

                    # ✅ Color según positivo/negativo/cero
                    if cell.value < 0:
                        bg = "#b22222"  # rojo suave
                    elif cell.value > 0:
                        bg = "#00a36c"  # verde suave
                    else:
                        bg = "#e6e6e6"  # gris

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

                # ✅ evitar que el garbage collector elimine la imagen
                label.image = image 

                label.grid(row=i, column=j, sticky="nsew")

        # Ajuste de filas/columnas
        for i in range(ROWS):
            self.board_frame.grid_rowconfigure(i, weight=1)

        for j in range(COLS):
            self.board_frame.grid_columnconfigure(j, weight=1)
