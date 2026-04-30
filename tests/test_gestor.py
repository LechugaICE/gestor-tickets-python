# tests/test_gestor.py
from logica.gestor import gestor_principal

def test_flujo_base_de_datos_orm():
    # 1. Simulamos guardar un ticket nuevo en la base de datos
    id_generado = gestor_principal.guardar_nuevo(
        problema="Test de cobertura", 
        prioridad="Baja", 
        comentarios="Prueba automatizada", 
        fecha="01/01/2026"
    )
    
    # Verificamos que sí nos devolvió un ID válido (ej. Tik-01)
    assert id_generado is not None
    assert "Tik-" in id_generado

    # 2. Verificamos que podemos buscar ese ticket específico
    ticket_bd = gestor_principal.obtener_ticket_por_id(id_generado)
    assert ticket_bd is not None
    assert ticket_bd['problema'] == "Test de cobertura"
    assert ticket_bd['estado'] == "Pendiente"

    # 3. Simulamos marcar el ticket como completado
    gestor_principal.marcar_completado(id_generado)

    # 4. Verificamos que ahora aparece en la bandeja de completos
    completos = gestor_principal.obtener_completos()
    
    # Extraemos todos los IDs de los tickets completos para buscar el nuestro
    ids_completos = [t['id'] for t in completos]
    assert id_generado in ids_completos