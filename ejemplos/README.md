# Ejemplos de Uso

Este directorio contiene ejemplos de cómo usar las funciones de AutoForense.

## ejemplo_uso.py

Ejemplo básico que muestra cómo usar la clase `PowerShellHelper` para ejecutar funciones de PowerShell desde Python.

### Uso:

```bash
cd src
python ../ejemplos/ejemplo_uso.py
```

O desde el directorio raíz:

```bash
python -m src.powershell_helper
```

## Ejemplo de código básico:

```python
from powershell_helper import PowerShellHelper

# Inicializar el helper
ps_helper = PowerShellHelper()

# Ejecutar una función específica
result = ps_helper.get_suspicious_events(
    max_events=100,
    dont_save_report=True
)

if result['success']:
    print(result['output'])
else:
    print(f"Error: {result['error']}")
```

## Funciones disponibles:

- `get_suspicious_events()` - Extrae eventos sospechosos del Visor de eventos
- `get_internet_processes()` - Correlaciona procesos con conexiones de red
- `get_unsigned_processes()` - Detecta procesos sin firma digital
- `get_suspicious_internet_processes()` - Investiga IPs sospechosas
- `get_full_forensic_analysis()` - Análisis forense completo
