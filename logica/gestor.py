# logica/gestor.py
from datetime import datetime
from logica.modelos import SessionLocal, TicketORM

class GestorTickets:
    def __init__(self):
        #self.tickets = []
        #self.contador = 1
        pass
    def guardar_nuevo(self, problema, prioridad, comentarios, fecha):
        db = SessionLocal() # Abrimos conexión a la base de datos
        try:
            total_tickets = db.query(TicketORM).count()
            nuevo_id = f'Tik-0{total_tickets + 1}'
            
            # Creamos el objeto ORM
            nuevo_ticket = TicketORM(
                codigo=nuevo_id,
                problema=problema,
                prioridad=prioridad,
                comentarios=comentarios,
                fecha=fecha,
                estado='Pendiente'
            )

            db.add(nuevo_ticket)
            db.commit() # Guardamos definitivamente en el archivo físico
            return nuevo_id
        except Exception as e:
            db.rollback() # Si algo falla, cancelamos la operación por seguridad
            raise e
        finally:
            db.close() # Siempre cerramos la conexión

    def obtener_pendientes(self, filtro_prioridad=None, ordenar_por_fecha=False):
        db = SessionLocal()
        try:
            # Consulta SQL traducida a Python (ORM)
            query = db.query(TicketORM).filter(TicketORM.estado == 'Pendiente')
            
            if filtro_prioridad:
                query = query.filter(TicketORM.prioridad == filtro_prioridad)
                
            pendientes_orm = query.all()
            
            # Convertimos los objetos ORM a diccionarios simples
            # Para que nuestras vistas de Tkinter no se rompan y sigan funcionando igual
            lista_pendientes = [{
                'id': t.codigo,
                'problema': t.problema,
                'prioridad': t.prioridad,
                'comentarios': t.comentarios,
                'fecha': t.fecha,
                'estado': t.estado
            } for t in pendientes_orm]

            if ordenar_por_fecha:
                lista_pendientes.sort(key=lambda x: datetime.strptime(x['fecha'], "%d/%m/%Y"))
                
            return lista_pendientes
        finally:
            db.close()

    def obtener_ticket_por_id(self, id_ticket):
        """Busca un ticket específico en la base de datos por su ID"""
        db = SessionLocal()
        try:
            t = db.query(TicketORM).filter(TicketORM.codigo == id_ticket).first()
            if t:
                return {
                    'id': t.codigo,
                    'problema': t.problema,
                    'prioridad': t.prioridad,
                    'comentarios': t.comentarios,
                    'fecha': t.fecha,
                    'estado': t.estado
                }
            return None
        finally:
            db.close()
            
    def obtener_completos(self):
        db = SessionLocal()
        try:
            completos_orm = db.query(TicketORM).filter(TicketORM.estado == 'Completo').all()
            return [{
                'id': t.codigo,
                'problema': t.problema,
                'prioridad': t.prioridad,
                'comentarios': t.comentarios,
                'fecha': t.fecha,
                'estado': t.estado
            } for t in completos_orm]
        finally:
            db.close()

    def marcar_completado(self, id_ticket):
        db = SessionLocal()
        try:
            # Buscamos el ticket por su código y le actualizamos el estado
            ticket = db.query(TicketORM).filter(TicketORM.codigo == id_ticket).first()
            if ticket:
                ticket.estado = 'Completo'
                db.commit()
        finally:
            db.close()

# Mantenemos la instancia global para las vistas
gestor_principal = GestorTickets()