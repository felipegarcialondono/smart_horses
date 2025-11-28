import tkinter as tk
import os

class DifficultyView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0B1F25")
        self.controller = controller

        # Fuentes consistentes con home_view
        self.FONT_TITLE = ("Calibri", 26, "bold")
        self.FONT_CARD_TITLE = ("Calibri", 18, "bold")
        self.FONT_CARD_INFO = ("Calibri", 12)
        self.FONT_CARD_DESC = ("Calibri", 10, "italic")
        self.FONT_BTN = ("Calibri", 14, "bold")
        self.FONT_BACK = ("Calibri", 12, "bold")

        # Título con mejor estilo
        title_frame = tk.Frame(self, bg="#0B1F25")
        title_frame.pack(pady=(30, 20))
        
        tk.Label(
            title_frame,
            text="SELECCIONA LA DIFICULTAD",
            bg="#0B1F25",
            fg="#ffc300",
            font=self.FONT_TITLE
        ).pack()

        # Línea decorativa
        tk.Frame(
            title_frame,
            bg="#ffc300",
            height=3,
            width=400
        ).pack(pady=(10, 0))

        # Contenedor de los botones de dificultad
        buttons_container = tk.Frame(self, bg="#0B1F25")
        buttons_container.pack(expand=True, pady=30)

        # Información de cada dificultad
        difficulties = [
            {
                "name": "PRINCIPIANTE",
                "level": "BEGGINER",
                "depth": "Profundidad: 2",
                "description": "Ideal para empezar",
                "color": "#00a36c",
                "hover_color": "#00cc87",
                "light_color": "#00d99a"
            },
            {
                "name": "AMATEUR",
                "level": "AMATEUR",
                "depth": "Profundidad: 4",
                "description": "Desafío moderado",
                "color": "#ffc300",
                "hover_color": "#ffd633",
                "light_color": "#ffe066"
            },
            {
                "name": "EXPERTO",
                "level": "EXPERT",
                "depth": "Profundidad: 6",
                "description": "Para jugadores avanzados",
                "color": "#d63031",
                "hover_color": "#ff4d4f",
                "light_color": "#ff6b6d"
            }
        ]

        # Crear un botón para cada dificultad
        for i, diff in enumerate(difficulties):
            self._create_difficulty_card(buttons_container, diff, i)

        # Botón de volver mejorado
        back_btn = tk.Button(
            self,
            text="← VOLVER",
            bg="#226d7c",
            fg="white",
            relief="flat",
            font=self.FONT_BACK,
            activebackground="#2a8a9e",
            activeforeground="white",
            command=lambda: controller.show_view("home"),
            cursor="hand2",
            width=18,
            borderwidth=0,
            highlightthickness=0
        )
        back_btn.pack(pady=(20, 30))

        # Hover para botón volver
        def on_enter_back(e):
            back_btn.config(bg="#2a8a9e")
        
        def on_leave_back(e):
            back_btn.config(bg="#226d7c")
        
        back_btn.bind("<Enter>", on_enter_back)
        back_btn.bind("<Leave>", on_leave_back)

    def _create_difficulty_card(self, parent, diff_info, index):
        """Crea una tarjeta para cada nivel de dificultad"""
        # Frame contenedor de la tarjeta con mejor diseño
        card_frame = tk.Frame(
            parent,
            bg="#1a3a42",
            relief="flat",
            borderwidth=0
        )
        card_frame.grid(row=0, column=index, padx=25, pady=20, sticky="nsew")

        # Configurar peso de columnas
        parent.grid_columnconfigure(index, weight=1)

        # Frame interno con borde destacado
        inner_frame = tk.Frame(
            card_frame,
            bg=diff_info["color"],
            relief="flat",
            borderwidth=0
        )
        inner_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Contenido de la tarjeta
        content_frame = tk.Frame(inner_frame, bg="#1a3a42")
        content_frame.pack(fill="both", expand=True, padx=3, pady=3)

        # Espaciado superior
        tk.Frame(content_frame, bg="#1a3a42", height=20).pack()

        # Nombre de la dificultad con mejor estilo
        title_label = tk.Label(
            content_frame,
            text=diff_info["name"],
            bg="#1a3a42",
            fg=diff_info["color"],
            font=self.FONT_CARD_TITLE
        )
        title_label.pack(pady=(5, 15))

        # Línea decorativa bajo el título
        tk.Frame(
            content_frame,
            bg=diff_info["color"],
            height=2,
            width=150
        ).pack(pady=(0, 15))

        # Profundidad con mejor presentación
        depth_label = tk.Label(
            content_frame,
            text=diff_info["depth"],
            bg="#1a3a42",
            fg="#ffffff",
            font=self.FONT_CARD_INFO
        )
        depth_label.pack(pady=8)

        # Descripción
        desc_label = tk.Label(
            content_frame,
            text=diff_info["description"],
            bg="#1a3a42",
            fg="#b0b0b0",
            font=self.FONT_CARD_DESC
        )
        desc_label.pack(pady=8)

        # Espaciado antes del botón
        tk.Frame(content_frame, bg="#1a3a42", height=15).pack()

        # Botón de selección mejorado
        def on_button_click(lvl=diff_info["level"]):
            print(f"🎮 [DIFICULTAD] Botón JUGAR clickeado - Nivel recibido: {lvl}")
            self.controller.start_game(lvl)
        
        btn = tk.Button(
            content_frame,
            text="JUGAR",
            bg=diff_info["color"],
            fg="white",
            relief="flat",
            font=self.FONT_BTN,
            activebackground=diff_info["hover_color"],
            activeforeground="white",
            command=lambda lvl=diff_info["level"]: on_button_click(lvl),
            cursor="hand2",
            width=18,
            height=2,
            borderwidth=0,
            highlightthickness=0
        )
        btn.pack(pady=(10, 25))

        # Guardar referencias locales para evitar problemas de closure
        btn_color = diff_info["color"]
        btn_hover_color = diff_info["hover_color"]
        card_border_color = diff_info["color"]
        level = diff_info["level"]

        # Efecto hover simple - solo cambio de color sin afectar el layout
        def on_enter(e, button=btn, hover_color=btn_hover_color, card=inner_frame):
            button.config(bg=hover_color)
            card.config(bg=hover_color)

        def on_leave(e, button=btn, normal_color=btn_color, card=inner_frame, border_color=card_border_color):
            button.config(bg=normal_color)
            card.config(bg=border_color)

        # Hover en toda la tarjeta - usando default parameters en los lambdas para capturar valores
        card_frame.bind("<Enter>", lambda e, b=btn, h=btn_hover_color, c=inner_frame: on_enter(e, b, h, c))
        card_frame.bind("<Leave>", lambda e, b=btn, n=btn_color, c=inner_frame, bc=card_border_color: on_leave(e, b, n, c, bc))
        inner_frame.bind("<Enter>", lambda e, b=btn, h=btn_hover_color, c=inner_frame: on_enter(e, b, h, c))
        inner_frame.bind("<Leave>", lambda e, b=btn, n=btn_color, c=inner_frame, bc=card_border_color: on_leave(e, b, n, c, bc))
        content_frame.bind("<Enter>", lambda e, b=btn, h=btn_hover_color, c=inner_frame: on_enter(e, b, h, c))
        content_frame.bind("<Leave>", lambda e, b=btn, n=btn_color, c=inner_frame, bc=card_border_color: on_leave(e, b, n, c, bc))
        btn.bind("<Enter>", lambda e, b=btn, h=btn_hover_color, c=inner_frame: on_enter(e, b, h, c))
        btn.bind("<Leave>", lambda e, b=btn, n=btn_color, c=inner_frame, bc=card_border_color: on_leave(e, b, n, c, bc))
        
        # Click en toda la tarjeta también activa el botón
        def on_card_click(e, lvl=level):
            print(f"🎮 [DIFICULTAD] Tarjeta clickeada - Nivel recibido: {lvl}")
            self.controller.start_game(lvl)
        
        card_frame.bind("<Button-1>", lambda e, l=level: on_card_click(e, l))
        inner_frame.bind("<Button-1>", lambda e, l=level: on_card_click(e, l))
        content_frame.bind("<Button-1>", lambda e, l=level: on_card_click(e, l))