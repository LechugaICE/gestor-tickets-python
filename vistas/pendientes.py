# vistas/pendientes.py
import tkinter as tk
from tkinter import ttk, messagebox
from logica.gestor import gestor_principal
from vistas.nuevo_ticket import VistaNuevoTicket

class VistaPendientes:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Bandeja de Tickets Pendientes")
        self.ventana.geometry("850x550")

        self.crear_interfaz()
        self.actualizar_tabla()

    def crear_interfaz(self):
        panel_izq = tk.Frame(self.ventana, bg="#e0e0e0", width=200)
        panel_izq.pack(side="left", fill="y")
        
        tk.Button(panel_izq, text="+ NUEVO TICKET", bg="white", font=("Arial", 10, "bold"), command=self.abrir_nuevo_ticket).pack(pady=20, padx=10, fill="x")
        
        tk.Label(panel_izq, text="Filtros Prioridad", bg="#e0e0e0", font=("Arial", 9, "bold")).pack(pady=(10, 5))
        # MODIFICACIÓN: Los botones ahora envían su color como filtro usando lambda
        tk.Button(panel_izq, text="Alta", bg="#ffcccc", command=lambda: self.actualizar_tabla(filtro_prio="Roja")).pack(fill="x", padx=10, pady=2)
        tk.Button(panel_izq, text="Moderada", bg="#fff5cc", command=lambda: self.actualizar_tabla(filtro_prio="Amarilla")).pack(fill="x", padx=10, pady=2)
        tk.Button(panel_izq, text="Baja", bg="#ccffcc", command=lambda: self.actualizar_tabla(filtro_prio="Verde")).pack(fill="x", padx=10, pady=2)
        
        # Botón extra para quitar los filtros
        tk.Button(panel_izq, text="Mostrar Todos", command=self.actualizar_tabla).pack(fill="x", padx=10, pady=10)

        tk.Label(panel_izq, text="Filtros Fecha", bg="#e0e0e0", font=("Arial", 9, "bold")).pack(pady=(10, 5))
        # MODIFICACIÓN: Ordena por fecha
        tk.Button(panel_izq, text="Ordenar (Más próximo)", command=lambda: self.actualizar_tabla(ordenar=True)).pack(fill="x", padx=10, pady=2)

        panel_der = tk.Frame(self.ventana)
        panel_der.pack(side="right", fill="both", expand=True)

        tk.Label(panel_der, text="Tickets Pendientes", font=("Arial", 14, "bold")).pack(pady=10)
        
        style = ttk.Style()
        style.theme_use('default') 
        
        columnas = ("Prioridad", "N° Ticket", "Problema", "Vencimiento")
        self.tabla = ttk.Treeview(panel_der, columns=columnas, show="headings")
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")
        
        self.tabla.column("Prioridad", width=140)
        self.tabla.column("N° Ticket", width=80)
        self.tabla.column("Problema", width=250)
        self.tabla.column("Vencimiento", width=100)

        self.tabla.tag_configure('Roja', background='#ffcccc')
        self.tabla.tag_configure('Amarilla', background='#fff5cc')
        self.tabla.tag_configure('Verde', background='#ccffcc')

        self.tabla.pack(fill="both", expand=True, padx=20, pady=10)
        self.tabla.bind("<Double-1>", self.abrir_detalle)

    # MODIFICACIÓN: Recibe parámetros de filtro
    def actualizar_tabla(self, filtro_prio=None, ordenar=False):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
            
        tickets = gestor_principal.obtener_pendientes(filtro_prioridad=filtro_prio, ordenar_por_fecha=ordenar)
        
        for t in tickets:
            prio_texto = t['prioridad']
            if prio_texto == "Roja":
                prio_visual = "🔴 Roja (Alta)"
            elif prio_texto == "Amarilla":
                prio_visual = "🟡 Amarilla (Mod)"
            else:
                prio_visual = "🟢 Verde (Baja)"

            valores = (prio_visual, t['id'], t['problema'], t['fecha'])
            self.tabla.insert("", tk.END, values=valores, tags=(t['prioridad'],))

    def abrir_nuevo_ticket(self):
        # MODIFICACIÓN: Le pasamos la función "self.actualizar_tabla" al formulario
        # para que se refresque automáticamente cuando se guarde el ticket
        VistaNuevoTicket(self.ventana, callback_actualizar=self.actualizar_tabla)

    def abrir_detalle(self, event):
        seleccion = self.tabla.focus()
        if not seleccion:
            return
            
        valores = self.tabla.item(seleccion, 'values')
        id_ticket = valores[1]
        
        #ticket_data = next((t for t in gestor_principal.tickets if t['id'] == id_ticket), None)
        ticket_data = gestor_principal.obtener_ticket_por_id(id_ticket)
        if ticket_data:
            VistaDetalle(self.ventana, ticket_data, self.actualizar_tabla)

class VistaDetalle:
    def __init__(self, parent, ticket, callback_actualizar):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Detalle - {ticket['id']}")
        self.ventana.geometry("350x300")
        self.id_ticket = ticket['id']
        self.callback_actualizar = callback_actualizar 

        tk.Label(self.ventana, text=f"Problema: {ticket['problema']}", font=("Arial", 11, "bold")).pack(pady=10)
        tk.Label(self.ventana, text="Comentarios completos:", font=("Arial", 9, "bold")).pack()
        
        caja = tk.Text(self.ventana, height=6, width=35)
        caja.insert(tk.END, ticket['comentarios'])
        caja.config(state="disabled")
        caja.pack(pady=5)

        tk.Button(self.ventana, text="✔ Marcar como Completo", bg="lightgreen", font=("Arial", 10, "bold"), command=self.completar).pack(pady=10)
        tk.Button(self.ventana, text="Cerrar", command=self.ventana.destroy).pack()

    def completar(self):
        gestor_principal.marcar_completado(self.id_ticket)
        messagebox.showinfo("Éxito", f"El ticket {self.id_ticket} se movió a Completos.")
        self.callback_actualizar()
        self.ventana.destroy()