# vistas/completos.py
import tkinter as tk
from tkinter import ttk
from logica.gestor import gestor_principal

class VistaCompletos:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Historial - Tickets Completos")
        self.ventana.geometry("700x400")

        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        # Título superior
        tk.Label(self.ventana, text="✅ Historial de Tickets Resueltos", font=("Arial", 14, "bold"), fg="green").pack(pady=15)

        # Usamos Treeview de nuevo para la tabla
        columnas = ("ID", "Problema", "Prioridad Original", "Fecha Creado/Vence")
        self.tabla = ttk.Treeview(self.ventana, columns=columnas, show="headings")
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")
        
        self.tabla.column("ID", width=80)
        self.tabla.column("Problema", width=300)
        self.tabla.column("Prioridad Original", width=120)
        self.tabla.column("Fecha Creado/Vence", width=150)

        # Forzar tema para que se vea limpio
        style = ttk.Style()
        style.theme_use('default') 

        self.tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botón simple para salir
        tk.Button(self.ventana, text="Cerrar Historial", command=self.ventana.destroy, width=20).pack(pady=10)

    def cargar_datos(self):
        """Carga los tickets que tienen estado 'Completo'"""
        tickets_resueltos = gestor_principal.obtener_completos()
        
        for t in tickets_resueltos:
            # Aquí no ponemos colores de fondo porque ya están resueltos (historial neutral)
            valores = (t['id'], t['problema'], t['prioridad'], t['fecha'])
            self.tabla.insert("", tk.END, values=valores)