# AutoForense
Automatización Inteligente de Análisis Forense en Sistemas Windows.

## Descripción general del proyecto:
AutoForense es una herramienta desarrollada en PowerShell que permite automatizar tareas forenses dentro de sistemas Windows. El usuario puede seleccionar distintas funciones, como la extracción de eventos relevantes, la correlación de procesos activos con conexiones de red y la investigación de direcciones IP remotas. Los datos recolectados se envían a una IA (por ejemplo, Google AI) para su análisis automatizado, con el fin de auditar el sistema, detectar comportamientos sospechosos y generar un reporte final detallado.

## Estructura del proyecto
```text
/
│
├── src/
│   ├── AutoForense.py          # Código principal del proyecto (interfaz de usuario)
│   ├── FuncionesForenses.psm1  # Funciones de investigación forense (módulo PowerShell)
│   ├── Prompt.txt              # Prompt del sistema
│   └── PowershellHelper.py     # Helper para ejecutar funciones PowerShell desde Python
│
├── docs/
│   ├── diagrama.png             # Diagrama del flujo de trabajo del programa
│   └── README.md                # Archivo de documentación 
│
├── ejemplos/                    # Ejemplos de uso y resultados de salida
│   └── README.md                # Documentación de ejemplos
│
├── .gitignore                   # Archivos ignorados por git
├── requirements.txt             # Dependencias del proyecto (Python)
└── README.md                    # Archivo con la información principal del programa 
```

## Propositos
- Autoforense.py Captura las tareas a revisar que seleccione el usuario.
- FuncionesForenses.psm1 envia los datos recopilados a la Inteligencia Artificial (IA).
- La IA ejecuta codigos a placer hasta auditar lo requerido y despues de eso genera un reporte y lo devuelve en formato PDF.


### FuncionesForenses.psm1
- **FuncionesForenses.psm1**: Módulo de powershell que contiene funciones para análisis forense
  - `Get-SuspiciousEvents`: Extrae eventos sospechosos del Visor de eventos de Windows
  - `Get-InternetProcesses`: Correlaciona procesos activos con conexiones de red
  - `Get-UnsignedProcesses`: Detecta procesos sin firma digital válida

## Diagrama del flujo de trabajo del programa
![Diagrama](docs/diagrama.png)
 
## Declaracion legal

AutoForense se proporciona “tal cual”, sin garantías de ningún tipo. Su uso es bajo su exclusiva responsabilidad. Ni el autor ni los distribuidores serán responsables por daños directos, indirectos, incidentales, consecuentes o de cualquier otra índole derivados del uso o mal uso del software. AutoForense no sustituye asesoría profesional forense ni legal; el usuario debe verificar el cumplimiento de todas las leyes y regulaciones aplicables. Al instalar o usar AutoForense, usted acepta mantener indemnes a sus desarrolladores y colaboradores frente a cualquier reclamación o responsabilidad.

Este proyecto se desarrollará exclusivamente con datos sintéticos o simulados. No se utilizarán datos reales, credenciales privadas ni información sensible. Todos los experimentos se ejecutarán en entornos controlados. El equipo se compromete a documentar cualquier riesgo ético y aplicar medidas de mitigación adecuadas.
