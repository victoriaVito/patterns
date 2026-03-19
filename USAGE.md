# Guía de Uso - Sistema de Detección de Patrones

## �� Objetivo

Este sistema analiza JSONs de niveles de Candy Crush Soda Saga, descubriendo patrones de forma progresiva mediante 4 pasadas de análisis cada vez más detalladas.

## 📋 Paso a Paso

### Paso 1: Preparación

```bash
cd idea
pip install -r requirements.txt
```

### Paso 2: Usa la CLI (Opción Recomendada)

```bash
python3 cli.py
```

**Flujo típico:**
1. Opción **1**: Carga niveles (10 en 10 para evitar problemas)
2. Opción **2**: Ejecuta análisis por pasada
3. Opción **3**: Ver progreso en barras visuales
4. Opción **4**: Ejecuta todas las pasadas automáticamente

### Paso 3 (Alternativo): Usa el API

```bash
# Terminal 1: Inicia servidor
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Realiza requests
curl -X POST http://localhost:8000/analysis/load-levels?limit=50
curl -X POST http://localhost:8000/analysis/run-pass/1
curl http://localhost:8000/analysis/progress
```

## 📊 Interpretación de Resultados

### Progress Bar (CLI)
```
Pass 1: [████████████████████] 100.0% (200/200)
Pass 2: [██████████░░░░░░░░░░] 50.0% (100/200)
Pass 3: [░░░░░░░░░░░░░░░░░░░░] 0.0% (0/200)
Pass 4: [░░░░░░░░░░░░░░░░░░░░] 0.0% (0/200)
```

- `████` = Completado
- `░░░░` = Pendiente
- Porcentaje = % de niveles analizados en esa pasada

### Average Passes
- **0.0**: Nada analizado
- **1.0-2.0**: Primeras pasadas en progreso
- **4.0-5.0**: Sistema completamente analizado

## 🔍 Qué Se Detecta en Cada Pasada

### Pasada 1: Estructura
- Tamaño del tablero (7x7, 6x5, etc.)
- Tipo de modo (Giant Bears, Soda, etc.)
- Número de movimientos
- Estrellas y puntuación

### Pasada 2: Gameplay
- Número de spawners
- Tipos de gravedad
- Caramelos especiales disponibles

### Pasada 3: Bloqueadores
- Tipos: hielo, chocolate, etc.
- Densidad en el tablero
- Complejidad de obstáculos

### Pasada 4: Avanzado
- Cámaras múltiples
- Niveles con scroll
- Portales y mecanismos especiales

## 💡 Consejos

1. **Comienza pequeño**: Carga 10-50 niveles primero para probar
2. **Monitorea progreso**: Usa opción 3 para ver avance
3. **Pausa si es necesario**: El sistema retomará de donde paró
4. **Para grandes cantidades**: Usa CLI, es más estable

## 🐛 Troubleshooting

| Problema | Solución |
|----------|----------|
| API se cierra | Usa CLI en lugar de API para cargas grandes |
| Niveles lentos | Reduce `limit` en load-levels a 20-30 |
| Errores de BD | Borra `candy_patterns.db` y reinicia |

## 📈 Escala

Sistema probado con:
- ✓ 100 niveles
- ✓ 200 niveles
- ✓ Carga incremental
- ✓ Análisis completo (4 pasadas)

---

**¡Listo! El sistema está funcionando correctamente.**
