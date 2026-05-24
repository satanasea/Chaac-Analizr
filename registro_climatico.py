import csv
from lectura import Lectura

class RegistroClimatico:
    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv
        self.lecturas = []

    def cargar_datos(self):
        self.lecturas = []
        with open(self.ruta_csv, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                
                lectura = Lectura(
                    fila["fecha_hora"],
                    fila["temperatura_C"],
                    fila["humedad_pct"],
                    fila["lluvia_mm"],
                    fila["ubicacion"],
                )
                self.lecturas.append(lectura)

    def obtener_lecturas(self):
        return self.lecturas