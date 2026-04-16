# vistas/menu_inicio.py
import tkinter as tk
from tkinter import messagebox
from vistas.nuevo_ticket import VistaNuevoTicket
from vistas.pendientes import VistaPendientes
from vistas.completos import VistaCompletos

class MenuPrincipal:
    def __init__(self):
        self.root = tk.Tk()
 feature/titulo-kelvin
        self.root.title("Sistema de Tickets Oficial")        self.root.geometry("400x350")

 develop
        
        # Título
        tk.Label(self.root, text="MENÚ PRINCIPAL", font=("Arial", 16, "bold")).pack(pady=30)
        
        # Botones
        tk.Button(self.root, text="1. Nuevo Ticket", width=25, height=2, command=self.abrir_nuevo).pack(pady=10)
        tk.Button(self.root, text="2. Tickets Pendientes", width=25, height=2, command=self.abrir_pendientes).pack(pady=10)
        tk.Button(self.root, text="3. Tickets Completos", width=25, height=2, command=self.abrir_completos).pack(pady=10)

    def abrir_nuevo(self):
        
       VistaNuevoTicket(self.root)

    def abrir_pendientes(self):
        VistaPendientes(self.root)

    def abrir_completos(self):
        VistaCompletos(self.root)

    def iniciar(self):
        self.root.mainloop()