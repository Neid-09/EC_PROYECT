"""
=====================================================================
    APLICACIÓN: LEY DE ENFRIAMIENTO DE NEWTON
=====================================================================
Descripción:
    Esta aplicación calcula la temperatura de un objeto en función del 
    tiempo utilizando la Ley de Enfriamiento de Newton.

Fórmula:
    T(t) = Tm + C * e^(K*t)
    
    Donde:
    - T(t): Temperatura del objeto en el tiempo t
    - Tm: Temperatura del medio ambiente (constante)
    - C: Constante que depende de la temperatura inicial (T0 - Tm)
    - K: Constante de enfriamiento (puede ser negativa para enfriamiento)
    - t: Tiempo transcurrido
    - e: Constante de Euler (≈ 2.71828)

Autor: [Neider Duvan Guindigua Machoa]
Fecha: 3 de Noviembre de 2025
=====================================================================
"""

import math
import os

# =====================================================================
# CONSTANTES GLOBALES
# =====================================================================
E = math.e  # Constante de Euler (más precisa usando math.e)


# =====================================================================
# FUNCIONES PRINCIPALES
# =====================================================================

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


# =====================================================================
# FUNCIONES DE ENTRADA/SALIDA
# =====================================================================

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def solicitar_numero(mensaje, valor_minimo=None, valor_maximo=None):
    """
    Solicita un número al usuario con validación.
    
    Parámetros:
        mensaje (str): Mensaje a mostrar al usuario
        valor_minimo (float): Valor mínimo permitido (opcional)
        valor_maximo (float): Valor máximo permitido (opcional)
    
    Retorna:
        float: Número ingresado por el usuario
    """
    while True:
        try:
            valor = float(input(mensaje))
            
            if valor_minimo is not None and valor < valor_minimo:
                print(f"❌ Error: El valor debe ser mayor o igual a {valor_minimo}")
                continue
            
            if valor_maximo is not None and valor > valor_maximo:
                print(f"❌ Error: El valor debe ser menor o igual a {valor_maximo}")
                continue
            
            return valor
        except ValueError:
            print("❌ Error: Por favor ingrese un número válido.")


def mostrar_menu():
    """Muestra el menú principal de la aplicación."""
    print("\n" + "="*60)
    print("    LEY DE ENFRIAMIENTO DE NEWTON - CALCULADORA")
    print("="*60)
    print("\n📋 MENÚ DE OPCIONES:\n")
    print("  1. Calcular temperatura en un tiempo específico")
    print("  2. Calcular tiempo para alcanzar una temperatura")
    print("  3. Calcular constante K (con datos conocidos)")
    print("  4. Generar tabla de enfriamiento")
    print("  5. Ver información sobre la ley")
    print("  6. Salir")
    print("\n" + "-"*60)


def mostrar_informacion():
    """Muestra información detallada sobre la Ley de Enfriamiento de Newton."""
    print("\n" + "="*60)
    print("    INFORMACIÓN: LEY DE ENFRIAMIENTO DE NEWTON")
    print("="*60)
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


def opcion_calcular_temperatura():
    """Maneja la opción 1: Calcular temperatura en un tiempo específico."""
    print("\n" + "="*60)
    print("    OPCIÓN 1: CALCULAR TEMPERATURA")
    print("="*60)
    
    print("\n📝 Ingrese los datos:\n")
    Tm = solicitar_numero("  Temperatura ambiente Tm (°C): ")
    C = solicitar_numero("  Constante C: ")
    K = solicitar_numero("  Constante K (negativa para enfriamiento): ")
    t = solicitar_numero("  Tiempo transcurrido t (minutos): ", valor_minimo=0)
    
    temperatura = calcular_temperatura(Tm, C, K, t)
    
    print("\n" + "-"*60)
    print("📊 RESULTADO:")
    print(f"   Temperatura después de {t} minutos: {temperatura:.2f}°C")
    print(f"   Fórmula usada: T = {Tm} + {C} * e^({K}*{t})")
    print("-"*60)
    
    input("\nPresione ENTER para continuar...")


