"""
=====================================================================
    VALIDATORS - Validadores de entrada
=====================================================================
Funciones para validar y solicitar datos del usuario.
=====================================================================
"""


def solicitar_numero(mensaje, valor_minimo=None, valor_maximo=None):
    """
    Solicita un número al usuario con validación.
    
    Parámetros:
        mensaje (str): Mensaje a mostrar al usuario
        valor_minimo (float): Valor mínimo permitido (opcional)
        valor_maximo (float): Valor máximo permitido (opcional)
    
    Retorna:
        float: Número válido ingresado por el usuario
    """
    while True:
        try:
            valor = float(input(mensaje))
            
            if valor_minimo is not None and valor < valor_minimo:
                print(f"  ❌ El valor debe ser mayor o igual a {valor_minimo}")
                continue
            
            if valor_maximo is not None and valor > valor_maximo:
                print(f"  ❌ El valor debe ser menor o igual a {valor_maximo}")
                if "N:" in mensaje or "cantidad" in mensaje.lower():
                    print(f"  💡 Recuerda: En desintegración, N (actual) ≤ N0 (inicial)")
                    print(f"     Si N0 es la cantidad inicial, N debe ser menor (la sustancia disminuye)")
                continue
            
            return valor
            
        except ValueError:
            print("  ❌ Por favor ingrese un número válido")
        except KeyboardInterrupt:
            print("\n\n❌ Operación cancelada por el usuario")
            return None


def solicitar_opcion(opciones_validas):
    """
    Solicita una opción del menú con validación.
    
    Parámetros:
        opciones_validas (list): Lista de opciones válidas (str)
    
    Retorna:
        str: Opción válida seleccionada
    """
    while True:
        opcion = input("\n👉 Seleccione una opción: ").strip().lower()
        
        if opcion in opciones_validas:
            return opcion
        else:
            opciones_texto = ", ".join(opciones_validas)
            print(f"❌ Opción inválida. Seleccione: {opciones_texto}")
