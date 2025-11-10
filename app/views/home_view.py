import tkinter as tk
from tkinter import ttk
import os

class HomeView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0B1F25", padx=10, pady=20)        

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        logo_path = os.path.join(base_path, "assets", "logo-md.png")

        self.logo = tk.PhotoImage(file=logo_path)
        tk.Label(self, image=self.logo, bg="#0B1F25").pack()

        tk.Button(
            self,
            text="INICIAR",
            bg="#ffc300",
            fg="white",
            highlightbackground="#fffa85",
            relief="flat",
            font=("TkDefaultFont", 14, "bold"),
            activebackground="#fffcc5",
            activeforeground="#ffc300",
            command=controller.start_game
        ).pack(pady=5)

        tk.Button(
            self,
            text="INSTRUCCIONES",
            bg="#00ced1",
            fg="white",
            highlightbackground="#8efff9",
            relief="flat",
            font=("TkDefaultFont", 14, "bold"),
            activebackground="#c6fffb",
            activeforeground="#00ced1"
        ).pack(pady=5)