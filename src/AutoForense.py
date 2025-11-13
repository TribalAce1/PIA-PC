"""
AutoForense - Automatización Inteligente de Análisis Forense en Sistemas Windows
Código principal del proyecto
"""
import sys
import os
import subprocess
from dotenv import load_dotenv
from PowershellHelper import PowerShellHelper
from AIAnalyzer import AIAnalyzer
from PDFGenerator import PDFGenerator

# Cargar variables de entorno
load_dotenv()


def verificar_dependencias():
    """Verifica e intenta instalar dependencias faltantes"""
    dependencias_faltantes = []
    
    # Verificar dependencias
    try:
        import google.generativeai
    except ImportError:
        dependencias_faltantes.append('google-generativeai')
    
    try:
        import reportlab
    except ImportError:
        dependencias_faltantes.append('reportlab')
    
    try:
        import dotenv
    except ImportError:
        dependencias_faltantes.append('python-dotenv')
    
    if dependencias_faltantes:
        print("\n⚠ DEPENDENCIAS FALTANTES:")
        for dep in dependencias_faltantes:
            print(f"  - {dep}")
        
        respuesta = input("\n¿Instalar dependencias ahora? (S/N): ").strip().upper()
        if respuesta == 'S':
            print("\nInstalando dependencias...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
                print("\n✓ Dependencias instaladas correctamente")
                print("  Reinicia el programa para usar las funciones de IA\n")
                return False
            except subprocess.CalledProcessError:
                print("\n✗ Error al instalar dependencias")
                print("  Funciones de IA no estarán disponibles")
                return True
        else:
            print("\n⚠ Continuando sin instalar dependencias")
            print("  Las opciones 1-3 funcionarán, pero NO las opciones 4-5\n")
            return True
    
    return True

def mostrar_bienvenida():
    art = r"""
      .~~~~`\~~\\
     ;       ~~ \\
     |           ;
 ,--------,______|---.
/          \-----`    \ 
`.__________`-_______-'_____                             
   / \  _   _| |_ ___ |  ___|__  _ __ ___ _ __  ___  ___ 
  / _ \| | | | __/ _ \| |_ / _ \| '__/ _ \ '_ \/ __|/ _ \
 / ___ \ |_| | || (_) |  _| (_) | | |  __/ | | \__ \  __/
/_/   \_\__,_|\__\___/|_|  \___/|_|  \___|_| |_|___/\___|
    """
    # Imprime el arte ASCII en verde (ansi)
    print("\033[32m" + art + "\033[0m")

def print_menu():
    print()
    print("Funciones disponibles:")
    print("1. Get-SuspiciousEvents - Extraer eventos sospechosos")
    print("2. Get-InternetProcesses - Procesos con conexiones de red")
    print("3. Get-UnsignedProcesses - Procesos sin firma digital")
    print("4. Análisis Forense con IA - Ejecuta una tarea y analiza con IA")
    print("5. Análisis Forense Completo - Ejecuta todas las tareas y genera reporte PDF")
    print("6. Salir")
    print()

def main():
    """Función principal del programa"""
    # Mostrar arte ASCII de bienvenida
    mostrar_bienvenida()
    
    # Verificar e instalar dependencias
    print("\n[Verificando dependencias...]")
    if not verificar_dependencias():
        return 0
    
    # Inicializar el helper de PowerShell
    try:
        ps_helper = PowerShellHelper()
        print("✓ Módulo PowerShell cargado correctamente")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return 1
    
    # Inicializar IA y generador de PDF (opcional)
    ai_analyzer = None
    pdf_generator = None
    
    try:
        ai_analyzer = AIAnalyzer()
        pdf_generator = PDFGenerator(output_dir="reportes")
        print("✓ Módulo de IA cargado correctamente")
    except ValueError as e:
        print(f"⚠ Advertencia: {e}")
        print("⚠ Las funciones de IA no estarán disponibles")
        print("⚠ Para usar IA, configura GOOGLE_API_KEY en archivo .env")
    except ImportError as e:
        print(f"⚠ Advertencia: No se pudo cargar módulo de IA - {e}")
        print("⚠ Ejecuta: pip install -r requirements.txt")
    
    
    while True:
        try:
            print_menu()
            opcion = input("Seleccione una opción (1-6): ").strip()
            
            if opcion == "1":
                print("\n[Ejecutando Get-SuspiciousEvents...]")
                max_events = input("Max eventos (Enter para 2000): ").strip()
                max_events = int(max_events) if max_events else 2000
                
                result = ps_helper.get_suspicious_events(
                    max_events=max_events,
                    dont_save_report=False
                )
                
                if result['success']:
                    print("\n✓ Ejecución exitosa")
                    print(result['output'])
                else:
                    print("\n✗ Error en la ejecución:")
                    print(result['error'])
            
            elif opcion == "2":
                print("\n[Ejecutando Get-InternetProcesses...]")
                result = ps_helper.get_internet_processes(dont_save_report=False)
                
                if result['success']:
                    print("\n✓ Ejecución exitosa")
                    print(result['output'])
                else:
                    print("\n✗ Error en la ejecución:")
                    print(result['error'])
            
            elif opcion == "3":
                print("\n[Ejecutando Get-UnsignedProcesses...]")
                result = ps_helper.get_unsigned_processes()
                
                if result['success']:
                    print("\n✓ Ejecución exitosa")
                    print(result['output'])
                else:
                    print("\n✗ Error en la ejecución:")
                    print(result['error'])
            
            elif opcion == "4":
                if ai_analyzer is None or pdf_generator is None:
                    print("\n✗ Las funciones de IA no están disponibles.")
                    print("✗ Configura GOOGLE_API_KEY en archivo .env")
                    continue
                
                print("\n[Análisis Forense con IA]")
                print("Seleccione la tarea a analizar:")
                print("1. Get-SuspiciousEvents")
                print("2. Get-InternetProcesses")
                print("3. Get-UnsignedProcesses")
                
                sub_opcion = input("Opción: ").strip()
                
                task_name = ""
                result = None
                
                if sub_opcion == "1":
                    task_name = "Get-SuspiciousEvents"
                    max_events = input("Max eventos (Enter para 2000): ").strip()
                    max_events = int(max_events) if max_events else 2000
                    result = ps_helper.get_suspicious_events(
                        max_events=max_events,
                        dont_save_report=True
                    )
                elif sub_opcion == "2":
                    task_name = "Get-InternetProcesses"
                    result = ps_helper.get_internet_processes(dont_save_report=True)
                elif sub_opcion == "3":
                    task_name = "Get-UnsignedProcesses"
                    result = ps_helper.get_unsigned_processes()
                else:
                    print("\n✗ Opción no válida")
                    continue
                
                if result and result['success']:
                    print(f"\n✓ Datos recopilados de {task_name}")
                    print("\n[Analizando con IA...]")
                    
                    analysis = ai_analyzer.analyze_forensic_data(
                        task_name=task_name,
                        data=result['output']
                    )
                    
                    if analysis['success']:
                        print("\n" + "="*60)
                        print("ANÁLISIS DE LA IA:")
                        print("="*60)
                        print(analysis['full_text'])
                        print("\n" + "="*60)
                        
                        # Generar PDF
                        print("\n[Generando reporte PDF...]")
                        pdf_path = pdf_generator.generate_forensic_report(
                            analysis_data=analysis,
                            task_name=task_name
                        )
                        print(f"✓ Reporte PDF generado: {pdf_path}")
                    else:
                        print(f"\n✗ Error en el análisis de IA: {analysis['error']}")
                else:
                    print(f"\n✗ Error al ejecutar {task_name}")
            
            elif opcion == "5":
                if ai_analyzer is None or pdf_generator is None:
                    print("\n✗ Las funciones de IA no están disponibles.")
                    print("✗ Configura GOOGLE_API_KEY en archivo .env")
                    continue
                
                print("\n[Análisis Forense Completo]")
                print("Se ejecutarán todas las tareas forenses y se generará un reporte consolidado")
                
                confirmar = input("\n¿Continuar? (s/n): ").strip().lower()
                if confirmar != 's':
                    print("Operación cancelada")
                    continue
                
                # Ejecutar todas las tareas
                print("\n[1/3] Extrayendo eventos sospechosos...")
                events_result = ps_helper.get_suspicious_events(
                    max_events=2000,
                    dont_save_report=True
                )
                
                print("[2/3] Analizando procesos con conexiones de red...")
                internet_result = ps_helper.get_internet_processes(dont_save_report=True)
                
                print("[3/3] Detectando procesos sin firma digital...")
                unsigned_result = ps_helper.get_unsigned_processes()
                
                # Recopilar datos
                tasks_data = {}
                if events_result['success']:
                    tasks_data['Get-SuspiciousEvents'] = events_result['output']
                if internet_result['success']:
                    tasks_data['Get-InternetProcesses'] = internet_result['output']
                if unsigned_result['success']:
                    tasks_data['Get-UnsignedProcesses'] = unsigned_result['output']
                
                if not tasks_data:
                    print("\n✗ No se pudieron recopilar datos")
                    continue
                
                # Analizar con IA
                print("\n[Analizando todos los datos con IA...]")
                consolidated_analysis = ai_analyzer.analyze_multiple_tasks(tasks_data)
                
                if consolidated_analysis['success']:
                    print("\n" + "="*60)
                    print("ANÁLISIS CONSOLIDADO:")
                    print("="*60)
                    print(consolidated_analysis['full_text'])
                    print("\n" + "="*60)
                    
                    # Generar reporte PDF consolidado
                    print("\n[Generando reporte PDF consolidado...]")
                    
                    # Usar solo el análisis consolidado (evita múltiples requests a la API)
                    pdf_path = pdf_generator.generate_multiple_tasks_report(
                        tasks_analyses={},  # Sin análisis individuales
                        consolidated_analysis=consolidated_analysis
                    )
                    print(f"✓ Reporte PDF consolidado generado: {pdf_path}")
                else:
                    print(f"\n✗ Error en el análisis consolidado: {consolidated_analysis['error']}")
            
            elif opcion == "6":
                print("\nSaliendo...")
                break
            
            else:
                print("\n✗ Opción no válida. Por favor seleccione 1-6.")
                print_menu()
            print("\n" + "-" * 60 + "\n")
        
        except KeyboardInterrupt:
            print("\n\nSaliendo...")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("\n" + "-" * 60 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

