class Analizador:
    TEMP_MAX_CONCRETO = 35.0
    TEMP_MIN_CONCRETO = 10.0
    HUMEDAD_MAX_SECADO = 85.0
    LLUVIA_CRITICA = 10.0

    def __init__(self, lecturas):
        self.lecturas = lecturas

    def evaluar_condicion(self, lectura):
        
        if lectura.lluvia_mm >= self.LLUVIA_CRITICA:
            return "NO RECOMENDABLE COLAR CONCRETO"
        if lectura.humedad_pct >= self.HUMEDAD_MAX_SECADO:
            return "CONDICIONES DE SECADO DEFICIENTES"
        if lectura.temperatura_C >= self.TEMP_MAX_CONCRETO or lectura.temperatura_C <= self.TEMP_MIN_CONCRETO:
            return "NO RECOMENDABLE COLAR CONCRETO"
        return "CONDICIONES OPTIMAS"

    def analizar_todas(self):
        
        resultados = []
        for lectura in self.lecturas:
            alerta = self.evaluar_condicion(lectura)
            resultados.append((lectura, alerta))
        return resultados