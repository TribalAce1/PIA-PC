**TAREA #1:**
**Título y propósito (2–3 frases):**

Extracción de eventos relevantes.
Su propósito es automatizar la recopilación y filtrado de eventos del Visor de Eventos de Windows (Application, System y Security). Esta tarea busca detectar patrones o indicios de actividad anómala o maliciosa en los registros del sistema.

**Función, rol o área de la ciberseguridad relacionada:**

DFIR (Digital Forensics and Incident Response) / SOC (Security Operations Center)

**Entradas esperadas (formato y ejemplos):**

Parámetros:

-MaxEvents: número máximo de eventos a analizar (ej. 500).

-OutPath: ruta de salida del reporte (ej. C:\AutoForense\eventos.csv).

**Salidas esperadas (formato y ejemplos):**

Archivo .csv o .txt con eventos filtrados, incluyendo campos como:

Fecha/Hora

Origen

ID del evento

Descripción

Nivel (Error, Warning, Critical)

**Descripción del procedimiento (narración funcional):**

El script invoca la función Get-SuspiciousEvents, que analiza los registros del sistema, aplicación y seguridad. Aplica filtros predefinidos para identificar errores, advertencias y eventos críticos. Luego, guarda los resultados en un archivo en formato CSV. Este archivo puede ser posteriormente procesado por la IA para evaluar tendencias o anomalías.

**Complejidad técnica (dimensiones que cubre):**

Lectura y análisis de registros del sistema Windows.

Filtrado de eventos por tipo y severidad.

Exportación de resultados a formato estructurado.

**Controles éticos o consideraciones éticas que se tomarán en cuenta:**

No se alteran registros del sistema.

Se garantiza la integridad de la evidencia recolectada.

Se utiliza únicamente en entornos autorizados para fines académicos o de auditoría.

**Dependencias (librerías, comandos, entorno):**

PowerShell 5.1 o superior.

Cmdlets: Get-WinEvent, Export-Csv.

Permisos de administrador.

**TAREA #2:**
**Título y propósito (2–3 frases):**

Correlación de procesos activos con conexiones de red.
El objetivo es identificar qué procesos del sistema mantienen conexiones activas a la red y correlacionar su actividad con posibles comportamientos anómalos.

**Función, rol o área de la ciberseguridad relacionada:**

DFIR / Threat Hunting / SOC

**Entradas esperadas (formato y ejemplos):**

Comandos del sistema como:

Get-Process

Get-NetTCPConnection

No requiere parámetros externos.

**Salidas esperadas (formato y ejemplos):**

Tabla o archivo con los campos:

Nombre del proceso

PID (Process ID)

Dirección local y remota

Puerto utilizado

Estado de la conexión

**Descripción del procedimiento (narración funcional):**

El módulo obtiene la lista de procesos activos y la correlaciona con las conexiones TCP abiertas mediante PowerShell. Se identifica qué procesos están comunicándose externamente, lo que ayuda a detectar software sospechoso o malware con conexiones persistentes.

**Complejidad técnica (dimensiones que cubre):**

Análisis de procesos y conexiones en tiempo real.

Correlación de información de red y sistema.

Exportación a CSV o pantalla.

**Controles éticos o consideraciones éticas que se tomarán en cuenta:**

Solo se ejecuta con consentimiento del usuario o en sistemas propios.

No se manipulan procesos ni conexiones, únicamente se observan.

**Dependencias (librerías, comandos, entorno):**

PowerShell (cmdlets Get-Process, Get-NetTCPConnection).

Permisos administrativos.

**TAREA #3:**
**Título y propósito (2–3 frases):**

Investigación de direcciones IP remotas.
Permite comprobar la reputación o procedencia de direcciones IP remotas detectadas en las conexiones del sistema, comparándolas con listas negras o APIs públicas.

**Función, rol o área de la ciberseguridad relacionada:**

Threat Intelligence / DFIR / SOC

**Entradas esperadas (formato y ejemplos):**

Lista de direcciones IP detectadas (por ejemplo, de la Tarea #2).

Ejemplo: 8.8.8.8, 45.33.32.156.

**Salidas esperadas (formato y ejemplos):**

Reporte o tabla con:

IP analizada

País / ASN

Reputación (maliciosa / confiable)

Fuente de validación

**Descripción del procedimiento (narración funcional):**

El script envía las direcciones IP obtenidas a un motor de consulta (por ejemplo, Google AI o una API externa de reputación). Recibe y clasifica las respuestas según su confiabilidad, marcando las direcciones sospechosas o asociadas a amenazas conocidas.

**Complejidad técnica (dimensiones que cubre):**

Integración con fuentes externas o IA.

Análisis y clasificación de reputación IP.

Correlación con resultados de procesos de red.

**Controles éticos o consideraciones éticas que se tomarán en cuenta:**

No se realiza exploración activa ni intrusión.

Solo se analizan direcciones IP obtenidas de manera pasiva.

Uso limitado a propósitos educativos o de auditoría.

**Dependencias (librerías, comandos, entorno):**

PowerShell + API externa (por ejemplo, Google AI, VirusTotal o AbuseIPDB).

Acceso a internet.
(![Diagrama]docs/diagrama.png)

