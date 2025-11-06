"""
=====================================================================
    OPTIONS - Opciones del menú principal
=====================================================================
Contiene las funciones para cada opción del menú con sus submenús.
=====================================================================
"""

from ..core.calculations import (
    calcular_temperatura,
    calcular_tiempo_para_temperatura,
    calcular_constante_K,
    calcular_constante_C,
    generar_tabla_enfriamiento
)
from ..utils.validators import solicitar_numero
from .display import (
    mostrar_cabecera,
    mostrar_datos_actuales,
    mostrar_submenu,
    mostrar_resultado_temperatura,
    mostrar_resultado_tiempo,
    mostrar_resultado_K,
    mostrar_tabla
)


def opcion_calcular_temperatura():
    """Maneja la opción 1: Calcular temperatura en un tiempo específico."""
    # Variables para almacenar datos calculados
    Tm = None
    C = None
    K = None
    ultima_temperatura = None
    ultimo_tiempo = None
    
    opciones_submenu = [
        ("a", "Ingresar nuevos datos y calcular"),
        ("b", "Calcular temperatura en otro tiempo (usar datos actuales)"),
        ("c", "Generar tabla con datos actuales"),
        ("d", "Regresar al menú principal")
    ]
    
    while True:
        mostrar_cabecera("OPCIÓN 1: CALCULAR TEMPERATURA")
        
        # Mostrar datos actuales si existen
        if Tm is not None:
            info_adicional = None
            if ultima_temperatura is not None:
                info_adicional = f"Último cálculo: T({ultimo_tiempo} min) = {ultima_temperatura:.2f}°C"
            mostrar_datos_actuales(Tm, C, K, info_adicional)
        
        mostrar_submenu(opciones_submenu)
        
        sub_opcion = input("\n👉 Seleccione una opción (a-d): ").strip().lower()
        
        if sub_opcion == "a":
            print("\n📝 Ingrese los datos:\n")
            Tm = solicitar_numero("  Temperatura ambiente Tm (°C): ")
            
            # Preguntar si desea calcular C automáticamente
            print("\n¿Cómo desea ingresar la constante C?")
            print("  1. Ingresar C directamente")
            print("  2. Calcular C automáticamente (C = T_inicial - Tm)")
            
            opcion_c = input("Seleccione (1 o 2): ").strip()
            
            if opcion_c == "2":
                T_inicial = solicitar_numero("  Temperatura inicial T(0) (°C): ")
                C = calcular_constante_C(T_inicial, Tm)
                print(f"\n✅ C calculado: C = {T_inicial} - {Tm} = {C:.2f}")
            else:
                C = solicitar_numero("  Constante C: ")
            
            K = solicitar_numero("  Constante K (negativa para enfriamiento): ")
            ultimo_tiempo = solicitar_numero("  Tiempo transcurrido t (minutos): ", valor_minimo=0)
            
            ultima_temperatura = calcular_temperatura(Tm, C, K, ultimo_tiempo)
            
            formula = f"Fórmula usada: T = {Tm} + {C} * e^({K}*{ultimo_tiempo})"
            mostrar_resultado_temperatura(ultimo_tiempo, ultima_temperatura, formula)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "b":
            if Tm is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C}, K={K}")
            ultimo_tiempo = solicitar_numero("  Tiempo transcurrido t (minutos): ", valor_minimo=0)
            
            ultima_temperatura = calcular_temperatura(Tm, C, K, ultimo_tiempo)
            mostrar_resultado_temperatura(ultimo_tiempo, ultima_temperatura)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "c":
            if Tm is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C}, K={K}")
            tiempo_total = solicitar_numero("  Tiempo total a simular (minutos): ", valor_minimo=0)
            intervalo = solicitar_numero("  Intervalo entre mediciones (minutos): ", valor_minimo=0.1)
            
            tabla = generar_tabla_enfriamiento(Tm, C, K, tiempo_total, intervalo)
            mostrar_tabla(tabla, Tm, C, K)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "d":
            break
        else:
            print("\n❌ Opción inválida. Seleccione a, b, c o d.")
            input("Presione ENTER para continuar...")


