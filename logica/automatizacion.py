# logica/automatizacion.py
def calcular_prioridad(problema):
    texto = problema.lower()
    
    # 1. Definimos nuestras categorías (Heurística)
    # Solo ponemos las raíces o palabras clave más evidentes
    criticos = ["servidor", "hack", "colaps", "base de datos", "caído", "virus", "fuego"]
    moderados = ["internet", "wifi", "impresora", "mouse", "teclado", "lento", "pantalla"]
    triviales = ["cafetera", "puerta", "silla", "limpieza", "ruido", "luz", "foco"]
    
    # 2. Lógica de detección usando 'any()' (Mucho más profesional y rápido)
    if any(palabra in texto for palabra in criticos):
        return "Alta"
        
    if any(palabra in texto for palabra in triviales):
        return "Baja"
        
    if any(palabra in texto for palabra in moderados):
        return "Moderada"
        
    # 3. Retorno por defecto si escriben algo rarísimo o genérico
    return "Moderada"