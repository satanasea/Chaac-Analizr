# 🌦️ CHAAC ANALIZR

## Sistema de Monitoreo Ambiental para Obra Civil

Proyecto desarrollado para el curso **Programación para la Ciencia e Ingeniería**  
Universidad Mariano Gálvez de Guatemala — Campus Antigua

---

## 📋 Descripción

CHAAC ANALIZR es un sistema desarrollado en Python para el monitoreo y análisis de condiciones ambientales en obras civiles.

El programa permite cargar registros climáticos desde archivos CSV y analizar automáticamente variables como:

- 🌡️ Temperatura
- 💧 Humedad relativa
- 🌧️ Precipitación pluvial

Con base en estos datos, el sistema genera alertas técnicas para apoyar decisiones importantes en obra, especialmente durante el colado de concreto.

---

## 🚀 Cómo ejecutar

### Requisitos
- Python 3.x instalado
- Librería matplotlib

### Instalación
```bash
pip install matplotlib
```

### Pasos
```bash
# Clona el repositorio
git clone https://github.com/TU_USUARIO/chaac-analizr.git

# Entra a la carpeta
cd chaac-analizr

# Ejecuta el sistema
python main_gui.py
```

---

## 🏗️ Problema que resuelve

En muchas obras civiles las decisiones relacionadas con el colado de concreto se realizan de forma empírica, sin analizar condiciones climáticas reales.

Factores como:
- Temperaturas extremas
- Humedad elevada
- Lluvias intensas

pueden afectar la resistencia y calidad del concreto, provocando:

- Fisuras
- Problemas de fraguado
- Segregación de agregados
- Pérdida de resistencia estructural

CHAAC ANALIZR automatiza este análisis mediante datos climáticos reales almacenados en archivos CSV.

---

## 🌤️ Captura de datos

Los datos climáticos fueron obtenidos manualmente mediante la aplicación de clima **AccuWeather**.

La aplicación proporciona información por horas sobre:

- Temperatura
- Humedad relativa
- Probabilidad y cantidad de lluvia

El proceso utilizado fue el siguiente:

1. Una vez al día se verificaban los datos climáticos horarios dentro de la aplicación.
2. Los registros relevantes eran anotados manualmente.
3. Posteriormente, los datos se transcribían al archivo CSV utilizado por el sistema.
4. Finalmente, el CSV era cargado en CHAAC ANALIZR para realizar el análisis automático.

Este método permitió simular un proceso real de monitoreo ambiental en obra civil utilizando datos climáticos reales.

---

## 📁 Formato del archivo CSV

El sistema utiliza archivos CSV con la siguiente estructura:

```csv
fecha_hora,temperatura_C,humedad_pct,lluvia_mm,ubicacion
2025-01-15 08:00,22.5,68.0,0.0,Zona A
2025-01-15 09:00,24.1,71.0,0.0,Zona A
2025-01-15 10:00,26.3,82.0,2.5,Zona A
```

---

## 🏛️ Arquitectura del sistema

```text
chaac_analizr/
│
├── main_gui.py              # Interfaz gráfica principal
├── analizador.py            # Lógica de análisis y alertas
├── registro_climatico.py    # Lectura y organización del CSV
└── lectura.py               # Modelo de datos climáticos
```

---

## 🧩 Clases del proyecto

### 📌 Lectura
Representa una lectura climática individual.

**Atributos:**
- fecha_hora
- temperatura_C
- humedad_pct
- lluvia_mm
- ubicacion

---

### 📌 RegistroClimatico
Carga el archivo CSV y almacena todas las lecturas.

Funciones principales:
- Leer datos
- Crear objetos Lectura
- Organizar información climática

---

### 📌 Analizador
Evalúa las condiciones climáticas utilizando umbrales técnicos del concreto.

Alertas generadas:
- ✅ CONDICIONES OPTIMAS
- ⚠️ CONDICIONES DE SECADO DEFICIENTES
- ❌ NO RECOMENDABLE COLAR CONCRETO

---

### 📌 App
Interfaz gráfica desarrollada con tkinter.

Muestra:
- Tabla de registros
- Alertas por color
- Métricas
- Gráficas dinámicas

---

## 📊 Sistema de alertas

| Estado | Condición |
|---|---|
| ✅ CONDICIONES OPTIMAS | Temp. entre 10°C y 35°C, humedad < 85%, lluvia < 10 mm |
| ⚠️ SECADO DEFICIENTE | Humedad ≥ 85% |
| ❌ NO COLAR CONCRETO | Lluvia ≥ 10 mm o temperatura fuera de rango |

---

## 📈 Funcionalidades

- Lectura de archivos CSV
- Procesamiento automático de datos
- Análisis climático
- Generación de alertas
- Interfaz gráfica
- Visualización mediante gráficas
- Organización modular
- Programación Orientada a Objetos

---

## 🧠 Conceptos aplicados

| Concepto | Uso en el sistema |
|---|---|
| Clases y objetos | Modelado de lecturas y análisis |
| Encapsulamiento | Organización de datos y métodos |
| Herencia | `App` hereda de `tk.Tk` |
| CSV | Lectura de datos climáticos |
| tkinter | Interfaz gráfica |
| matplotlib | Generación de gráficas |
| if / else | Evaluación de condiciones |
| list | Almacenamiento de lecturas |
| datetime | Manejo de fecha y hora |
| constantes de clase | Umbrales técnicos |

---

## 🔄 Flujo del programa

```text
Usuario carga archivo CSV
            ↓
RegistroClimatico lee datos
            ↓
Lectura convierte tipos de datos
            ↓
Analizador evalúa condiciones
            ↓
App muestra alertas y gráficas
```

---

## 🖥️ Interfaz del sistema

La aplicación incluye:

- 📋 Tabla de monitoreo climático
- 📊 Gráficas de temperatura, humedad y lluvia
- 🎨 Sistema de alertas por colores
- 📌 Tarjetas de métricas globales

---

## 📂 Archivos

```text
chaac_analizr/
├── main_gui.py
├── analizador.py
├── registro_climatico.py
├── lectura.py
├── datos_climaticos.csv
└── README.md
```

---

## 🎬 Presentación del proyecto

Durante la presentación se explica:

- Captura manual de datos climáticos
- Lectura del CSV
- Funcionamiento del sistema
- Programación Orientada a Objetos aplicada
- Gráficas y alertas automáticas

---

## 👤 Autor

**Eduardo Alejandro García González**  
Carnet: 1010-26-22427  
Ingeniería Civil — Universidad Mariano Gálvez de Guatemala

---
