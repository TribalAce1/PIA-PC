# AutoForense - Documentación Técnica

> **Automatización Inteligente de Análisis Forense en Sistemas Windows**

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura](#arquitectura)
3. [Componentes](#componentes)
4. [Instalación](#instalación)
5. [Guía de Uso](#guía-de-uso)
6. [API de Módulos](#api-de-módulos)
7. [Resolución de Problemas](#resolución-de-problemas)

---

## Descripción General

AutoForense es una herramienta de análisis forense digital para Windows que combina PowerShell para recopilación de datos con IA (Google Gemini) para análisis automatizado.

### Características

- ✅ **Recopilación Forense**: Eventos del sistema, procesos activos y conexiones de red
- 🤖 **Análisis con IA**: Google Gemini 2.5 Pro para detectar anomalías
- 📄 **Reportes PDF**: Generación automática de reportes profesionales
- 🔍 **Detección de Amenazas**: Procesos sin firma, eventos sospechosos, conexiones anómalas
- 🛡️ **No Destructivo**: Solo operaciones de lectura

---

## Arquitectura

```
AutoForense.py (Interfaz)
    │
    ├── PowershellHelper.py ──► FuncionesForenses.psm1 (PowerShell)
    │
    ├── AIAnalyzer.py ──► Google AI API (Gemini)
    │
    └── PDFGenerator.py ──► Reportes PDF
```

---

## Componentes

### 1. AutoForense.py
Programa principal con menú interactivo que coordina todos los componentes.

### 2. FuncionesForenses.psm1
Módulo PowerShell con funciones de recopilación forense:

- **Get-SuspiciousEvents**: Extrae eventos sospechosos del Visor de Eventos
- **Get-InternetProcesses**: Correlaciona procesos con conexiones de red
- **Get-UnsignedProcesses**: Detecta procesos sin firma digital válida

### 3. PowershellHelper.py
Puente entre Python y PowerShell. Ejecuta funciones forenses y captura resultados.

### 4. AIAnalyzer.py
Integración con Google Gemini para análisis inteligente de datos forenses.

### 5. PDFGenerator.py
Genera reportes profesionales en PDF con hallazgos, recomendaciones y estadísticas.

### 6. Prompt.txt
Define el comportamiento de la IA: rol, formato de salida y restricciones de seguridad.

---

## Instalación

### Requisitos
- **Sistema**: Windows 10/11
- **Python**: 3.8 o superior
- **PowerShell**: 5.1+ (incluido en Windows)

### Pasos

1. **Clonar repositorio**
```bash
git clone https://github.com/tu-usuario/PIA-PC.git
cd PIA-PC
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar API Key de Google AI**

Obtener key en: https://makersuite.google.com/app/apikey

Crear archivo `.env`:
```env
GOOGLE_API_KEY=tu_api_key_aqui
```

4. **Ejecutar**
```bash
.\ejecutar_autoforense.bat
```

O manualmente:
```bash
cd src
python AutoForense.py
```

---

## Guía de Uso

### Modo Básico (sin IA)

**Opción 1-3**: Funcionan sin API Key

```
1. Get-SuspiciousEvents     → Eventos sospechosos del sistema
2. Get-InternetProcesses    → Procesos con conexiones activas
3. Get-UnsignedProcesses    → Procesos sin firma digital
```

**Salida**: Reporte en consola + archivo CSV

### Modo con IA

**Opción 4**: Análisis de una tarea específica
- Ejecuta la tarea seleccionada
- Analiza con IA
- Genera reporte PDF

**Opción 5**: Análisis Forense Completo
- Ejecuta todas las tareas (1-3)
- Análisis consolidado con correlaciones
- Reporte PDF completo

**Tiempo estimado**: 1-3 minutos

---

## API de Módulos

### PowershellHelper

```python
from PowershellHelper import PowerShellHelper

ps = PowerShellHelper()

# Analizar eventos
result = ps.get_suspicious_events(max_events=2000, dont_save_report=False)

# Analizar procesos con Internet
result = ps.get_internet_processes(dont_save_report=False)

# Detectar procesos sin firma
result = ps.get_unsigned_processes()

# Estructura de retorno
{
    'success': bool,
    'output': str,
    'error': str,
    'returncode': int
}
```

### AIAnalyzer

```python
from AIAnalyzer import AIAnalyzer

ai = AIAnalyzer()  # Usa GOOGLE_API_KEY del .env

# Analizar una tarea
analysis = ai.analyze_forensic_data(
    task_name="Get-SuspiciousEvents",
    data=datos_recopilados
)

# Analizar múltiples tareas
tasks_data = {
    'Get-SuspiciousEvents': datos1,
    'Get-InternetProcesses': datos2
}
consolidated = ai.analyze_multiple_tasks(tasks_data)

# Estructura de retorno
{
    'success': bool,
    'summary_short': str,
    'analysis': dict,     # JSON estructurado
    'full_text': str,
    'error': str or None
}
```

### PDFGenerator

```python
from PDFGenerator import PDFGenerator

pdf = PDFGenerator(output_dir="reportes")

# Generar reporte individual
pdf_path = pdf.generate_forensic_report(
    analysis_data=analysis,
    task_name="Get-SuspiciousEvents"
)

# Generar reporte consolidado
pdf_path = pdf.generate_multiple_tasks_report(
    tasks_analyses=individual_analyses,
    consolidated_analysis=consolidated_analysis
)
```

---

## Resolución de Problemas

### Error: "No se encuentra el módulo PowerShell"
**Solución**: Verificar que `src/FuncionesForenses.psm1` existe

### Error: "GOOGLE_API_KEY no configurada"
**Solución**: 
1. Crear archivo `.env` en la raíz
2. Agregar: `GOOGLE_API_KEY=tu_api_key`
3. O usar opciones 1-3 que no requieren IA

### Error: "Error al ejecutar PowerShell"
**Solución**: Ejecutar PowerShell como Administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
```

### Error: "Dependencias faltantes"
**Solución**:
```bash
pip install -r requirements.txt
```

### Error: "Permisos insuficientes"
**Solución**: Ejecutar como Administrador (click derecho → "Ejecutar como administrador")

### Error: "Timeout Google AI"
**Solución**:
- Verificar conexión a Internet
- Reducir `max_events` para enviar menos datos
- Reintentar después de unos minutos

---

## Ejemplos Rápidos

### Análisis Simple con IA

```python
from PowershellHelper import PowerShellHelper
from AIAnalyzer import AIAnalyzer
from PDFGenerator import PDFGenerator

# Inicializar
ps = PowerShellHelper()
ai = AIAnalyzer()
pdf = PDFGenerator()

# Recopilar y analizar
result = ps.get_suspicious_events(max_events=1000, dont_save_report=True)
analysis = ai.analyze_forensic_data("Get-SuspiciousEvents", result['output'])

# Generar reporte
if analysis['success']:
    pdf_path = pdf.generate_forensic_report(analysis, "Get-SuspiciousEvents")
    print(f"Reporte: {pdf_path}")
```

### Análisis Completo Automatizado

```python
# Ejecutar todas las tareas
tasks_data = {
    'Get-SuspiciousEvents': ps.get_suspicious_events(max_events=2000, dont_save_report=True)['output'],
    'Get-InternetProcesses': ps.get_internet_processes(dont_save_report=True)['output'],
    'Get-UnsignedProcesses': ps.get_unsigned_processes()['output']
}

# Analizar consolidado
analysis = ai.analyze_multiple_tasks(tasks_data)

# Generar reporte
if analysis['success']:
    pdf_path = pdf.generate_multiple_tasks_report({}, analysis)
    print(f"Reporte consolidado: {pdf_path}")
```

---

## Estructura de Archivos

```
PIA-PC/
├── src/
│   ├── AutoForense.py              # Programa principal
│   ├── PowershellHelper.py         # Interfaz Python-PowerShell
│   ├── AIAnalyzer.py               # Integración con IA
│   ├── PDFGenerator.py             # Generador de reportes
│   ├── FuncionesForenses.psm1      # Funciones PowerShell
│   └── Prompt.txt                  # Prompt para IA
├── docs/
│   ├── README.md                   # Documentación técnica
│   ├── ai_plan.md                  # Plan de integración IA
│   └── diagrama.png                # Diagrama de flujo
├── ejemplos/                       # Ejemplos de salida
├── reportes/                       # Reportes PDF generados
├── ejecutar_autoforense.bat        # Script de inicio
├── requirements.txt                # Dependencias Python
├── .env                            # Variables de entorno (crear)
└── README.md                       # README principal
```

---

## Seguridad y Responsabilidad

### Principios
- **No Destructivo**: Solo operaciones de lectura
- **Autorización**: Obtener permiso antes de analizar sistemas
- **Privacidad**: No compartir reportes con información sensible
- **Verificación**: Los hallazgos deben ser validados por un profesional

### Limitaciones Legales
AutoForense se proporciona "tal cual", sin garantías. El usuario es responsable del uso apropiado y del cumplimiento de leyes aplicables (GDPR, CCPA, etc.).

---

## Recursos Adicionales

- **Google AI Studio**: https://makersuite.google.com/
- **Gemini API Docs**: https://ai.google.dev/docs
- **ReportLab Docs**: https://www.reportlab.com/docs/
- **PowerShell Docs**: https://docs.microsoft.com/powershell/

---

## Contribuir

1. Fork el repositorio
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request


**AutoForense v1.0** - Documentación actualizada: Noviembre 2025
