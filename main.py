"""
=====================================================================
    MAIN - Punto de entrada de la aplicación
=====================================================================
    APLICACIÓN: LEY DE ENFRIAMIENTO DE NEWTON
    
    Esta aplicación calcula la temperatura de un objeto en función del 
    tiempo utilizando la Ley de Enfriamiento de Newton.
    
    Fórmula: T(t) = Tm + C * e^(K*t)
    
    Autor: Neider Duvan Guindigua Machoa
    Fecha: 3 de Noviembre de 2025
=====================================================================
"""

from newton_cooling.ui import ejecutar_aplicacion


def main():
    """Punto de entrada principal del programa."""
    ejecutar_aplicacion()


if __name__ == "__main__":
    main()
