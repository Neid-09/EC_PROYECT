"""
=====================================================================
    CALCULATIONS - Funciones de cálculo
=====================================================================
Contiene todas las funciones matemáticas relacionadas con la 
Ley de Enfriamiento de Newton.

Fórmula principal: T(t) = Tm + C * e^(K*t)
=====================================================================
"""

import math


def calcular_temperatura(Tm, C, K, t):
    """
    Calcula la temperatura de un objeto usando la Ley de Enfriamiento de Newton.
    Fórmula: T = Tm + C * e^(K*t)
    
    Parámetros:
        Tm (float): Temperatura del medio ambiente (°C)
        C (float): Constante C (diferencia inicial de temperatura)
        K (float): Constante K (generalmente negativa para enfriamiento)
        t (float): Tiempo transcurrido (minutos)
    
    Retorna:
        float: Temperatura del objeto en el tiempo t (°C)
    """
    temperatura = Tm + C * math.exp(K * t)
    return temperatura


def calcular_tiempo_para_temperatura(Tm, C, K, T_objetivo):
    """
    Calcula el tiempo necesario para alcanzar una temperatura objetivo.
    Despejando t de: T = Tm + C * e^(K*t)
    
    Parámetros:
        Tm (float): Temperatura del medio ambiente (°C)
        C (float): Constante C
        K (float): Constante K
        T_objetivo (float): Temperatura deseada (°C)
    
    Retorna:
        float: Tiempo necesario (minutos) o None si no es posible
    """
    # Validar que la temperatura objetivo sea alcanzable
    if T_objetivo == Tm and C != 0:
        return float('inf')  # Nunca alcanza exactamente Tm (a menos que C=0)
    
    # Fórmula despejada: t = ln((T - Tm) / C) / K
    try:
        if C == 0:
            return None
        
        argumento = (T_objetivo - Tm) / C
        
        if argumento <= 0:
            return None
        
        tiempo = math.log(argumento) / K
        
        if tiempo < 0:
            return None
            
        return tiempo
    except (ValueError, ZeroDivisionError):
        return None


def calcular_constante_K(T0, Tm, T_en_t, t):
    """
    Calcula la constante K dados los datos de temperatura.
    Despejando K de: T(t) = Tm + C * e^(K*t), donde C = T0 - Tm
    
    Parámetros:
        T0 (float): Temperatura inicial en t=0 (°C)
        Tm (float): Temperatura del medio ambiente (°C)
        T_en_t (float): Temperatura en un tiempo específico (°C)
        t (float): Tiempo en el que se midió T_en_t (minutos)
    
    Retorna:
        tuple: (K, C) o (None, None) si no es posible calcular
    """
    # C = T0 - Tm
    C = T0 - Tm
    
    # Validaciones
    if t == 0:
        return None, None
    
    if C == 0:
        return None, None
    
    # Fórmula despejada: K = ln((T(t) - Tm) / C) / t
    try:
        argumento = (T_en_t - Tm) / C
        
        if argumento <= 0:
            return None, None
        
        K = math.log(argumento) / t
        
        return K, C
    except (ValueError, ZeroDivisionError):
        return None, None


def generar_tabla_enfriamiento(Tm, C, K, tiempo_total, intervalo):
    """
    Genera una tabla con la evolución de la temperatura en el tiempo.
    
    Parámetros:
        Tm (float): Temperatura del medio ambiente (°C)
        C (float): Constante C
        K (float): Constante K
        tiempo_total (float): Tiempo total a simular (minutos)
        intervalo (float): Intervalo de tiempo entre mediciones (minutos)
    
    Retorna:
        list: Lista de tuplas (tiempo, temperatura)
    """
    tabla = []
    tiempo = 0
    
    while tiempo <= tiempo_total:
        temp = calcular_temperatura(Tm, C, K, tiempo)
        tabla.append((tiempo, temp))
        tiempo += intervalo
    
    return tabla
