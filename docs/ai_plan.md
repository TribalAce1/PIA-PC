# Plan de Integración de IA - AutoForense

## Propósito del uso de IA
La IA analiza automáticamente los datos forenses recopilados del sistema Windows, detecta comportamientos sospechosos y genera reportes detallados en PDF con recomendaciones de seguridad.

## Punto de integración en el flujo
Se integra después de la recopilación de datos:

1. **Usuario** selecciona las tareas forenses desde `AutoForense.py`
2. **PowerShell** recopila datos del sistema (`FuncionesForenses.psm1`)
3. **IA** analiza los datos y detecta anomalías (`AIAnalyzer.py`)
4. **PDF** genera el reporte final (`PDFGenerator.py`)

## Modelo de IA utilizado
**API:** Google AI (Generative AI)  
**Modelo:** Gemini 1.5 Flash  
**Razón:** Balance entre velocidad, capacidad de análisis y costo-efectividad

## Ejemplo de prompt del sistema
```
Eres un experto en análisis forense digital y ciberseguridad especializado en sistemas Windows.

Analiza los siguientes datos forenses y genera un reporte estructurado con:
1. Resumen ejecutivo de hallazgos
2. Actividades o procesos sospechosos detectados
3. Nivel de riesgo (Bajo, Medio, Alto, Crítico)
4. Posibles causas o anomalías
5. Recomendaciones de seguridad priorizadas

Datos recopilados:
<datos_forenses_en_formato_csv>
```

## Formato de respuesta esperado
La IA devuelve un JSON estructurado con:
- Resumen ejecutivo
- Hallazgos principales con nivel de riesgo
- Análisis detallado por categoría (eventos, procesos, red)
- Recomendaciones priorizadas
- Conclusión y próximos pasos

## Modos de análisis disponibles
- **Análisis individual:** Una tarea específica con reporte focalizado
- **Análisis completo:** Todas las tareas con reporte consolidado
- **Modo básico:** Exportación CSV sin análisis de IA

## Seguridad
- API Key en archivo `.env`
- Datos procesados localmente
- Sin almacenamiento en servidores externos
- Reportes PDF guardados en `src/reportes/`
