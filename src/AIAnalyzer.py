"""
Módulo para análisis forense usando Google AI (Gemini)
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import google.generativeai as genai

# Configurar logging
def setup_logging():
    """Configura el sistema de logging para errores y eventos"""
    log_dir = os.path.join(os.path.dirname(__file__), 'reportes')
    os.makedirs(log_dir, exist_ok=True)
    
    log_filename = os.path.join(
        log_dir, 
        f'aianalyzer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    
    # Configurar formato detallado
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # También mostrar en consola
        ]
    )
    
    return logging.getLogger(__name__)

# Inicializar logger global
logger = setup_logging()


class AIAnalyzer:
    """Clase para analizar datos forenses usando Google AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el analizador de IA
        
        Args:
            api_key: API key de Google AI. Si no se proporciona, se busca en variable de entorno GOOGLE_API_KEY
        """
        logger.info("Inicializando AIAnalyzer...")
        
        try:
            if api_key is None:
                api_key = os.getenv('GOOGLE_API_KEY')
            
            if not api_key:
                logger.error("GOOGLE_API_KEY no encontrada en variables de entorno")
                raise ValueError(
                    "Se requiere GOOGLE_API_KEY. Configúrala como variable de entorno o pásala como parámetro."
                )
            
            # Configurar Google AI
            genai.configure(api_key=api_key)
            logger.info("Google AI configurado correctamente")
            
            # Usar el modelo Gemini 2.5 Pro
            self.model = genai.GenerativeModel('gemini-2.5-pro')
            logger.info("Modelo Gemini 2.5 Pro inicializado")
            
            # Cargar el prompt del sistema
            self.system_prompt = self._load_system_prompt()
            logger.info("AIAnalyzer inicializado exitosamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar AIAnalyzer: {str(e)}", exc_info=True)
            raise
    
    def _load_system_prompt(self) -> str:
        """Carga el prompt del sistema desde Prompt.txt"""
        prompt_path = os.path.join(
            os.path.dirname(__file__),
            "Prompt.txt"
        )
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt = f.read()
                logger.info(f"Prompt del sistema cargado desde {prompt_path}")
                return prompt
        except FileNotFoundError:
            logger.warning(f"Archivo Prompt.txt no encontrado en {prompt_path}. Usando prompt básico.")
            # Prompt básico si no se encuentra el archivo
            return """Eres un asistente forense orientado a sistemas Windows. 
            Analiza los datos proporcionados y genera un resumen claro de hallazgos sospechosos."""
        except Exception as e:
            logger.error(f"Error al cargar Prompt.txt: {str(e)}", exc_info=True)
            return """Eres un asistente forense orientado a sistemas Windows. 
            Analiza los datos proporcionados y genera un resumen claro de hallazgos sospechosos."""
    
    def analyze_forensic_data(
        self,
        task_name: str,
        data: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analiza datos forenses usando IA
        
        Args:
            task_name: Nombre de la tarea ejecutada (ej: "Get-SuspiciousEvents")
            data: Datos recopilados en formato texto
            additional_context: Contexto adicional opcional
            
        Returns:
            Dict con el análisis estructurado
        """
        logger.info(f"Iniciando análisis forense para tarea: {task_name}")
        logger.debug(f"Tamaño de datos a analizar: {len(data)} caracteres")
        
        try:
            # Construir el prompt para la IA
            prompt = self._build_analysis_prompt(task_name, data, additional_context)
            logger.debug(f"Prompt construido, tamaño: {len(prompt)} caracteres")
            
            # Generar respuesta
            print("  Enviando datos a Google AI (Gemini)...")
            print("  Esto puede tardar 10-30 segundos...")
            logger.info("Enviando solicitud a Google AI (Gemini)...")
            
            response = self.model.generate_content(prompt)
            
            print("  ✓ Respuesta recibida de la IA")
            logger.info("Respuesta recibida exitosamente de Google AI")
            
            # Intentar parsear la respuesta como JSON
            analysis_text = response.text
            logger.debug(f"Longitud de respuesta: {len(analysis_text)} caracteres")
            
            # Buscar el JSON en la respuesta
            json_start = analysis_text.find('{')
            json_end = analysis_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = analysis_text[json_start:json_end]
                try:
                    analysis_json = json.loads(json_str)
                    logger.info("JSON parseado correctamente de la respuesta de IA")
                except json.JSONDecodeError as e:
                    logger.warning(f"Error al parsear JSON de la respuesta: {str(e)}")
                    # Si no se puede parsear, crear estructura básica
                    analysis_json = {
                        "summary": "Análisis completado",
                        "findings": [],
                        "recommendations": []
                    }
            else:
                logger.warning("No se encontró JSON en la respuesta de la IA")
                analysis_json = {
                    "summary": "Análisis completado",
                    "findings": [],
                    "recommendations": []
                }
            
            # Extraer resumen corto (texto antes del JSON)
            if json_start > 0:
                summary_short = analysis_text[:json_start].strip()
            else:
                summary_short = analysis_text[:200].strip() + "..."
            
            logger.info(f"Análisis completado exitosamente para tarea: {task_name}")
            
            return {
                'success': True,
                'summary_short': summary_short,
                'analysis': analysis_json,
                'full_text': analysis_text,
                'error': None
            }
            
        except Exception as e:
            error_msg = f"Error en análisis de IA para {task_name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            print(f"  ✗ Error en análisis de IA: {str(e)}")
            return {
                'success': False,
                'summary_short': '',
                'analysis': {},
                'full_text': '',
                'error': f"Error al analizar con IA: {str(e)}"
            }
    
    def _build_analysis_prompt(
        self,
        task_name: str,
        data: str,
        additional_context: Optional[str] = None
    ) -> str:
        """Construye el prompt para el análisis"""
        
        prompt = f"""{self.system_prompt}

---

TAREA EJECUTADA: {task_name}

DATOS RECOPILADOS:
{data[:10000]}  

{"CONTEXTO ADICIONAL: " + additional_context if additional_context else ""}

---

INSTRUCCIONES:
1. Analiza los datos forenses proporcionados
2. Identifica hallazgos sospechosos o relevantes
3. Evalúa el nivel de riesgo de cada hallazgo
4. Proporciona recomendaciones específicas

FORMATO DE SALIDA REQUERIDO:

Primero, proporciona un resumen corto (3-5 líneas) en español.

Luego, proporciona un análisis estructurado en JSON con el siguiente formato:
{{
    "summary": "Resumen general del análisis",
    "findings": [
        {{
            "id": "F1",
            "title": "Título del hallazgo",
            "description": "Descripción detallada",
            "confidence": "high/medium/low",
            "risk_level": "high/medium/low",
            "evidence": "Evidencia específica de los datos"
        }}
    ],
    "recommendations": [
        "Recomendación 1",
        "Recomendación 2"
    ],
    "statistics": {{
        "total_items_analyzed": 0,
        "suspicious_items": 0,
        "clean_items": 0
    }}
}}
"""
        return prompt
    
    def analyze_multiple_tasks(
        self,
        tasks_data: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Analiza múltiples tareas forenses juntas
        
        Args:
            tasks_data: Dict con nombre de tarea como clave y datos como valor
            
        Returns:
            Dict con análisis consolidado
        """
        logger.info(f"Iniciando análisis consolidado de {len(tasks_data)} tareas")
        logger.info(f"Tareas a analizar: {', '.join(tasks_data.keys())}")
        
        try:
            # Combinar todos los datos
            combined_data = ""
            for task_name, data in tasks_data.items():
                combined_data += f"\n\n=== {task_name} ===\n{data[:5000]}\n"
                logger.debug(f"Agregando datos de {task_name}: {len(data)} caracteres")
            
            logger.debug(f"Datos combinados totales: {len(combined_data)} caracteres")
            
            # Construir prompt combinado
            prompt = f"""{self.system_prompt}

---

ANÁLISIS FORENSE MÚLTIPLE

Se han ejecutado las siguientes tareas forenses:
{', '.join(tasks_data.keys())}

DATOS COMBINADOS:
{combined_data[:15000]}

---

INSTRUCCIONES:
1. Analiza todos los datos forenses de forma consolidada
2. Busca correlaciones entre diferentes fuentes de datos
3. Identifica patrones sospechosos que emergen al combinar información
4. Prioriza hallazgos por nivel de riesgo
5. Proporciona un análisis integral del estado del sistema

FORMATO DE SALIDA: Igual que el análisis individual (resumen corto + JSON estructurado)
"""
            
            # Generar respuesta
            print("  Enviando datos consolidados a Google AI...")
            print("  Esto puede tardar 30-60 segundos...")
            logger.info("Enviando análisis consolidado a Google AI...")
            
            response = self.model.generate_content(prompt)
            
            print("  ✓ Análisis consolidado recibido")
            logger.info("Análisis consolidado recibido exitosamente de Google AI")
            
            analysis_text = response.text
            logger.debug(f"Longitud de respuesta consolidada: {len(analysis_text)} caracteres")
            
            # Parsear respuesta
            json_start = analysis_text.find('{')
            json_end = analysis_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = analysis_text[json_start:json_end]
                try:
                    analysis_json = json.loads(json_str)
                    logger.info("JSON consolidado parseado correctamente")
                except json.JSONDecodeError as e:
                    logger.warning(f"Error al parsear JSON consolidado: {str(e)}")
                    analysis_json = {
                        "summary": "Análisis múltiple completado",
                        "findings": [],
                        "recommendations": []
                    }
            else:
                logger.warning("No se encontró JSON en la respuesta consolidada")
                analysis_json = {
                    "summary": "Análisis múltiple completado",
                    "findings": [],
                    "recommendations": []
                }
            
            if json_start > 0:
                summary_short = analysis_text[:json_start].strip()
            else:
                summary_short = analysis_text[:200].strip() + "..."
            
            logger.info("Análisis consolidado completado exitosamente")
            
            return {
                'success': True,
                'summary_short': summary_short,
                'analysis': analysis_json,
                'full_text': analysis_text,
                'error': None
            }
            
        except Exception as e:
            error_msg = f"Error en análisis consolidado: {str(e)}"
            logger.error(error_msg, exc_info=True)
            print(f"  ✗ Error en análisis consolidado: {str(e)}")
            return {
                'success': False,
                'summary_short': '',
                'analysis': {},
                'full_text': '',
                'error': f"Error al analizar con IA: {str(e)}"
            }

