"""
=====================================================================
    DISPLAY - Funciones de visualización
=====================================================================
Funciones para mostrar información y resultados formateados.
=====================================================================
"""

from ..core.constants import LINE_WIDTH, SEPARATOR_CHAR, SUBSEPARATOR_CHAR


def mostrar_cabecera(titulo):
    """
    Muestra una cabecera formateada.
    
    Parámetros:
        titulo (str): Título a mostrar
    """
    print("\n" + SEPARATOR_CHAR * LINE_WIDTH)
    print(f"    {titulo}")
    print(SEPARATOR_CHAR * LINE_WIDTH)


def mostrar_separador():
    """Muestra un separador de línea."""
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)


def mostrar_datos_actuales(Tm, C, K, info_adicional=None):
    """
    Muestra los datos actuales guardados.
    
    Parámetros:
        Tm (float): Temperatura ambiente
        C (float): Constante C
        K (float): Constante K
        info_adicional (str): Información adicional opcional
    """
    print("\n📌 DATOS ACTUALES:")
    print(f"   Tm = {Tm}°C | C = {C} | K = {K}")
    if info_adicional:
        print(f"   {info_adicional}")


def mostrar_submenu(opciones):
    """
    Muestra un submenú con opciones.
    
    Parámetros:
        opciones (list): Lista de tuplas (letra, descripción)
    """
    print("\n📋 SUBMENÚ:")
    for letra, descripcion in opciones:
        print(f"  {letra}) {descripcion}")


def mostrar_resultado_temperatura(tiempo, temperatura, formula=None):
    """
    Muestra el resultado de un cálculo de temperatura.
    
    Parámetros:
        tiempo (float): Tiempo en minutos
        temperatura (float): Temperatura calculada
        formula (str): Fórmula utilizada (opcional)
    """
    print("\n" + SUBSEPARATOR_CHAR * LINE_WIDTH)
    print("📊 RESULTADO:")
    print(f"   Temperatura después de {tiempo} minutos: {temperatura:.2f}°C")
    if formula:
        print(f"   {formula}")
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)


def mostrar_resultado_tiempo(tiempo, temp_objetivo):
    """
    Muestra el resultado de un cálculo de tiempo.
    
    Parámetros:
        tiempo (float): Tiempo calculado (puede ser None o inf)
        temp_objetivo (float): Temperatura objetivo
    """
    print("\n" + SUBSEPARATOR_CHAR * LINE_WIDTH)
    print("📊 RESULTADO:")
    if tiempo is None:
        print("   ❌ No es posible alcanzar esa temperatura con estos parámetros.")
    elif tiempo == float('inf'):
        print("   ⚠️  El objeto nunca alcanzará exactamente esa temperatura.")
    else:
        print(f"   Tiempo necesario: {tiempo:.2f} minutos ({tiempo/60:.2f} horas)")
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)


def mostrar_resultado_K(K, C, Tm, t_verificacion=None, T_verificacion=None):
    """
    Muestra el resultado del cálculo de K.
    
    Parámetros:
        K (float): Constante K calculada (puede ser None)
        C (float): Constante C calculada
        Tm (float): Temperatura ambiente
        t_verificacion (float): Tiempo de verificación (opcional)
        T_verificacion (float): Temperatura de verificación (opcional)
    """
    print("\n" + SUBSEPARATOR_CHAR * LINE_WIDTH)
    print("📊 RESULTADO:")
    if K is None:
        print("   ❌ No es posible calcular K con estos datos.")
        print("   Verifica que los datos sean consistentes.")
    else:
        print(f"   Constante K = {K:.6f} (1/min)")
        print(f"   Constante C = {C:.2f} (°C)")
        print(f"\n   Fórmula completa: T(t) = {Tm} + {C:.2f} * e^({K:.6f}*t)")
        
        if t_verificacion is not None and T_verificacion is not None:
            print(f"\n   ✓ Verificación en t={t_verificacion} min: T = {T_verificacion:.2f}°C")
        
        if K < 0:
            print(f"   📉 K negativa → El objeto se está ENFRIANDO")
        elif K > 0:
            print(f"   📈 K positiva → El objeto se está CALENTANDO")
        else:
            print(f"   ➡️  K = 0 → Temperatura constante")
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)


def mostrar_tabla(tabla, Tm, C, K):
    """
    Muestra una tabla de enfriamiento formateada.
    
    Parámetros:
        tabla (list): Lista de tuplas (tiempo, temperatura)
        Tm (float): Temperatura ambiente
        C (float): Constante C
        K (float): Constante K
    """
    print("\n" + SEPARATOR_CHAR * LINE_WIDTH)
    print(f"📊 TABLA - T = {Tm} + {C} * e^({K}*t)")
    print(SEPARATOR_CHAR * LINE_WIDTH)
    print(f"{'Tiempo (min)':>15} | {'Temperatura (°C)':>20}")
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)
    
    for tiempo, temperatura in tabla:
        print(f"{tiempo:>15.2f} | {temperatura:>20.2f}")
    
    print(SEPARATOR_CHAR * LINE_WIDTH)


def mostrar_informacion():
    """Muestra información detallada sobre la Ley de Enfriamiento de Newton."""
    mostrar_cabecera("INFORMACIÓN: LEY DE ENFRIAMIENTO DE NEWTON")
    print("""
La Ley de Enfriamiento de Newton establece que la tasa de cambio
de la temperatura de un objeto es proporcional a la diferencia
entre su temperatura y la temperatura del medio ambiente.

📐 FÓRMULA:
   T(t) = Tm + C * e^(K*t)

📊 VARIABLES:
   • T(t): Temperatura en el tiempo t (°C)
   • Tm:   Temperatura del medio ambiente (°C)
   • C:    Constante C (diferencia inicial: T0 - Tm)
   • K:    Constante K (negativa para enfriamiento) (1/min)
   • t:    Tiempo transcurrido (minutos)

💡 VALORES TÍPICOS DE K:
   • Agua en aire: -0.01 a -0.05 (1/min)
   • Metal pequeño: -0.05 a -0.15 (1/min)
   • Café en taza: -0.08 a -0.12 (1/min)
   
💡 NOTA:
   • K es negativo para enfriamiento
   • K es positivo para calentamiento

📝 APLICACIONES:
   • Ciencia forense (determinar hora de muerte)
   • Industria alimentaria (enfriamiento de productos)
   • Ingeniería térmica
   • Meteorología
""")
    input("\nPresione ENTER para continuar...")
