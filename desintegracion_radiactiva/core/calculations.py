"""
=====================================================================
    CALCULATIONS - Cálculos de desintegración radiactiva
=====================================================================
Funciones matemáticas para resolver la ecuación de desintegración:
dN/dt = -kN  →  N(t) = N0 * e^(-k*t)
=====================================================================
"""

import math
from .constants import LN_2


def calcular_constante_k(t_media):
    """
    Calcula la constante de desintegración k a partir de la media de vida.
    
    Fórmula: k = ln(2) / t_media
    
    Parámetros:
        t_media (float): Media de vida (tiempo en el que N = N0/2)
    
    Retorna:
        float: Constante de desintegración k (positiva, siempre)
    """
    if t_media <= 0:
        return None
    
    k = LN_2 / t_media
    return k


def calcular_N_en_tiempo_t(N0, k, t):
    """
    Calcula la cantidad de sustancia N en un tiempo t.
    
    Fórmula: N(t) = N0 * e^(-k*t)
    
    Parámetros:
        N0 (float): Cantidad inicial de sustancia
        k (float): Constante de desintegración (positiva)
        t (float): Tiempo transcurrido
    
    Retorna:
        float: Cantidad de sustancia en el tiempo t
    """
    if N0 < 0 or k <= 0 or t < 0:
        return None
    
    N = N0 * math.exp(-k * t)
    return N


def calcular_tiempo_t(N0, N, k):
    """
    Calcula el tiempo necesario para que la cantidad pase de N0 a N.
    
    Fórmula: t = ln(N0/N) / k
    
    IMPORTANTE: N debe ser MENOR que N0 (la cantidad disminuye)
    Ejemplo: Si queda 65% del original:
             N0 = 100 (o 1 = 100%)
             N = 65 (o 0.65 = 65%)
             t = ln(100/65) / k = ln(1.538) / k
    
    Parámetros:
        N0 (float): Cantidad INICIAL de sustancia (en t=0)
        N (float): Cantidad FINAL/ACTUAL de sustancia (en t=?)
        k (float): Constante de desintegración (positiva)
    
    Retorna:
        float: Tiempo necesario (None si es imposible)
    """
    if N0 <= 0 or k <= 0:
        return None
    
    if N < 0 or N > N0:
        return None
    
    if N == 0:
        return float('inf')  # Tiempo infinito para llegar a 0
    
    if N == N0:
        return 0.0
    
    t = math.log(N0 / N) / k
    return t


def calcular_N0(N, k, t):
    """
    Calcula la cantidad inicial N0 a partir de la cantidad en el tiempo t.
    
    Fórmula: N0 = N * e^(k*t)
    
    Parámetros:
        N (float): Cantidad de sustancia en el tiempo t
        k (float): Constante de desintegración
        t (float): Tiempo transcurrido
    
    Retorna:
        float: Cantidad inicial de sustancia
    """
    if N < 0 or k <= 0 or t < 0:
        return None
    
    N0 = N * math.exp(k * t)
    return N0


def calcular_media_vida(k):
    """
    Calcula la media de vida a partir de la constante k.
    
    Fórmula: t_media = ln(2) / k
    
    Parámetros:
        k (float): Constante de desintegración
    
    Retorna:
        float: Media de vida
    """
    if k <= 0:
        return None
    
    t_media = LN_2 / k
    return t_media


def calcular_k_desde_datos(N0, N, t):
    """
    Calcula la constante k cuando se conoce N0, N en un tiempo t.
    
    Fórmula: k = ln(N0/N) / t
    
    Parámetros:
        N0 (float): Cantidad inicial
        N (float): Cantidad en el tiempo t
        t (float): Tiempo transcurrido
    
    Retorna:
        tuple: (k, t_media) o (None, None) si no es posible
    """
    if N0 <= 0 or N <= 0 or t <= 0:
        return None, None
    
    if N > N0:
        return None, None
    
    if N == N0:
        return 0.0, float('inf')
    
    try:
        k = math.log(N0 / N) / t
        t_media = calcular_media_vida(k)
        return k, t_media
    except (ValueError, ZeroDivisionError):
        return None, None


def generar_tabla_desintegracion(N0, k, tiempo_total, intervalo):
    """
    Genera una tabla de valores de desintegración.
    
    Parámetros:
        N0 (float): Cantidad inicial
        k (float): Constante de desintegración
        tiempo_total (float): Tiempo total a simular
        intervalo (float): Intervalo entre mediciones
    
    Retorna:
        list: Lista de tuplas (tiempo, N, porcentaje)
    """
    tabla = []
    tiempo_actual = 0.0
    
    while tiempo_actual <= tiempo_total:
        N = calcular_N_en_tiempo_t(N0, k, tiempo_actual)
        porcentaje = (N / N0) * 100
        tabla.append((tiempo_actual, N, porcentaje))
        tiempo_actual += intervalo
    
    return tabla
