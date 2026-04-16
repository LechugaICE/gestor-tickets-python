# logica/gestor.py
from datetime import datetime

class GestorTickets:
    def __init__(self):
        self.tickets = []
        self.contador = 1

    def guardar_nuevo(self, problema, prioridad, comentarios, fecha):
        nuevo_ticket = {
            'id': f'Tik-0{self.contador}',
            'problema': problema,
            'prioridad': prioridad,
            'comentarios': comentarios,
            'fecha': fecha,
            'estado': 'Pendiente'
        }
        self.tickets.append(nuevo_ticket)
        self.contador += 1
        return nuevo_ticket['id']

    # --- MODIFICACIÓN: AHORA RECIBE PARÁMETROS DE FILTRO ---
    def obtener_pendientes(self, filtro_prioridad=None, ordenar_por_fecha=False):
        pendientes = [t for t in self.tickets if t['estado'] == 'Pendiente']

        # Si el usuario apretó un botón de prioridad, filtramos la lista
        if filtro_prioridad:
            pendientes = [t for t in pendientes if t['prioridad'] == filtro_prioridad]

        # Si apretó ordenar por fecha, los ordenamos del más cercano al más lejano
        if ordenar_por_fecha:
            pendientes.sort(key=lambda x: datetime.strptime(x['fecha'], "%d/%m/%Y"))

        return pendientes

    def marcar_completado(self, id_ticket):
        for ticket in self.tickets:
            if ticket['id'] == id_ticket:
                ticket['estado'] = 'Completo'
                break
    def obtener_completos(self):
        """Devuelve solo los tickets que ya fueron resueltos"""
        return [t for t in self.tickets if t['estado'] == 'Completo']

gestor_principal = GestorTickets()