def opcion_calcular_tiempo():
    """Maneja la opción 2: Calcular tiempo para alcanzar temperatura objetivo."""
    print("\n" + "="*60)
    print("    OPCIÓN 2: CALCULAR TIEMPO")
    print("="*60)
    
    print("\n📝 Ingrese los datos:\n")
    Tm = solicitar_numero("  Temperatura ambiente Tm (°C): ")
    C = solicitar_numero("  Constante C: ")
    K = solicitar_numero("  Constante K: ")
    T_objetivo = solicitar_numero("  Temperatura objetivo (°C): ")
    
    tiempo = calcular_tiempo_para_temperatura(Tm, C, K, T_objetivo)
    
    print("\n" + "-"*60)
    print("📊 RESULTADO:")
    if tiempo is None:
        print("   ❌ No es posible alcanzar esa temperatura con estos parámetros.")
    elif tiempo == float('inf'):
        print("   ⚠️  El objeto nunca alcanzará exactamente esa temperatura.")
    else:
        print(f"   Tiempo necesario: {tiempo:.2f} minutos ({tiempo/60:.2f} horas)")
    print("-"*60)
    
    input("\nPresione ENTER para continuar...")


def opcion_calcular_constante_K():
    """Maneja la opción 3: Calcular constante K con datos conocidos."""
    print("\n" + "="*60)
    print("    OPCIÓN 3: CALCULAR CONSTANTE K")
    print("="*60)
    print("\n💡 Esta opción calcula K cuando conoces:")
    print("   • Temperatura inicial T(0)")
    print("   • Temperatura ambiente Tm")
    print("   • Temperatura en un tiempo específico T(t)")
    print("   • El tiempo t en que se midió")
    
    print("\n📝 Ingrese los datos:\n")
    T0 = solicitar_numero("  Temperatura inicial T(0) (°C): ")
    Tm = solicitar_numero("  Temperatura ambiente Tm (°C): ")
    T_en_t = solicitar_numero("  Temperatura en tiempo t (°C): ")
    t = solicitar_numero("  Tiempo t en que se midió (minutos): ", valor_minimo=0.0001)
    
    K, C = calcular_constante_K(T0, Tm, T_en_t, t)
    
    print("\n" + "-"*60)
    print("📊 RESULTADO:")
    if K is None:
        print("   ❌ No es posible calcular K con estos datos.")
        print("   Verifica que los datos sean consistentes.")
    else:
        print(f"   Constante K = {K:.6f} (1/min)")
        print(f"   Constante C = {C:.2f} (°C)")
        print(f"\n   Fórmula completa: T(t) = {Tm} + {C:.2f} * e^({K:.6f}*t)")
        
        # Verificación
        T_verificacion = calcular_temperatura(Tm, C, K, t)
        print(f"\n   ✓ Verificación en t={t} min: T = {T_verificacion:.2f}°C")
        
        if K < 0:
            print(f"   📉 K negativa → El objeto se está ENFRIANDO")
        elif K > 0:
            print(f"   📈 K positiva → El objeto se está CALENTANDO")
        else:
            print(f"   ➡️  K = 0 → Temperatura constante")
    print("-"*60)
    
    input("\nPresione ENTER para continuar...")


def opcion_generar_tabla():
    """Maneja la opción 4: Generar tabla de enfriamiento."""
    print("\n" + "="*60)
    print("    OPCIÓN 4: TABLA DE ENFRIAMIENTO")
    print("="*60)
    
    print("\n📝 Ingrese los datos:\n")
    Tm = solicitar_numero("  Temperatura ambiente Tm (°C): ")
    C = solicitar_numero("  Constante C: ")
    K = solicitar_numero("  Constante K: ")
    tiempo_total = solicitar_numero("  Tiempo total a simular (minutos): ", valor_minimo=0)
    intervalo = solicitar_numero("  Intervalo entre mediciones (minutos): ", valor_minimo=0.1)
    
    tabla = generar_tabla_enfriamiento(Tm, C, K, tiempo_total, intervalo)
    
    print("\n" + "="*60)
    print(f"📊 TABLA DE ENFRIAMIENTO - Fórmula: T = {Tm} + {C} * e^({K}*t)")
    print("="*60)
    print(f"{'Tiempo (min)':>15} | {'Temperatura (°C)':>20}")
    print("-"*60)
    
    for tiempo, temperatura in tabla:
        print(f"{tiempo:>15.2f} | {temperatura:>20.2f}")
    
    print("="*60)
    
    input("\nPresione ENTER para continuar...")


# =====================================================================
# FUNCIÓN PRINCIPAL
# =====================================================================

def main():
    """
    Función principal que ejecuta el programa.
    Controla el flujo del menú y las opciones.
    """
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
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
            print("="*60)
            break
        else:
            print("\n❌ Opción inválida. Por favor seleccione una opción del 1 al 6.")
            input("Presione ENTER para continuar...")


# =====================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# =====================================================================

if __name__ == "__main__":
    main()
