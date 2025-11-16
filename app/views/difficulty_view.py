import tkinter as tk
import os

class DifficultyView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0B1F25")
        self.controller = controller

        # Título
        tk.Label(
            self,
            text="SELECCIONA LA DIFICULTAD",
            bg="#0B1F25",
            fg="white",
            font=("TkDefaultFont", 24, "bold")
        ).pack(pady=40)

        # Contenedor de los botones de dificultad
        buttons_container = tk.Frame(self, bg="#0B1F25")
        buttons_container.pack(expand=True, pady=20)

        # Información de cada dificultad
        difficulties = [
            {
                "name": "PRINCIPIANTE",
                "level": "BEGGINER",
                "depth": "Profundidad: 2",
                "description": "Ideal para empezar",
                "color": "#00a36c",
                "hover_color": "#00cc87"
            },
            {
                "name": "AMATEUR",
                "level": "AMATEUR",
                "depth": "Profundidad: 4",
                "description": "Desafío moderado",
                "color": "#ffc300",
                "hover_color": "#ffd633"
            },
            {
                "name": "EXPERTO",
                "level": "EXPERT",
                "depth": "Profundidad: 6",
                "description": "Para jugadores avanzados",
                "color": "#d63031",
                "hover_color": "#ff4d4f"
            }
        ]

        # Crear un botón para cada dificultad
        for i, diff in enumerate(difficulties):
            self._create_difficulty_card(buttons_container, diff, i)

        # Botón de volver
        tk.Button(
            self,
            text="← VOLVER",
            bg="#226d7c",
            fg="white",
            relief="flat",
            font=("TkDefaultFont", 12, "bold"),
            activebackground="#2a8a9e",
            activeforeground="white",
            command=lambda: controller.show_view("home"),
            cursor="hand2"
        ).pack(pady=20)

    def _create_difficulty_card(self, parent, diff_info, index):
        """Crea una tarjeta para cada nivel de dificultad"""
        # Frame contenedor de la tarjeta
        card_frame = tk.Frame(
            parent,
            bg="#1a3a42",
            relief="raised",
            borderwidth=3,
            highlightbackground=diff_info["color"],
            highlightthickness=2
        )
        card_frame.grid(row=0, column=index, padx=20, pady=20, sticky="nsew")

        # Configurar peso de columnas
        parent.grid_columnconfigure(index, weight=1)

        # Contenido de la tarjeta
        content_frame = tk.Frame(card_frame, bg="#1a3a42")
        content_frame.pack(padx=30, pady=30)

        # Nombre de la dificultad
        tk.Label(
            content_frame,
            text=diff_info["name"],
            bg="#1a3a42",
            fg=diff_info["color"],
            font=("TkDefaultFont", 20, "bold")
        ).pack(pady=10)

        # Profundidad
        tk.Label(
            content_frame,
            text=diff_info["depth"],
            bg="#1a3a42",
            fg="white",
            font=("TkDefaultFont", 12)
        ).pack(pady=5)

        # Descripción
        tk.Label(
            content_frame,
            text=diff_info["description"],
            bg="#1a3a42",
            fg="#a0a0a0",
            font=("TkDefaultFont", 10, "italic")
        ).pack(pady=5)

        # Botón de selección
        btn = tk.Button(
            content_frame,
            text="JUGAR",
            bg=diff_info["color"],
            fg="white",
            relief="flat",
            font=("TkDefaultFont", 14, "bold"),
            activebackground=diff_info["hover_color"],
            activeforeground="white",
            command=lambda: self.controller.start_game(diff_info["level"]),
            cursor="hand2",
            width=12,
            height=2
        )
        btn.pack(pady=20)

        # Efecto hover
        def on_enter(e):
            btn.config(bg=diff_info["hover_color"])
            card_frame.config(highlightthickness=4)

        def on_leave(e):
            btn.config(bg=diff_info["color"])
            card_frame.config(highlightthickness=2)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)