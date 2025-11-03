"""
=====================================================================
    SCREEN - Utilidades de pantalla
=====================================================================
Funciones para manipular la pantalla de la consola.
=====================================================================
"""

import os


def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')
