"""
AutoForense - Automatización Inteligente de Análisis Forense en Sistemas Windows
Código principal del proyecto
"""
import sys
import os
import subprocess
from PowershellHelper import PowerShellHelper


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
    print("4. Salir")
    print()

def main():
    """Función principal del programa"""
    # Mostrar arte ASCII de bienvenida
    mostrar_bienvenida()
    
    # Inicializar el helper de PowerShell
    try:
        ps_helper = PowerShellHelper()
        print("✓ Módulo PowerShell cargado correctamente")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return 1
    
    
    while True:
        try:
            print_menu()
            opcion = input("Seleccione una opción (1-4): ").strip()
            
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
                print("\nSaliendo...")
                break
            
            else:
                print("\n✗ Opción no válida. Por favor seleccione 1-4.")
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