def opcion_calcular_tiempo():
    """Maneja la opción 2: Calcular tiempo para alcanzar temperatura objetivo."""
    # Variables para almacenar datos calculados
    Tm = None
    C = None
    K = None
    ultimo_tiempo = None
    ultima_temp_objetivo = None
    
    opciones_submenu = [
        ("a", "Ingresar nuevos datos y calcular"),
        ("b", "Calcular tiempo para otra temperatura (usar datos actuales)"),
        ("c", "Calcular temperatura en un tiempo específico"),
        ("d", "Generar tabla con datos actuales"),
        ("e", "Regresar al menú principal")
    ]
    
    while True:
        mostrar_cabecera("OPCIÓN 2: CALCULAR TIEMPO")
        
        # Mostrar datos actuales si existen
        if Tm is not None:
            info_adicional = None
            if ultimo_tiempo is not None and ultimo_tiempo != float('inf'):
                info_adicional = f"Último cálculo: t = {ultimo_tiempo:.2f} min para alcanzar {ultima_temp_objetivo}°C"
            mostrar_datos_actuales(Tm, C, K, info_adicional)
        
        mostrar_submenu(opciones_submenu)
        
        sub_opcion = input("\n👉 Seleccione una opción (a-e): ").strip().lower()
        
        if sub_opcion == "a":
            print("\n📝 Ingrese los datos:\n")
            Tm = solicitar_numero("  Temperatura ambiente Tm (°C): ")
            
            # Preguntar si desea calcular C automáticamente
            print("\n¿Cómo desea ingresar la constante C?")
            print("  1. Ingresar C directamente")
            print("  2. Calcular C automáticamente (C = T_inicial - Tm)")
            
            opcion_c = input("Seleccione (1 o 2): ").strip()
            
            if opcion_c == "2":
                T_inicial = solicitar_numero("  Temperatura inicial T(0) (°C): ")
                C = calcular_constante_C(T_inicial, Tm)
                print(f"\n✅ C calculado: C = {T_inicial} - {Tm} = {C:.2f}")
            else:
                C = solicitar_numero("  Constante C: ")
            
            K = solicitar_numero("  Constante K: ")
            ultima_temp_objetivo = solicitar_numero("  Temperatura objetivo (°C): ")
            
            ultimo_tiempo = calcular_tiempo_para_temperatura(Tm, C, K, ultima_temp_objetivo)
            mostrar_resultado_tiempo(ultimo_tiempo, ultima_temp_objetivo)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "b":
            if Tm is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C}, K={K}")
            ultima_temp_objetivo = solicitar_numero("  Temperatura objetivo (°C): ")
            
            ultimo_tiempo = calcular_tiempo_para_temperatura(Tm, C, K, ultima_temp_objetivo)
            mostrar_resultado_tiempo(ultimo_tiempo, ultima_temp_objetivo)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "c":
            if Tm is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C}, K={K}")
            t = solicitar_numero("  Tiempo t (minutos): ", valor_minimo=0)
            
            temperatura = calcular_temperatura(Tm, C, K, t)
            mostrar_resultado_temperatura(t, temperatura)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "d":
            if Tm is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C}, K={K}")
            tiempo_total = solicitar_numero("  Tiempo total a simular (minutos): ", valor_minimo=0)
            intervalo = solicitar_numero("  Intervalo entre mediciones (minutos): ", valor_minimo=0.1)
            
            tabla = generar_tabla_enfriamiento(Tm, C, K, tiempo_total, intervalo)
            mostrar_tabla(tabla, Tm, C, K)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "e":
            break
        else:
            print("\n❌ Opción inválida. Seleccione a, b, c, d o e.")
            input("Presione ENTER para continuar...")


