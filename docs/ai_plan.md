# Propósito del uso de IA en el proyecto
La ia ejecutará códigos a placer hasta auditar lo requerido y despues se generara un reporte en formato pdf y lo devolverá.

# Punto del flujo donde se integrará
Se integrará al final del flujo de recopilación de datos, una vez que las tres tareas generen sus salidas en un formato estructurado.
El flujo seria de la siguiente manera:
- **1)** El usuario seleccionará las tareas que desee desde el script principal.
- **2)** Los resultados se exportarán en archivos y enviados a la IA para raelizar el análisis.
- **3)** La IA procesará, generará un resumen y redactará el reporte final.

# Tipo  de modelo/API a utilizar 
Se utilizara **Google AI API**, lo cual proporciona modelos de lenguaje y análisis basados en aprendizaje automático. 
El sistema se conecta a esta API desde el script AutoForense.py para enviarles los datos recolectados y recibir respuestas estructuradas o reportes generados automáticamente. 

# Ejemplo de prompt inicial 
Analiza los siguientes datos forenses y genera un reporte con las siguientes secciones:
- **1)** Actividades o archivos sospechosos detectados
- **2)** Posibles causas o anomalías
- **3)** Recomendaciones de seguridad

Datos recopilados:
<contenido_recopilado_por_FuncionesForenses.psm1>
