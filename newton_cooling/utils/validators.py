"""
=====================================================================
    VALIDATORS - Validaciones de entrada
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