def opcion_calcular_constante_K():
    """Maneja la opción 3: Calcular constante K con datos conocidos."""
    # Variables para almacenar datos calculados
    T0 = None
    Tm = None
    K = None
    C = None
    
    opciones_submenu = [
        ("a", "Calcular K con nuevos datos"),
        ("b", "Calcular temperatura en un tiempo específico"),
        ("c", "Calcular tiempo para alcanzar una temperatura"),
        ("d", "Generar tabla con datos calculados"),
        ("e", "Regresar al menú principal")
    ]
    
    while True:
        mostrar_cabecera("OPCIÓN 3: CALCULAR CONSTANTE K")
        print("\n💡 Esta opción calcula K cuando conoces:")
        print("   • Temperatura inicial T(0)")
        print("   • Temperatura ambiente Tm")
        print("   • Temperatura en un tiempo específico T(t)")
        print("   • El tiempo t en que se midió")
        
        # Mostrar datos actuales si existen
        if K is not None:
            print(f"\n📌 DATOS CALCULADOS:")
            print(f"   K = {K:.6f} (1/min) | C = {C:.2f} | Tm = {Tm}°C | T(0) = {T0}°C")
        
        mostrar_submenu(opciones_submenu)
        
        sub_opcion = input("\n👉 Seleccione una opción (a-e): ").strip().lower()
        
        if sub_opcion == "a":
            print("\n📝 Ingrese los datos:\n")
            T0 = solicitar_numero("  Temperatura inicial T(0) (°C): ")
            Tm = solicitar_numero("  Temperatura ambiente Tm (°C): ")
            T_en_t = solicitar_numero("  Temperatura en tiempo t (°C): ")
            t = solicitar_numero("  Tiempo t en que se midió (minutos): ", valor_minimo=0.0001)
            
            K, C = calcular_constante_K(T0, Tm, T_en_t, t)
            
            # Verificación
            T_verificacion = None
            if K is not None:
                T_verificacion = calcular_temperatura(Tm, C, K, t)
            
            mostrar_resultado_K(K, C, Tm, t, T_verificacion)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "b":
            if K is None:
                print("\n❌ Primero debe calcular K (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C:.2f}, K={K:.6f}")
            t = solicitar_numero("  Tiempo t (minutos): ", valor_minimo=0)
            
            temperatura = calcular_temperatura(Tm, C, K, t)
            mostrar_resultado_temperatura(t, temperatura)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "c":
            if K is None:
                print("\n❌ Primero debe calcular K (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C:.2f}, K={K:.6f}")
            T_objetivo = solicitar_numero("  Temperatura objetivo (°C): ")
            
            tiempo = calcular_tiempo_para_temperatura(Tm, C, K, T_objetivo)
            mostrar_resultado_tiempo(tiempo, T_objetivo)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "d":
            if K is None:
                print("\n❌ Primero debe calcular K (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C:.2f}, K={K:.6f}")
            tiempo_total = solicitar_numero("  Tiempo total a simular (minutos): ", valor_minimo=0)
            intervalo = solicitar_numero("  Intervalo entre mediciones (minutos): ", valor_minimo=0.1)
            
            tabla = generar_tabla_enfriamiento(Tm, C, K, tiempo_total, intervalo)
            mostrar_tabla(tabla, Tm, C, K)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "e":
            break
        else:
            print("\n❌ Opción inválida. Seleccione a, b, c, d o e.")
            input("Presione ENTER para continuar...")


def opcion_calcular_constante_C():
    """Maneja la opción 4: Calcular constante C."""
    while True:
        mostrar_cabecera("OPCIÓN 4: CALCULAR CONSTANTE C")
        print("\n💡 Esta opción calcula C usando la fórmula:")
        print("   C = T_inicial - Tm")
        print("\n   Donde:")
        print("   • T_inicial: Temperatura inicial del objeto en t=0")
        print("   • Tm: Temperatura del medio ambiente")
        
        print("\n📝 Ingrese los datos:\n")
        T_inicial = solicitar_numero("  Temperatura inicial T(0) (°C): ")
        Tm = solicitar_numero("  Temperatura ambiente Tm (°C): ")
        
        C = calcular_constante_C(T_inicial, Tm)
        
        print("\n" + "─" * 60)
        print("✅ RESULTADO:")
        print("─" * 60)
        print(f"\n  C = T_inicial - Tm")
        print(f"  C = {T_inicial} - {Tm}")
        print(f"  C = {C:.2f}")
        print("\n" + "─" * 60)
        
        # Interpretación del resultado
        if C > 0:
            print("\n📊 Interpretación:")
            print(f"  • C es positivo ({C:.2f})")
            print("  • El objeto está más caliente que el ambiente")
            print("  • Con K negativo, el objeto se enfriará hacia Tm")
        elif C < 0:
            print("\n📊 Interpretación:")
            print(f"  • C es negativo ({C:.2f})")
            print("  • El objeto está más frío que el ambiente")
            print("  • Con K positivo, el objeto se calentará hacia Tm")
        else:
            print("\n📊 Interpretación:")
            print("  • C es cero")
            print("  • El objeto ya está a la temperatura ambiente")
            print("  • La temperatura no cambiará con el tiempo")
        
        print("\n¿Desea hacer otro cálculo de C?")
        respuesta = input("(s/n): ").strip().lower()
        if respuesta != 's':
            break
        print()


