"""
=====================================================================
    MENU - Menú principal de la aplicación
=====================================================================
Funciones para mostrar y controlar el menú principal.
=====================================================================
"""

from ..core.constants import APP_TITLE, LINE_WIDTH, SEPARATOR_CHAR, SUBSEPARATOR_CHAR
from ..utils.screen import limpiar_pantalla
from .display import mostrar_informacion
from .options import (
    opcion_calcular_temperatura,
    opcion_calcular_tiempo,
    opcion_calcular_constante_K,
    opcion_generar_tabla
)


def mostrar_menu_principal():
    """Muestra el menú principal de la aplicación."""
    print("\n" + SEPARATOR_CHAR * LINE_WIDTH)
    print(f"    {APP_TITLE}")
    print(SEPARATOR_CHAR * LINE_WIDTH)
    print("\n📋 MENÚ DE OPCIONES:\n")
    print("  1. Calcular temperatura en un tiempo específico")
    print("  2. Calcular tiempo para alcanzar una temperatura")
    print("  3. Calcular constante K (con datos conocidos)")
    print("  4. Generar tabla de enfriamiento")
    print("  5. Ver información sobre la ley")
    print("  6. Salir")
    print("\n" + SUBSEPARATOR_CHAR * LINE_WIDTH)


def ejecutar_aplicacion():
    """
    Función principal que ejecuta el programa.
    Controla el flujo del menú y las opciones.
    """
    while True:
        limpiar_pantalla()
        mostrar_menu_principal()
        
        opcion = input("\n👉 Seleccione una opción (1-6): ").strip()
        
        if opcion == "1":
            opcion_calcular_temperatura()
        elif opcion == "2":
            opcion_calcular_tiempo()
        elif opcion == "3":
            opcion_calcular_constante_K()
        elif opcion == "4":
            opcion_generar_tabla()
        elif opcion == "5":
            mostrar_informacion()
        elif opcion == "6":
            print("\n👋 ¡Gracias por usar la aplicación!")
            print(SEPARATOR_CHAR * LINE_WIDTH)
            break
        else:
            print("\n❌ Opción inválida. Por favor seleccione una opción del 1 al 6.")
            input("Presione ENTER para continuar...")
