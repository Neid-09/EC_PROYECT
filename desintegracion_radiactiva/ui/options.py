"""
=====================================================================
    OPTIONS - Opciones del menú principal
=====================================================================
Contiene las funciones para cada opción del menú con sus submenús.
=====================================================================
"""

from ..core.calculations import (
    calcular_N_en_tiempo_t,
    calcular_tiempo_t,
    calcular_constante_k,
    calcular_N0,
    calcular_media_vida,
    calcular_k_desde_datos,
    generar_tabla_desintegracion
)
from ..utils.validators import solicitar_numero
from .display import (
    mostrar_cabecera,
    mostrar_datos_actuales,
    mostrar_submenu,
    mostrar_resultado_N,
    mostrar_resultado_tiempo,
    mostrar_resultado_k,
    mostrar_resultado_N0,
    mostrar_resultado_media_vida,
    mostrar_tabla,
    formatear_numero
)


def opcion_calcular_N():
    """Maneja la opción 1: Calcular cantidad N en un tiempo t."""
    # Variables para almacenar datos calculados
    N0 = None
    k = None
    t_media = None
    ultimo_N = None
    ultimo_t = None
    
    opciones_submenu = [
        ("a", "Ingresar nuevos datos y calcular N(t)"),
        ("b", "Calcular N en otro tiempo (usar datos actuales)"),
        ("c", "Generar tabla con datos actuales"),
        ("d", "Regresar al menú principal")
    ]
    
    while True:
        mostrar_cabecera("OPCIÓN 1: CALCULAR CANTIDAD N(t)")
        
        # Mostrar datos actuales si existen
        if N0 is not None:
            info_adicional = None
            if ultimo_N is not None:
                info_adicional = f"Último cálculo: N({ultimo_t:.4e}) = {ultimo_N:.4e}"
            mostrar_datos_actuales(N0, k, t_media, info_adicional)
        
        mostrar_submenu(opciones_submenu)
        
        sub_opcion = input("\n👉 Seleccione una opción (a-d): ").strip().lower()
        
        if sub_opcion == "a":
            print("\n📝 Ingrese los datos:\n")
            N0 = solicitar_numero("  Cantidad inicial N0: ", valor_minimo=0)
            if N0 is None:
                continue
            
            k = solicitar_numero("  Constante k (positiva): ", valor_minimo=0.0000001)
            if k is None:
                continue
            
            t_media = calcular_media_vida(k)
            
            ultimo_t = solicitar_numero("  Tiempo transcurrido t: ", valor_minimo=0)
            if ultimo_t is None:
                continue
            
            ultimo_N = calcular_N_en_tiempo_t(N0, k, ultimo_t)
            
            mostrar_resultado_N(ultimo_t, ultimo_N, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "b":
            if N0 is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            ultimo_t = solicitar_numero("  Tiempo transcurrido t: ", valor_minimo=0)
            if ultimo_t is None:
                continue
            
            ultimo_N = calcular_N_en_tiempo_t(N0, k, ultimo_t)
            mostrar_resultado_N(ultimo_t, ultimo_N, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "c":
            if N0 is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            tiempo_total = solicitar_numero("  Tiempo total a simular: ", valor_minimo=0)
            if tiempo_total is None:
                continue
            
            intervalo = solicitar_numero("  Intervalo entre mediciones: ", valor_minimo=0.0001)
            if intervalo is None:
                continue
            
            tabla = generar_tabla_desintegracion(N0, k, tiempo_total, intervalo)
            mostrar_tabla(tabla, N0, k)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "d":
            break
        else:
            print("\n❌ Opción inválida. Seleccione a, b, c o d.")
            input("Presione ENTER para continuar...")


def opcion_calcular_tiempo():
    """Maneja la opción 2: Calcular tiempo para alcanzar una cantidad N."""
    # Variables para almacenar datos calculados
    N0 = None
    k = None
    t_media = None
    ultimo_t = None
    ultimo_N_objetivo = None
    
    opciones_submenu = [
        ("a", "Ingresar nuevos datos y calcular tiempo"),
        ("b", "Calcular tiempo para otra cantidad (usar datos actuales)"),
        ("c", "Calcular N en un tiempo específico"),
        ("d", "Generar tabla con datos actuales"),
        ("e", "Regresar al menú principal")
    ]
    
    while True:
        mostrar_cabecera("OPCIÓN 2: CALCULAR TIEMPO t")
        
        # Mostrar datos actuales si existen
        if N0 is not None:
            info_adicional = None
            if ultimo_t is not None and ultimo_t != float('inf'):
                info_adicional = f"Último cálculo: t = {ultimo_t:.4e} para N = {ultimo_N_objetivo:.4e}"
            mostrar_datos_actuales(N0, k, t_media, info_adicional)
        
        mostrar_submenu(opciones_submenu)
        
        sub_opcion = input("\n👉 Seleccione una opción (a-e): ").strip().lower()
        
        if sub_opcion == "a":
            print("\n📝 Ingrese los datos:\n")
            N0 = solicitar_numero("  Cantidad inicial N0: ", valor_minimo=0)
            if N0 is None:
                continue
            
            k = solicitar_numero("  Constante k (positiva): ", valor_minimo=0.0000001)
            if k is None:
                continue
            
            t_media = calcular_media_vida(k)
            
            print(f"\n💡 Nota: N debe ser MENOR que N0={formatear_numero(N0)}")
            print(f"   Ejemplo: Si queda 65% → N = {N0*0.65:.4e}")
            ultimo_N_objetivo = solicitar_numero("  Cantidad objetivo N: ", valor_minimo=0, valor_maximo=N0)
            if ultimo_N_objetivo is None:
                continue
            
            ultimo_t = calcular_tiempo_t(N0, ultimo_N_objetivo, k)
            mostrar_resultado_tiempo(ultimo_t, ultimo_N_objetivo, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "b":
            if N0 is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            print(f"💡 Nota: N debe ser MENOR que N0 (la cantidad disminuye)")
            print(f"   Ejemplo: Si queda 65% → N = {N0*0.65:.4e}")
            ultimo_N_objetivo = solicitar_numero("  Cantidad objetivo N: ", valor_minimo=0, valor_maximo=N0)
            if ultimo_N_objetivo is None:
                continue
            
            ultimo_t = calcular_tiempo_t(N0, ultimo_N_objetivo, k)
            mostrar_resultado_tiempo(ultimo_t, ultimo_N_objetivo, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "c":
            if N0 is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            t = solicitar_numero("  Tiempo t: ", valor_minimo=0)
            if t is None:
                continue
            
            N = calcular_N_en_tiempo_t(N0, k, t)
            mostrar_resultado_N(t, N, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "d":
            if N0 is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            tiempo_total = solicitar_numero("  Tiempo total a simular: ", valor_minimo=0)
            if tiempo_total is None:
                continue
            
            intervalo = solicitar_numero("  Intervalo entre mediciones: ", valor_minimo=0.0001)
            if intervalo is None:
                continue
            
            tabla = generar_tabla_desintegracion(N0, k, tiempo_total, intervalo)
            mostrar_tabla(tabla, N0, k)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "e":
            break
        else:
            print("\n❌ Opción inválida. Seleccione a, b, c, d o e.")
            input("Presione ENTER para continuar...")


def opcion_calcular_k():
    """Maneja la opción 3: Calcular constante k desde media de vida o datos."""
    # Variables para almacenar datos calculados
    k = None
    t_media = None
    N0 = None
    
    opciones_submenu = [
        ("a", "Calcular k desde media de vida (t_media)"),
        ("b", "Calcular k desde datos experimentales (N0, N, t)"),
        ("c", "Calcular N(t) con datos actuales"),
        ("d", "Calcular tiempo con datos actuales"),
        ("e", "Generar tabla con datos actuales"),
        ("f", "Regresar al menú principal")
    ]
    
    while True:
        mostrar_cabecera("OPCIÓN 3: CALCULAR CONSTANTE k")
        print("\n💡 Esta opción calcula k de dos formas:")
        print("   • Desde la media de vida: k = ln(2) / t_media")
        print("   • Desde datos: k = ln(N0/N) / t")
        
        # Mostrar datos actuales si existen
        if k is not None:
            mostrar_datos_actuales(N0, k, t_media)
        
        mostrar_submenu(opciones_submenu)
        
        sub_opcion = input("\n👉 Seleccione una opción (a-f): ").strip().lower()
        
        if sub_opcion == "a":
            print("\n📝 Ingrese la media de vida:\n")
            t_media = solicitar_numero("  Media de vida (t_media): ", valor_minimo=0.0000001)
            if t_media is None:
                continue
            
            k = calcular_constante_k(t_media)
            
            print(f"\n💡 Nota: La media de vida es el tiempo en que N = N0/2")
            
            mostrar_resultado_k(k, t_media)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "b":
            print("\n📝 Ingrese los datos experimentales:\n")
            N0 = solicitar_numero("  Cantidad inicial N0: ", valor_minimo=0)
            if N0 is None:
                continue
            
            N = solicitar_numero("  Cantidad en tiempo t (N): ", valor_minimo=0, valor_maximo=N0)
            if N is None:
                continue
            
            t = solicitar_numero("  Tiempo en que se midió (t): ", valor_minimo=0.0000001)
            if t is None:
                continue
            
            k, t_media = calcular_k_desde_datos(N0, N, t)
            
            mostrar_resultado_k(k, t_media, N0, N, t)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "c":
            if k is None:
                print("\n❌ Primero debe calcular k (opción a o b)")
                input("Presione ENTER para continuar...")
                continue
            
            if N0 is None:
                N0 = solicitar_numero("  Cantidad inicial N0: ", valor_minimo=0)
                if N0 is None:
                    continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            t = solicitar_numero("  Tiempo t: ", valor_minimo=0)
            if t is None:
                continue
            
            N = calcular_N_en_tiempo_t(N0, k, t)
            mostrar_resultado_N(t, N, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "d":
            if k is None:
                print("\n❌ Primero debe calcular k (opción a o b)")
                input("Presione ENTER para continuar...")
                continue
            
            if N0 is None:
                N0 = solicitar_numero("  Cantidad inicial N0: ", valor_minimo=0)
                if N0 is None:
                    continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            print(f"💡 Nota: N debe ser MENOR que N0 (la cantidad disminuye)")
            print(f"   Ejemplo: Si queda 65% → N0=1, N=0.65 o N0=100, N=65")
            N_objetivo = solicitar_numero("  Cantidad objetivo N: ", valor_minimo=0, valor_maximo=N0)
            if N_objetivo is None:
                continue
            
            t = calcular_tiempo_t(N0, N_objetivo, k)
            mostrar_resultado_tiempo(t, N_objetivo, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "e":
            if k is None:
                print("\n❌ Primero debe calcular k (opción a o b)")
                input("Presione ENTER para continuar...")
                continue
            
            if N0 is None:
                N0 = solicitar_numero("  Cantidad inicial N0: ", valor_minimo=0)
                if N0 is None:
                    continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            tiempo_total = solicitar_numero("  Tiempo total a simular: ", valor_minimo=0)
            if tiempo_total is None:
                continue
            
            intervalo = solicitar_numero("  Intervalo entre mediciones: ", valor_minimo=0.0001)
            if intervalo is None:
                continue
            
            tabla = generar_tabla_desintegracion(N0, k, tiempo_total, intervalo)
            mostrar_tabla(tabla, N0, k)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "f":
            break
        else:
            print("\n❌ Opción inválida. Seleccione a, b, c, d, e o f.")
            input("Presione ENTER para continuar...")


def opcion_calcular_N0():
    """Maneja la opción 4: Calcular cantidad inicial N0."""
    # Variables para almacenar datos calculados
    N0 = None
    k = None
    t_media = None
    
    opciones_submenu = [
        ("a", "Calcular N0 desde datos actuales"),
        ("b", "Calcular N(t) con datos actuales"),
        ("c", "Calcular tiempo con datos actuales"),
        ("d", "Generar tabla con datos actuales"),
        ("e", "Regresar al menú principal")
    ]
    
    while True:
        mostrar_cabecera("OPCIÓN 4: CALCULAR CANTIDAD INICIAL N0")
        print("\n💡 Esta opción calcula N0 cuando conoces:")
        print("   • Cantidad actual N")
        print("   • Constante k")
        print("   • Tiempo transcurrido t")
        
        # Mostrar datos actuales si existen
        if N0 is not None:
            mostrar_datos_actuales(N0, k, t_media)
        
        mostrar_submenu(opciones_submenu)
        
        sub_opcion = input("\n👉 Seleccione una opción (a-e): ").strip().lower()
        
        if sub_opcion == "a":
            print("\n📝 Ingrese los datos:\n")
            N = solicitar_numero("  Cantidad actual N: ", valor_minimo=0)
            if N is None:
                continue
            
            k = solicitar_numero("  Constante k (positiva): ", valor_minimo=0.0000001)
            if k is None:
                continue
            
            t_media = calcular_media_vida(k)
            
            t = solicitar_numero("  Tiempo transcurrido t: ", valor_minimo=0)
            if t is None:
                continue
            
            N0 = calcular_N0(N, k, t)
            
            mostrar_resultado_N0(N0, N, t, k)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "b":
            if N0 is None or k is None:
                print("\n❌ Primero debe calcular N0 (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            t = solicitar_numero("  Tiempo t: ", valor_minimo=0)
            if t is None:
                continue
            
            N = calcular_N_en_tiempo_t(N0, k, t)
            mostrar_resultado_N(t, N, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "c":
            if N0 is None or k is None:
                print("\n❌ Primero debe calcular N0 (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            N_objetivo = solicitar_numero("  Cantidad objetivo N: ", valor_minimo=0, valor_maximo=N0)
            if N_objetivo is None:
                continue
            
            t = calcular_tiempo_t(N0, N_objetivo, k)
            mostrar_resultado_tiempo(t, N_objetivo, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "d":
            if N0 is None or k is None:
                print("\n❌ Primero debe calcular N0 (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            tiempo_total = solicitar_numero("  Tiempo total a simular: ", valor_minimo=0)
            if tiempo_total is None:
                continue
            
            intervalo = solicitar_numero("  Intervalo entre mediciones: ", valor_minimo=0.0001)
            if intervalo is None:
                continue
            
            tabla = generar_tabla_desintegracion(N0, k, tiempo_total, intervalo)
            mostrar_tabla(tabla, N0, k)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "e":
            break
        else:
            print("\n❌ Opción inválida. Seleccione a, b, c, d o e.")
            input("Presione ENTER para continuar...")


def opcion_generar_tabla():
    """Maneja la opción 5: Generar tabla de desintegración."""
    # Variables para almacenar datos calculados
    N0 = None
    k = None
    t_media = None
    
    opciones_submenu = [
        ("a", "Generar tabla con nuevos datos"),
        ("b", "Generar tabla con diferente intervalo/tiempo"),
        ("c", "Calcular N en un tiempo específico"),
        ("d", "Calcular tiempo para alcanzar una cantidad"),
        ("e", "Regresar al menú principal")
    ]
    
    while True:
        mostrar_cabecera("OPCIÓN 5: TABLA DE DESINTEGRACIÓN")
        
        # Mostrar datos actuales si existen
        if N0 is not None:
            mostrar_datos_actuales(N0, k, t_media)
        
        mostrar_submenu(opciones_submenu)
        
        sub_opcion = input("\n👉 Seleccione una opción (a-e): ").strip().lower()
        
        if sub_opcion == "a":
            print("\n📝 Ingrese los datos:\n")
            N0 = solicitar_numero("  Cantidad inicial N0: ", valor_minimo=0)
            if N0 is None:
                continue
            
            k = solicitar_numero("  Constante k (positiva): ", valor_minimo=0.0000001)
            if k is None:
                continue
            
            t_media = calcular_media_vida(k)
            
            tiempo_total = solicitar_numero("  Tiempo total a simular: ", valor_minimo=0)
            if tiempo_total is None:
                continue
            
            intervalo = solicitar_numero("  Intervalo entre mediciones: ", valor_minimo=0.0001)
            if intervalo is None:
                continue
            
            tabla = generar_tabla_desintegracion(N0, k, tiempo_total, intervalo)
            mostrar_tabla(tabla, N0, k)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "b":
            if N0 is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            tiempo_total = solicitar_numero("  Tiempo total a simular: ", valor_minimo=0)
            if tiempo_total is None:
                continue
            
            intervalo = solicitar_numero("  Intervalo entre mediciones: ", valor_minimo=0.0001)
            if intervalo is None:
                continue
            
            tabla = generar_tabla_desintegracion(N0, k, tiempo_total, intervalo)
            mostrar_tabla(tabla, N0, k)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "c":
            if N0 is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            t = solicitar_numero("  Tiempo t: ", valor_minimo=0)
            if t is None:
                continue
            
            N = calcular_N_en_tiempo_t(N0, k, t)
            mostrar_resultado_N(t, N, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "d":
            if N0 is None:
                print("\n❌ Primero debe ingresar datos (opción a)")
                input("Presione ENTER para continuar...")
                continue
            
            print(f"\n📝 Usando: N0={formatear_numero(N0)}, k={formatear_numero(k, 6)}")
            N_objetivo = solicitar_numero("  Cantidad objetivo N: ", valor_minimo=0, valor_maximo=N0)
            if N_objetivo is None:
                continue
            
            t = calcular_tiempo_t(N0, N_objetivo, k)
            mostrar_resultado_tiempo(t, N_objetivo, N0)
            input("\nPresione ENTER para continuar...")
            
        elif sub_opcion == "e":
            break
        else:
            print("\n❌ Opción inválida. Seleccione a, b, c, d o e.")
            input("Presione ENTER para continuar...")
