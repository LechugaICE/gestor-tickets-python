# tests/test_prioridad.py
from logica.automatizacion import calcular_prioridad

def test_prioridad_alta_emergencias_ti():
    # Detecta servidores y hackeos
    assert calcular_prioridad("Se quemó el servidor principal") == "Alta"
    assert calcular_prioridad("Creo que nos hackearon") == "Alta"

def test_prioridad_baja_mantenimiento_general():
    # Detecta cosas que no son de TI (triviales)
    assert calcular_prioridad("La cafetera está botando agua") == "Baja"
    assert calcular_prioridad("La puerta rechina mucho") == "Baja"

def test_prioridad_moderada_soporte_normal():
    # Detecta problemas de TI de nivel usuario
    assert calcular_prioridad("Mi zona no tiene wifi") == "Moderada"
    assert calcular_prioridad("Mi computadora está muy lenta") == "Moderada"

def test_prioridad_defecto_desconocido():
    # Si alguien escribe algo sin sentido, por seguridad debe ser Moderada
    assert calcular_prioridad("hjksdfh sdkjf") == "Moderada"