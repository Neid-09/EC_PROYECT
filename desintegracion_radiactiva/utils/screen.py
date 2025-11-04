"""
=====================================================================
    SCREEN - Utilidades de pantalla
=====================================================================
Funciones para manipular la visualización de la consola.
=====================================================================
"""

import os


def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')
