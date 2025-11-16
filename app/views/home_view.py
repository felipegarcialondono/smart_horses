import tkinter as tk
import os
from PIL import Image, ImageTk

class HomeView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0B1F25")
        self.controller = controller

        FONT_FALLBACK_NAMES = "Calibri Segoe UI Symbol Noto Color Emoji"

        self.FONT_BASE = ("Calibri", 12)
        self.FONT_TITLE = ("Calibri", 18, "bold")
        self.FONT_BTN_LARGE = ("Calibri", 16, "bold")
        self.FONT_BTN_MEDIUM = ("Calibri", 14, "bold")
        self.FONT_BTN_SMALL = ("Calibri", 12, "bold")
        self.FONT_INSTR_TITLE = (FONT_FALLBACK_NAMES, 14, "bold")
        self.FONT_INSTR_BODY = (FONT_FALLBACK_NAMES, 11)

        main_content_frame = tk.Frame(self, bg="#0B1F25")
        main_content_frame.pack(expand=True)

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        logo_path = os.path.join(base_path, "assets", "logo-md.png")

        try:
            img_pil = Image.open(logo_path)
            self.logo = ImageTk.PhotoImage(img_pil)
            logo_label = tk.Label(main_content_frame, image=self.logo, bg="#0B1F25")
            logo_label.pack(pady=30)
        except FileNotFoundError:
            print(f"Error: No se encontró la imagen en {logo_path}")
            tk.Label(
                main_content_frame, 
                text="Smart Horses", 
                font=("Calibri", 30, "bold"), 
                bg="#0B1F25", 
                fg="#ffc300"
            ).pack(pady=30)
        except Exception as e:
            print(f"Error al cargar la imagen con Pillow: {e}")
            tk.Label(
                main_content_frame, 
                text="Smart Horses (Error Imagen)", 
                font=("Calibri", 24, "bold"), 
                bg="#0B1F25", 
                fg="red"
            ).pack(pady=30)

        description_frame = tk.Frame(main_content_frame, bg="#1a3a42", relief="raised", borderwidth=2)
        description_frame.pack(pady=20, padx=40, fill="x")

        tk.Label(
            description_frame,
            text="Smart Horses",
            bg="#1a3a42",
            fg="#ffc300",
            font=self.FONT_TITLE
        ).pack(pady=10)

        tk.Label(
            description_frame,
            text="Juego de estrategia para dos jugadores.\nMueve tu caballo y acumula más puntos que la computadora.",
            bg="#1a3a42",
            fg="white",
            font=self.FONT_BASE,
            justify="center"
        ).pack(pady=10, padx=20)

        BTN_WIDTH = 22
        
        start_btn = tk.Button(
            main_content_frame,
            text="INICIAR JUEGO",
            bg="#ffc300",
            fg="#0B1F25",
            relief="flat",
            font=self.FONT_BTN_LARGE,
            activebackground="#fffcc5",
            activeforeground="#e0ac00",
            command=lambda: [controller.music_player.play_sound("click"), controller.show_view("difficulty")],
            cursor="hand2",
            width=BTN_WIDTH,
            height=2,
            borderwidth=0,
            highlightthickness=0
        )
        start_btn.pack(pady=15)

        def on_enter(e):
            start_btn.config(bg="#e0ac00")

        def on_leave(e):
            start_btn.config(bg="#ffc300")

        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)

        instructions_btn = tk.Button(
            main_content_frame,
            text="INSTRUCCIONES",
            bg="#00ced1",
            fg="white",
            relief="flat",
            font=self.FONT_BTN_MEDIUM,
            activebackground="#c6fffb",
            activeforeground="#00b2b5",
            command=lambda: [controller.music_player.play_sound("click"), self.show_instructions()],
            cursor="hand2",
            width=BTN_WIDTH,
            borderwidth=0,
            highlightthickness=0
        )
        instructions_btn.pack(pady=5)

        def on_enter_inst(e):
            instructions_btn.config(bg="#00b2b5")

        def on_leave_inst(e):
            instructions_btn.config(bg="#00ced1")

        instructions_btn.bind("<Enter>", on_enter_inst)
        instructions_btn.bind("<Leave>", on_leave_inst)

        # Control de volumen
        volume_frame = tk.Frame(main_content_frame, bg="#0B1F25")
        volume_frame.pack(pady=10)

        tk.Label(volume_frame, text="🔊 Volumen:", bg="#0B1F25", fg="white",
                font=("Calibri", 10)).pack()

        volume_slider = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient="horizontal",
            bg="#1a3a42",
            fg="white",
            highlightthickness=0,
            length=200,
            command=lambda v: controller.music_player.set_volume(int(v) / 100)
        )
        volume_slider.set(30)
        volume_slider.pack()

        exit_btn = tk.Button(
            main_content_frame,
            text="SALIR",
            bg="#d63031",
            fg="white",
            relief="flat",
            font=self.FONT_BTN_SMALL,
            activebackground="#fde3e3",
            activeforeground="#c02a2b",
            command=parent.destroy,
            cursor="hand2",
            width=BTN_WIDTH,
            borderwidth=0,
            highlightthickness=0
        )
        exit_btn.pack(pady=15)

        def on_enter_exit(e):
            exit_btn.config(bg="#c02a2b")

        def on_leave_exit(e):
            exit_btn.config(bg="#d63031")

        exit_btn.bind("<Enter>", on_enter_exit)
        exit_btn.bind("<Leave>", on_leave_exit)

    def show_instructions(self):
        """Muestra una ventana con las instrucciones del juego (con scroll e iconos)"""
        instructions_window = tk.Toplevel(self.master)
        instructions_window.title("Instrucciones")
        instructions_window.geometry("550x500")
        instructions_window.configure(bg="#0B1F25")
        instructions_window.transient(self.master)
        instructions_window.grab_set()
        instructions_window.resizable(False, False)

        tk.Label(
            instructions_window,
            text="INSTRUCCIONES",
            bg="#0B1F25",
            fg="#ffc300",
            font=("Calibri", 20, "bold")
        ).pack(pady=20)

        container_frame = tk.Frame(instructions_window, bg="#1a3a42", relief="raised", borderwidth=2)
        container_frame.pack(pady=10, padx=30, fill="both", expand=True)

        canvas = tk.Canvas(container_frame, bg="#1a3a42", highlightthickness=0)
        
        scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas, bg="#1a3a42")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        icons_path = os.path.join(base_path, "assets", "icons")
        
        icons_available = True
        try:
            self.icon_target = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "target.png")).resize((24, 24)))
            self.icon_horse = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "horse.png")).resize((24, 24)))
            self.icon_star = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "star.png")).resize((24, 24)))
            self.icon_warning = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "warning.png")).resize((24, 24)))
            self.icon_trophy = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "trophy.png")).resize((24, 24)))
            self.icon_bulb = ImageTk.PhotoImage(Image.open(os.path.join(icons_path, "bulb.png")).resize((24, 24)))
        except Exception as e:
            print(f"No se pudieron cargar los iconos: {e}")
            icons_available = False

        def create_section(parent, title, text, icon=None, fallback_color="#ffc300"):
            WRAP_LENGTH = 400 
            
            section_frame = tk.Frame(parent, bg="#1a3a42")
            section_frame.pack(fill="x", pady=10, padx=10)
            
            if icons_available and icon:
                icon_label = tk.Label(section_frame, image=icon, bg="#1a3a42")
                icon_label.image = icon
                icon_label.pack(side="left", padx=(0, 10), anchor="n", pady=2)
            else:
                icon_canvas = tk.Canvas(section_frame, width=24, height=24, bg="#1a3a42", highlightthickness=0)
                icon_canvas.pack(side="left", padx=(0, 10), anchor="n", pady=2)
                icon_canvas.create_oval(4, 4, 20, 20, fill=fallback_color, outline=fallback_color)
            
            text_frame = tk.Frame(section_frame, bg="#1a3a42")
            text_frame.pack(side="left", fill="x", expand=True)
            
            tk.Label(
                text_frame,
                text=title,
                font=self.FONT_INSTR_TITLE,
                bg="#1a3a42",
                fg="#ffc300",
                justify="left"
            ).pack(anchor="w")
            
            tk.Label(
                text_frame,
                text=text.strip(),
                font=self.FONT_INSTR_BODY,
                bg="#1a3a42",
                fg="white",
                justify="left",
                wraplength=WRAP_LENGTH
            ).pack(anchor="w", pady=(5, 0))

        create_section(
            scrollable_frame, 
            "OBJETIVO", 
            "Acumula más puntos que la computadora moviendo tu caballo estratégicamente por el tablero.",
            icon=self.icon_target if icons_available else None,
            fallback_color="#00a36c"
        )
        create_section(
            scrollable_frame,
            "MOVIMIENTO",
            'Los caballos se mueven en forma de "L" (como en ajedrez): 2 casillas en una dirección + 1 casilla perpendicular.',
            icon=self.icon_horse if icons_available else None,
            fallback_color="#00ced1"
        )
        create_section(
            scrollable_frame,
            "PUNTOS",
            "• Casillas verdes: Suman puntos (+1, +3, +4, +5, +10)\n"
            "• Casillas rojas: Restan puntos (-1, -3, -4, -5, -10)\n"
            "• Cada casilla visitada se destruye (roja oscura)",
            icon=self.icon_star if icons_available else None,
            fallback_color="#ffc300"
        )
        create_section(
            scrollable_frame,
            "PENALIZACIÓN",
            "Si un jugador no puede moverse pero su oponente sí, recibe -4 puntos de penalización.",
            icon=self.icon_warning if icons_available else None,
            fallback_color="#d63031"
        )
        create_section(
            scrollable_frame,
            "VICTORIA",
            "Gana quien tenga más puntos cuando ninguno de los dos jugadores pueda realizar un movimiento válido.",
            icon=self.icon_trophy if icons_available else None,
            fallback_color="#ffc300"
        )
        create_section(
            scrollable_frame,
            "CONSEJO",
            "Planifica tus movimientos para tomar las casillas de alto valor y, al mismo tiempo, bloquear las mejores opciones de tu oponente.",
            icon=self.icon_bulb if icons_available else None,
            fallback_color="#226d7c"
        )

        BTN_WIDTH = 22
        close_btn = tk.Button(
            instructions_window,
            text="CERRAR",
            bg="#ffc300",
            fg="#0B1F25",
            relief="flat",
            font=self.FONT_BTN_SMALL,
            command=instructions_window.destroy,
            cursor="hand2",
            width=BTN_WIDTH,
            borderwidth=0,
            highlightthickness=0
        )
        close_btn.pack(pady=20)

        def on_enter_close(e):
            close_btn.config(bg="#e0ac00")

        def on_leave_close(e):
            close_btn.config(bg="#ffc300")

        close_btn.bind("<Enter>", on_enter_close)
        close_btn.bind("<Leave>", on_leave_close)