def opcion_generar_tabla():
    """Maneja la opción 4: Generar tabla de enfriamiento."""
    # Variables para almacenar datos calculados
    Tm = None
    C = None
    K = None
    ultima_tabla = None
    
    opciones_submenu = [
        ("a", "Generar tabla con nuevos datos"),
        ("b", "Generar tabla con diferente intervalo/tiempo"),
        ("c", "Calcular temperatura en un tiempo específico"),
        ("d", "Calcular tiempo para alcanzar una temperatura"),
        ("e", "Regresar al menú principal")
    ]
    
    while True:
        mostrar_cabecera("OPCIÓN 4: TABLA DE ENFRIAMIENTO")
        
        # Mostrar datos actuales si existen
        if Tm is not None:
            mostrar_datos_actuales(Tm, C, K)
        
        mostrar_submenu(opciones_submenu)
        
        sub_opcion = input("\n👉 Seleccione una opción (a-e): ").strip().lower()
        
        if sub_opcion == "a":
            print("\n📝 Ingrese los datos:\n")
            Tm = solicitar_numero("  Temperatura ambiente Tm (°C): ")
            
            # Preguntar si desea calcular C automáticamente
            print("\n¿Cómo desea ingresar la constante C?")
            print("  1. Ingresar C directamente")
            print("  2. Calcular C automáticamente (C = T_inicial - Tm)")
            
            opcion_c = input("Seleccione (1 o 2): ").strip()
            
            if opcion_c == "2":
                T_inicial = solicitar_numero("  Temperatura inicial T(0) (°C): ")
                C = calcular_constante_C(T_inicial, Tm)
                print(f"\n✅ C calculado: C = {T_inicial} - {Tm} = {C:.2f}")
            else:
                C = solicitar_numero("  Constante C: ")
            
            K = solicitar_numero("  Constante K: ")
            tiempo_total = solicitar_numero("  Tiempo total a simular (minutos): ", valor_minimo=0)
            intervalo = solicitar_numero("  Intervalo entre mediciones (minutos): ", valor_minimo=0.1)
            
            ultima_tabla = generar_tabla_enfriamiento(Tm, C, K, tiempo_total, intervalo)
            mostrar_tabla(ultima_tabla, Tm, C, K)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "b":
            if Tm is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C}, K={K}")
            tiempo_total = solicitar_numero("  Tiempo total a simular (minutos): ", valor_minimo=0)
            intervalo = solicitar_numero("  Intervalo entre mediciones (minutos): ", valor_minimo=0.1)
            
            ultima_tabla = generar_tabla_enfriamiento(Tm, C, K, tiempo_total, intervalo)
            mostrar_tabla(ultima_tabla, Tm, C, K)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "c":
            if Tm is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C}, K={K}")
            t = solicitar_numero("  Tiempo t (minutos): ", valor_minimo=0)
            
            temperatura = calcular_temperatura(Tm, C, K, t)
            mostrar_resultado_temperatura(t, temperatura)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "d":
            if Tm is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: Tm={Tm}°C, C={C}, K={K}")
            T_objetivo = solicitar_numero("  Temperatura objetivo (°C): ")
            
            tiempo = calcular_tiempo_para_temperatura(Tm, C, K, T_objetivo)
            mostrar_resultado_tiempo(tiempo, T_objetivo)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "e":
            break
        else:
            print("\n❌ Opción inválida. Seleccione a, b, c, d o e.")
            input("Presione ENTER para continuar...")
