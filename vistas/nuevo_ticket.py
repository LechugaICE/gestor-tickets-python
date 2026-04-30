# vistas/nuevo_ticket.py
import tkinter as tk
from tkinter import ttk, messagebox  # ¡Importante! ttk es necesario para el Combobox
from datetime import datetime
from logica.gestor import gestor_principal
from logica.automatizacion import calcular_prioridad

class VistaNuevoTicket:
    def __init__(self, parent, callback_actualizar=None):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Crear Nuevo Ticket")
        self.ventana.geometry("400x550")
        self.ventana.grab_set()

        self.prioridad_seleccionada = None # ### NUEVO: Descomentado para evitar errores si no se selecciona nada
        self.callback_actualizar = callback_actualizar 

        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.ventana, text="Problema (Máx 5 palabras):", font=("Arial", 10, "bold")).pack(pady=(15, 0))
        self.entrada_problema = tk.Entry(self.ventana, width=40)
        self.entrada_problema.pack(pady=5)

        # ### NUEVO:detecta cuando escribes
        self.entrada_problema.bind("<KeyRelease>", self.actualizar_prioridad_en_vivo)

        tk.Label(self.ventana, text="Prioridad:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        
        frame_prioridad = tk.Frame(self.ventana)
        frame_prioridad.pack(pady=5)

        self.btn_verde = tk.Button(frame_prioridad, text="Verde", bg="#ccffcc", width=10, command=lambda: self.seleccionar_prioridad("Verde", self.btn_verde))
        self.btn_verde.pack(side="left", padx=5)
        
        self.btn_amarillo = tk.Button(frame_prioridad, text="Amarillo", bg="#fff5cc", width=10, command=lambda: self.seleccionar_prioridad("Amarilla", self.btn_amarillo))
        self.btn_amarillo.pack(side="left", padx=5)
        
        self.btn_rojo = tk.Button(frame_prioridad, text="Rojo", bg="#ffcccc", width=10, command=lambda: self.seleccionar_prioridad("Roja", self.btn_rojo))
        self.btn_rojo.pack(side="left", padx=5)

        tk.Label(self.ventana, text="Comentarios detallados:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.entrada_comentarios = tk.Text(self.ventana, height=6, width=40)
        self.entrada_comentarios.pack(pady=5)

        # --- SECCIÓN DE FECHAS MEJORADA (Dropdowns) ---
        fecha_hoy_obj = datetime.now()
        fecha_actual_str = fecha_hoy_obj.strftime("%d/%m/%Y")
        tk.Label(self.ventana, text=f"Fecha de creación: {fecha_actual_str}", fg="gray").pack(pady=(10, 5))

        tk.Label(self.ventana, text="Fecha de Vencimiento:", font=("Arial", 10, "bold")).pack(pady=(5, 0))
        
        # Un frame para agrupar los 3 desplegables y las barras "/"
        frame_fecha = tk.Frame(self.ventana)
        frame_fecha.pack(pady=5)

        # Valores para los desplegables (zfill pone el '0' delante, ej: '01', '02')
        dias = [str(i).zfill(2) for i in range(1, 32)]
        meses = [str(i).zfill(2) for i in range(1, 13)]
        anios = ["2026", "2027"]

        # Combobox Día
        self.combo_dia = ttk.Combobox(frame_fecha, values=dias, width=3, state="readonly")
        self.combo_dia.pack(side="left")
        self.combo_dia.set(fecha_hoy_obj.strftime("%d")) # Por defecto el día de hoy

        tk.Label(frame_fecha, text="/", font=("Arial", 12)).pack(side="left", padx=2)

        # Combobox Mes
        self.combo_mes = ttk.Combobox(frame_fecha, values=meses, width=3, state="readonly")
        self.combo_mes.pack(side="left")
        self.combo_mes.set(fecha_hoy_obj.strftime("%m")) # Por defecto el mes actual

        tk.Label(frame_fecha, text="/", font=("Arial", 12)).pack(side="left", padx=2)

        # Combobox Año
        self.combo_anio = ttk.Combobox(frame_fecha, values=anios, width=5, state="readonly")
        self.combo_anio.pack(side="left")
        self.combo_anio.set(fecha_hoy_obj.strftime("%Y")) # Por defecto el año actual

        # --- BOTONES FINALES ---
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Cancelar", command=self.ventana.destroy, width=15).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Confirmar", command=self.validar_y_guardar, bg="lightblue", font=("Arial", 10, "bold"), width=15).pack(side="right", padx=10)

    
    def actualizar_prioridad_en_vivo(self, event):
        texto_actual = self.entrada_problema.get()
        nivel = calcular_prioridad(texto_actual)
        
        # Mapeamos el resultado 
        if nivel == "Baja":
            self.seleccionar_prioridad("Verde", self.btn_verde)
        elif nivel == "Moderada":
            self.seleccionar_prioridad("Amarilla", self.btn_amarillo)
        elif nivel == "Alta":
            self.seleccionar_prioridad("Roja", self.btn_rojo)

    def seleccionar_prioridad(self, color, boton):
        self.prioridad_seleccionada = color
        self.btn_verde.config(relief="raised", borderwidth=2)
        self.btn_amarillo.config(relief="raised", borderwidth=2)
        self.btn_rojo.config(relief="raised", borderwidth=2)
        boton.config(relief="sunken", borderwidth=4)

    def validar_y_guardar(self):
        problema = self.entrada_problema.get().strip()
        comentarios = self.entrada_comentarios.get("1.0", tk.END).strip()
        
        # Obtener valores de los desplegables
        dia = self.combo_dia.get()
        mes = self.combo_mes.get()
        anio = self.combo_anio.get()

        if not problema or not comentarios or not dia or not mes or not anio:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return

        if len(problema.split()) > 5:
            messagebox.showwarning("Error", "El problema máximo es de 5 palabras.")
            return

        if not self.prioridad_seleccionada:
            messagebox.showwarning("Error", "Selecciona una prioridad.")
            return

        # --- VALIDACIÓN EXACTA DE FECHA ---
        vencimiento_str = f"{dia}/{mes}/{anio}"
        
        try:
            # 1. Validar que la fecha exista en el calendario (ej: rechaza 31 de Febrero)
            fecha_vencimiento = datetime.strptime(vencimiento_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "La fecha seleccionada no es válida en el calendario.")
            return

        # 2. Validar que no sea una fecha en el pasado
        fecha_hoy = datetime.now().date() # Solo extraemos la fecha (sin la hora)
        if fecha_vencimiento.date() < fecha_hoy:
            messagebox.showwarning("Error", "La fecha de vencimiento no puede estar en el pasado. Debe ser hoy o a futuro.")
            return

        # Guardar datos
        try:
            id_generado = gestor_principal.guardar_nuevo(problema, self.prioridad_seleccionada, comentarios, vencimiento_str)
            messagebox.showinfo("Éxito", f"Se ha creado el ticket: {id_generado}")
            
            if self.callback_actualizar:
                self.callback_actualizar()
                
            self.ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")