"""
Módulo core - Funciones principales de cálculo.
"""

from .calculations import (
    calcular_temperatura,
    calcular_tiempo_para_temperatura,
    calcular_constante_K,
    generar_tabla_enfriamiento
)

__all__ = [
    'calcular_temperatura',
    'calcular_tiempo_para_temperatura',
    'calcular_constante_K',
    'generar_tabla_enfriamiento'
]
