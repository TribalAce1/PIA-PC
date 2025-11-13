# Ejemplos de Uso de AutoForense

Este directorio contiene ejemplos de salida de las funciones forenses de AutoForense.

---

## Archivos de Ejemplo

### 1. eventos_sospechosos_07_11_2025.csv
**Tarea**: Get-SuspiciousEvents  
**Contenido**: Eventos del Visor de Eventos de Windows que pueden indicar actividad sospechosa.

**Campos**:
- `TimeCreated`: Fecha y hora del evento
- `Id`: ID del evento
- `LevelDisplayName`: Nivel (Error, Warning, Information)
- `ProviderName`: Fuente del evento
- `Message`: Descripción del evento

**Uso**:
```bash
python AutoForense.py
# Seleccionar opción 1
```

---

### 2. procesos_sin_firma_07_11_2025.csv
**Tarea**: Get-UnsignedProcesses  
**Contenido**: Procesos en ejecución sin firma digital válida.

**Campos**:
- `ProcessName`: Nombre del proceso
- `Id`: PID (Process ID)
- `Path`: Ruta del ejecutable
- `SignatureStatus`: Estado de la firma
- `SignerCertificate`: Certificado del firmante

**Uso**:
```bash
python AutoForense.py
# Seleccionar opción 3
```

---

### 3. reporte_procesos_internet_07_11_2025.csv
**Tarea**: Get-InternetProcesses  
**Contenido**: Procesos activos con conexiones de red establecidas.

**Campos**:
- `ProcessId`: PID del proceso
- `ProcessName`: Nombre del proceso
- `ExecutablePath`: Ruta del ejecutable
- `RemoteAddress`: IP remota conectada
- `RemotePort`: Puerto remoto
- `State`: Estado de la conexión (Established, TimeWait, etc.)

**Uso**:
```bash
python AutoForense.py
# Seleccionar opción 2
```

---

## Ejemplos de Código

### Ejemplo 1: Uso Básico

```python
from src.PowershellHelper import PowerShellHelper

# Inicializar
ps = PowerShellHelper()

# Ejecutar análisis de eventos
result = ps.get_suspicious_events(max_events=100, dont_save_report=True)

if result['success']:
    print(result['output'])
else:
    print(f"Error: {result['error']}")
```

### Ejemplo 2: Análisis con IA

```python
from src.PowershellHelper import PowerShellHelper
from src.AIAnalyzer import AIAnalyzer
from src.PDFGenerator import PDFGenerator

ps = PowerShellHelper()
ai = AIAnalyzer()
pdf = PDFGenerator()

# Recopilar datos
result = ps.get_unsigned_processes()

# Analizar con IA
if result['success']:
    analysis = ai.analyze_forensic_data(
        task_name="Get-UnsignedProcesses",
        data=result['output']
    )
    
    # Generar PDF
    if analysis['success']:
        pdf_path = pdf.generate_forensic_report(analysis, "Get-UnsignedProcesses")
        print(f"Reporte: {pdf_path}")
```

### Ejemplo 3: Análisis Completo

```python
# Ejecutar todas las tareas
tasks = {
    'eventos': ps.get_suspicious_events(max_events=2000, dont_save_report=True)['output'],
    'procesos': ps.get_internet_processes(dont_save_report=True)['output'],
    'sin_firma': ps.get_unsigned_processes()['output']
}

# Analizar consolidado
analysis = ai.analyze_multiple_tasks(tasks)

# Generar reporte
if analysis['success']:
    pdf_path = pdf.generate_multiple_tasks_report({}, analysis)
    print(f"Reporte consolidado: {pdf_path}")
```

---

## Interpretación de Resultados

### Eventos Sospechosos
**IDs críticos a revisar**:
- `4624`: Inicio de sesión exitoso
- `4625`: Inicio de sesión fallido
- `4720`: Cuenta de usuario creada
- `7045`: Nuevo servicio instalado
- `1102`: Log de auditoría borrado

### Procesos Sin Firma
**Indicadores de riesgo**:
- Procesos en `%TEMP%` o `%APPDATA%`
- Nombres aleatorios (ej: `abc123.exe`)
- Consumo alto de CPU/memoria
- Conexiones a IPs sospechosas

### Procesos con Internet
**Patrones anómalos**:
- Procesos del sistema conectados a IPs públicas
- Puertos no estándar
- Múltiples conexiones del mismo proceso
- IPs de países inusuales

---

## Notas

- Los archivos CSV usan codificación UTF-8
- Las fechas están en formato local del sistema
- Los ejemplos son datos sintéticos para demostración
- **No ejecutar en sistemas de producción sin autorización**

---

Para más información, consulta la [documentación técnica](../docs/README.md).
