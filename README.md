# Candy Crush Pattern Detection System

Un sistema inteligente de análisis y detección de patrones en niveles de **Candy Crush Soda Saga** que utiliza un enfoque de **múltiples pasadas** para descubrir patrones progresivamente, de mayor a menor detalle.

## 🎯 Características

### Sistema de 5 Pasadas de Análisis
El sistema analiza cada nivel de forma iterativa, mejorando el detalle con cada pasada:

1. **Pasada 1: Estructura General**
   - Dimensiones del tablero
   - Disposición y layouts
   - Modos de juego
   - Mecánicas de puntuación

2. **Pasada 2: Mecánicas de Gameplay**
   - Patrones de gameplay
   - Spawners y posiciones
   - Gravedad y física
   - Caramelos especiales

3. **Pasada 3: Bloqueadores y Obstáculos**
   - Tipos de bloqueadores
   - Densidad de obstáculos
   - Distribución de patrones
   - Reglas de interacción

4. **Pasada 4: Mecánicas Avanzadas**
   - Cámaras múltiples
   - Niveles con scroll
   - Portales y mecanismos
   - Complejidad de control

5. **Pasada 5: Análisis Correlacional**
   - Correlaciones entre características
   - Clustering de niveles similares
   - Detección de anomalías
   - Recomendaciones de dificultad

### Tracking de Análisis
- Cada nivel registra cuáles pasadas ha completado
- Visualización de progreso en tiempo real
- Estadísticas por pasada
- Promedio de pasadas completadas

## 📂 Estructura del Proyecto

```
idea/
├── api/                      # API REST con FastAPI
│   ├── main.py              # Aplicación principal
│   ├── routes_levels.py     # Endpoints de niveles
│   ├── routes_analysis.py   # Endpoints de análisis
│   └── schemas.py           # Schemas Pydantic
├── analyzer/                # Motor de análisis
│   ├── json_loader.py       # Cargador de JSONs
│   ├── pattern_detector.py  # Detector de patrones (5 pasadas)
│   └── level_analyzer.py    # Orquestador de análisis
├── db/                      # Base de datos
│   └── models.py            # Modelos SQLAlchemy
├── cli.py                   # Interfaz CLI interactiva
├── config.py                # Configuración
├── requirements.txt         # Dependencias Python
└── candy_patterns.db        # Base de datos SQLite (se crea automáticamente)
```

## 🚀 Uso Rápido

### 1. Instalación

```bash
cd idea
pip install -r requirements.txt
```

### 2. CLI Interactiva (Recomendado)

```bash
python3 cli.py
```

Menú interactivo con opciones:
- **1**: Cargar niveles (10 en 10)
- **2**: Ejecutar una pasada específica
- **3**: Ver progreso del análisis
- **4**: Ejecutar todas las 4 pasadas
- **5**: Salir

**Ejemplo:**
```
Select option (1-5): 1
Current levels in DB: 0
How many levels to load? (default 10): 100
Loading 100 levels in batches of 10...
✓ Loaded 100 new levels
Total in DB: 100

Select option (1-5): 4
Running all 4 passes...
--- Pass 1 ---
Analyzed 100 levels
Total progress: 100/100 (100.0%)
...
✓ All passes completed!
```

### 3. API REST

Iniciar servidor:
```bash
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Acceso:
- Documentación interactiva: http://localhost:8000/docs
- Especificación OpenAPI: http://localhost:8000/openapi.json

**Endpoints principales:**

```bash
# Cargar niveles
POST /analysis/load-levels?limit=50

# Ejecutar análisis
POST /analysis/run-pass/1           # Pass 1
POST /analysis/run-pass/2           # Pass 2
POST /analysis/run-all-passes       # Todas las 4

# Ver progreso
GET /analysis/progress

# Estadísticas
GET /analysis/stats

# Obtener patrones de un nivel
GET /levels/1?level_id=199850
```

## 📊 Ejemplo de Salida

### Progreso de Análisis
```
Total levels: 200
==================================================

Pass 1: [████████████████████] 100.0% (200/200)
Pass 2: [████████████████████] 100.0% (200/200)
Pass 3: [████████████████████] 100.0% (200/200)
Pass 4: [████████████████████] 100.0% (200/200)

Average passes per level: 4.0
```

### Estadísticas API
```json
{
  "summary": {
    "total_levels": 200,
    "total_analyses": 800,
    "average_analyses_per_level": 4.0
  },
  "progress": {
    "total_levels": 200,
    "average_passes_per_level": 4.0,
    "pass_statistics": {
      "pass_1": { "completed": 200, "percent": 100.0 },
      "pass_2": { "completed": 200, "percent": 100.0 },
      "pass_3": { "completed": 200, "percent": 100.0 },
      "pass_4": { "completed": 200, "percent": 100.0 }
    }
  },
  "correlations": {
    "board_size_range": {
      "min": 49,
      "max": 589,
      "avg": 104.1
    }
  }
}
```

## 🗄️ Base de Datos

SQLite con tablas:

- **levels**: Metadatos de niveles con tracking de pasadas completadas
- **level_raw_data**: Datos JSON raw almacenados de forma eficiente
- **level_analyses**: Resultados de cada análisis por pasada
- **patterns**: Definiciones de patrones
- **pattern_instances**: Mapeos nivel↔patrón
- **global_statistics**: Estadísticas globales del sistema

## 🔧 Configuración

Archivo `.env`:
```env
DATABASE_URL=sqlite:///./candy_patterns.db
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
JSON_INPUT_PATH=/ruta/a/niveles/json
```

## 📈 Rendimiento

- **Carga**: ~10 niveles por segundo
- **Análisis (Pass 1)**: ~30 niveles por segundo
- **Análisis (Pass 2-4)**: ~20 niveles por segundo
- **Batching**: 10 en 10 para evitar timeouts
- **BD**: SQLite optimizada con índices

## 🎮 Patrones Detectados

### Dimensiones del Tablero
- 6x5, 7x6, 8x5, etc.
- Layouts regulares e irregulares

### Mecánicas
- Giant Bears, Soda, Timed modes
- Spawners y cámaras
- Tipos de gravedad

### Bloqueadores
- Hielo, Chocolate, Caramelo pegajoso
- Densidad y distribución
- Complejidad

### Avanzados
- Scroll levels
- Múltiples áreas de juego
- Portales y tubos

## 📝 Notas

- El sistema es completamente autónomo y reanudable
- Cada pasada es independiente y puede ejecutarse por separado
- Los niveles ya analizados no se reprocesanon
- Compatible con archivos JSON de Candy Crush Soda Saga LIVE
- Sin dependencias externas (usa SQLite nativo)

## 🚀 Próximas Mejoras

- [ ] Exportación de resultados (CSV, JSON)
- [ ] Dashboard web con visualización
- [ ] Machine learning para clustering automático
- [ ] Recomendaciones de dificultad
- [ ] Análisis predictivo

---

**Sistema creado para análisis avanzado de niveles de Candy Crush Soda Saga**
