from datetime import datetime

class Lectura:
    def __init__(self, fecha_hora, temperatura_C, humedad_pct, lluvia_mm, ubicacion):
        
        self.fecha_hora = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M")
        self.temperatura_C = float(temperatura_C)
        self.humedad_pct = float(humedad_pct)
        self.lluvia_mm = float(lluvia_mm)
        self.ubicacion = ubicacion