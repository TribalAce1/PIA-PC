"""
Módulo helper para ejecutar funciones de PowerShell desde Python
"""
import subprocess
import json
import os
from typing import Optional, Dict, Any, List


class PowerShellHelper:
    """Clase helper para ejecutar funciones PowerShell desde Python"""
    
    def __init__(self, module_path: Optional[str] = None):
        """
        Inicializa el helper de PowerShell
        
        Args:
            module_path: Ruta al módulo FuncionesForenses.psm1
        """
        if module_path is None:
            # Buscar el módulo en el directorio src
            self.module_path = os.path.join(
                os.path.dirname(__file__),
                "FuncionesForenses.psm1"
            )
        else:
            self.module_path = module_path
        
        # Convertir a ruta absoluta para evitar problemas con rutas relativas
        self.module_path = os.path.abspath(self.module_path)
        
        if not os.path.exists(self.module_path):
            raise FileNotFoundError(
                f"No se encontró el módulo PowerShell en: {self.module_path}"
            )
    
    def _execute_powershell(self, command: str) -> Dict[str, Any]:
        """
        Ejecuta un comando de PowerShell y retorna el resultado
        
        Args:
            command: Comando PowerShell a ejecutar
            
        Returns:
            Dict con 'success', 'output' y 'error'
        """
        try:
            # Normalizar la ruta del módulo para PowerShell (escapar comillas dobles)
            # Usar comillas dobles para manejar mejor rutas con espacios
            module_path_normalized = self.module_path.replace('"', '`"')
            
            # Importar el módulo y ejecutar el comando
            full_command = f"""
            Import-Module "{module_path_normalized}" -Force
            {command}
            """
            
            # Ejecutar PowerShell con ExecutionPolicy Bypass para permitir scripts no firmados
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", full_command],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'returncode': -1
            }
    
    def get_suspicious_events(
        self,
        max_events: int = 2000,
        output_path: Optional[str] = None,
        dont_save_report: bool = False
    ) -> Dict[str, Any]:
        """
        Ejecuta Get-SuspiciousEvents para extraer eventos sospechosos
        
        Args:
            max_events: Número máximo de eventos a analizar
            output_path: Ruta donde guardar el CSV (opcional)
            dont_save_report: Si True, no guarda el reporte
            
        Returns:
            Dict con el resultado de la ejecución
        """
        params = []
        params.append(f"-MaxEvents {max_events}")
        
        if output_path:
            params.append(f"-OutputPath '{output_path}'")
        
        if dont_save_report:
            params.append("-DontSaveReport")
        
        command = f"Get-SuspiciousEvents {' '.join(params)}"
        return self._execute_powershell(command)
    
    def get_internet_processes(
        self,
        dont_save_report: bool = False
    ) -> Dict[str, Any]:
        """
        Ejecuta Get-InternetProcesses para correlacionar procesos con conexiones de red
        
        Args:
            dont_save_report: Si True, no guarda el reporte
            
        Returns:
            Dict con el resultado de la ejecución
        """
        params = []
        if dont_save_report:
            params.append("-DontSaveReport")
        
        command = f"Get-InternetProcesses {' '.join(params)}"
        return self._execute_powershell(command)
    
    def get_unsigned_processes(self) -> Dict[str, Any]:
        """
        Ejecuta Get-UnsignedProcesses para detectar procesos sin firma digital
        
        Returns:
            Dict con el resultado de la ejecución
        """
        command = "Get-UnsignedProcesses"
        return self._execute_powershell(command)
    
    def get_suspicious_internet_processes(
        self,
        threshold: int = 10,
        dont_save_report: bool = False
    ) -> Dict[str, Any]:
        """
        Ejecuta Get-SuspiciousInternetProcesses para investigar IPs sospechosas
        
        Args:
            threshold: Umbral de confianza de abuso (0-100)
            dont_save_report: Si True, no guarda el reporte
            
        Returns:
            Dict con el resultado de la ejecución
        """
        params = [f"-Threshold {threshold}"]
        if dont_save_report:
            params.append("-DontSaveReport")
        
        command = f"Get-SuspiciousInternetProcesses {' '.join(params)}"
        return self._execute_powershell(command)
    
    def get_full_forensic_analysis(
        self,
        output_path: Optional[str] = None,
        dont_save_report: bool = False
    ) -> Dict[str, Any]:
        """
        Ejecuta Get-FullForensicAnalysis para un análisis forense completo
        
        Args:
            output_path: Ruta donde guardar el CSV (opcional)
            dont_save_report: Si True, no guarda el reporte
            
        Returns:
            Dict con el resultado de la ejecución
        """
        params = []
        if output_path:
            params.append(f"-OutputPath '{output_path}'")
        
        if dont_save_report:
            params.append("-DontSaveReport")
        
        command = f"Get-FullForensicAnalysis {' '.join(params)}"
        return self._execute_powershell(command)

