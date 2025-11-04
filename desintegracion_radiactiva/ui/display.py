"""
=====================================================================
    DISPLAY - Funciones de visualización
=====================================================================
Funciones para mostrar información y resultados formateados.
=====================================================================
"""

from ..core.constants import LINE_WIDTH, SEPARATOR_CHAR, SUBSEPARATOR_CHAR


def formatear_numero(valor, decimales=4):
    """
    Formatea un número de manera inteligente.
    Usa notación normal para números razonables y científica para muy grandes/pequeños.
    
    Parámetros:
        valor (float): Número a formatear
        decimales (int): Cantidad de decimales
    
    Retorna:
        str: Número formateado
    """
    if valor == 0:
        return "0"
    
    abs_valor = abs(valor)
    
    # Usar notación normal para números entre 0.001 y 999999
    if 0.001 <= abs_valor < 1000000:
        # Para números muy cercanos a enteros, mostrar como entero
        if abs(valor - round(valor)) < 0.0001 and abs_valor < 10000:
            return f"{int(round(valor))}"
        # Para números decimales normales
        elif abs_valor >= 1:
            return f"{valor:.{decimales}f}".rstrip('0').rstrip('.')
        else:
            return f"{valor:.{decimales}f}"
    else:
        # Usar notación científica para números muy grandes o muy pequeños
        return f"{valor:.{decimales}e}"


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


def mostrar_datos_actuales(N0=None, k=None, t_media=None, info_adicional=None):
    """
    Muestra los datos actuales guardados.
    
    Parámetros:
        N0 (float): Cantidad inicial
        k (float): Constante de desintegración
        t_media (float): Media de vida
        info_adicional (str): Información adicional opcional
    """
    print("\n📌 DATOS ACTUALES:")
    if N0 is not None:
        print(f"   N0 = {formatear_numero(N0)}", end="")
    if k is not None:
        print(f" | k = {formatear_numero(k, 6)}", end="")
    if t_media is not None:
        print(f" | t_media = {formatear_numero(t_media)}", end="")
    print()
    
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


def mostrar_resultado_N(t, N, N0=None):
    """
    Muestra el resultado de un cálculo de N(t).
    
    Parámetros:
        t (float): Tiempo
        N (float): Cantidad calculada
        N0 (float): Cantidad inicial (opcional, para mostrar porcentaje)
    """
    print("\n" + SUBSEPARATOR_CHAR * LINE_WIDTH)
    print("📊 RESULTADO:")
    if N is None:
        print("   ❌ No es posible calcular con estos datos.")
    else:
        print(f"   Cantidad N después de t = {formatear_numero(t)}: N = {formatear_numero(N)}")
        if N0 is not None and N0 > 0:
            porcentaje = (N / N0) * 100
            print(f"   Porcentaje restante: {porcentaje:.2f}%")
            print(f"   Cantidad desintegrada: {formatear_numero(N0 - N)} ({100-porcentaje:.2f}%)")
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)


def mostrar_resultado_tiempo(t, N_objetivo, N0=None):
    """
    Muestra el resultado de un cálculo de tiempo.
    
    Parámetros:
        t (float): Tiempo calculado (puede ser None o inf)
        N_objetivo (float): Cantidad objetivo
        N0 (float): Cantidad inicial (opcional)
    """
    print("\n" + SUBSEPARATOR_CHAR * LINE_WIDTH)
    print("📊 RESULTADO:")
    if t is None:
        print("   ❌ No es posible calcular el tiempo con estos parámetros.")
        print("   Verifica que N esté entre 0 y N0.")
    elif t == float('inf'):
        print("   ⚠️  Tiempo infinito (la sustancia nunca llegará exactamente a N = 0)")
    elif t == 0:
        print("   ⚠️  Tiempo = 0 (N ya es igual a N0)")
    else:
        print(f"   Tiempo necesario: t = {formatear_numero(t)}")
        if t >= 60:
            print(f"   Equivalente a: {t/60:.2f} horas")
        if t >= 1440:
            print(f"   Equivalente a: {t/1440:.2f} días")
        if t >= 525600:
            print(f"   Equivalente a: {t/525600:.2f} años")
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)


def mostrar_resultado_k(k, t_media=None, N0=None, N=None, t=None):
    """
    Muestra el resultado del cálculo de k.
    
    Parámetros:
        k (float): Constante k calculada (puede ser None)
        t_media (float): Media de vida calculada (opcional)
        N0 (float): Cantidad inicial usada (opcional)
        N (float): Cantidad final usada (opcional)
        t (float): Tiempo usado (opcional)
    """
    print("\n" + SUBSEPARATOR_CHAR * LINE_WIDTH)
    print("📊 RESULTADO:")
    if k is None:
        print("   ❌ No es posible calcular k con estos datos.")
        print("   Verifica que los datos sean consistentes.")
    else:
        print(f"   Constante k = {formatear_numero(k, 6)} (unidad⁻¹)")
        if t_media is not None:
            print(f"   Media de vida (t_media) = {formatear_numero(t_media)}")
        
        print(f"\n   Fórmula completa: N(t) = N0 * e^(-{formatear_numero(k, 6)} * t)")
        
        if N0 is not None and N is not None and t is not None:
            print(f"\n   ✓ Verificación: N({formatear_numero(t)}) = {formatear_numero(N)}")
            porcentaje = (N/N0) * 100 if N0 > 0 else 0
            print(f"   ✓ Porcentaje restante: {porcentaje:.2f}%")
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)


def mostrar_resultado_N0(N0, N=None, t=None, k=None):
    """
    Muestra el resultado del cálculo de N0.
    
    Parámetros:
        N0 (float): Cantidad inicial calculada
        N (float): Cantidad usada (opcional)
        t (float): Tiempo usado (opcional)
        k (float): Constante usada (opcional)
    """
    print("\n" + SUBSEPARATOR_CHAR * LINE_WIDTH)
    print("📊 RESULTADO:")
    if N0 is None:
        print("   ❌ No es posible calcular N0 con estos datos.")
    else:
        print(f"   Cantidad inicial N0 = {formatear_numero(N0)}")
        if N is not None and N > 0:
            print(f"   Cantidad actual N = {formatear_numero(N)}")
            porcentaje = (N/N0) * 100
            print(f"   Porcentaje restante: {porcentaje:.2f}%")
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)


def mostrar_resultado_media_vida(t_media, k=None):
    """
    Muestra el resultado del cálculo de media de vida.
    
    Parámetros:
        t_media (float): Media de vida calculada
        k (float): Constante k usada (opcional)
    """
    print("\n" + SUBSEPARATOR_CHAR * LINE_WIDTH)
    print("📊 RESULTADO:")
    if t_media is None:
        print("   ❌ No es posible calcular la media de vida.")
    else:
        print(f"   Media de vida (t_media) = {formatear_numero(t_media)}")
        print(f"   En este tiempo, N = N0/2 (queda el 50%)")
        if k is not None:
            print(f"   Constante k = {formatear_numero(k, 6)}")
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)


def mostrar_tabla(tabla, N0, k):
    """
    Muestra una tabla de desintegración formateada.
    
    Parámetros:
        tabla (list): Lista de tuplas (tiempo, N, porcentaje)
        N0 (float): Cantidad inicial
        k (float): Constante de desintegración
    """
    print("\n" + SEPARATOR_CHAR * LINE_WIDTH)
    print(f"📊 TABLA DE DESINTEGRACIÓN - N(t) = {formatear_numero(N0)} * e^(-{formatear_numero(k, 6)}*t)")
    print(SEPARATOR_CHAR * LINE_WIDTH)
    print(f"{'Tiempo':>15} | {'Cantidad N':>20} | {'Porcentaje':>15}")
    print(SUBSEPARATOR_CHAR * LINE_WIDTH)
    
    for tiempo, N, porcentaje in tabla:
        print(f"{formatear_numero(tiempo):>15} | {formatear_numero(N):>20} | {porcentaje:>14.2f}%")
    
    print(SEPARATOR_CHAR * LINE_WIDTH)


def mostrar_informacion():
    """Muestra información detallada sobre la Desintegración Radiactiva."""
    mostrar_cabecera("INFORMACIÓN: DESINTEGRACIÓN RADIACTIVA")
    print("""
La desintegración radiactiva es el proceso por el cual un núcleo
atómico inestable pierde energía mediante la emisión de radiación.
La velocidad de desintegración es proporcional a la cantidad presente.

📐 ECUACIÓN DIFERENCIAL:
   dN/dt = -k * N

📐 SOLUCIÓN (FÓRMULA):
   N(t) = N0 * e^(-k*t)

📊 VARIABLES:
   • N(t):   Cantidad de sustancia en el tiempo t
   • N0:     Cantidad inicial de sustancia
   • k:      Constante de desintegración (positiva) (tiempo⁻¹)
   • t:      Tiempo transcurrido
   • t_media: Media de vida (cuando N = N0/2)

📐 RELACIONES IMPORTANTES:
   • k = ln(2) / t_media  ≈  0.693147 / t_media
   • t_media = ln(2) / k  ≈  0.693147 / k
   • t = ln(N0/N) / k     (tiempo para pasar de N0 a N)
   • N0 = N * e^(k*t)     (cantidad inicial desde N en tiempo t)

💡 EJEMPLOS DE MEDIA DE VIDA:
   • Carbono-14:     5,730 años
   • Uranio-238:     4,468 millones de años
   • Radio-226:      1,600 años
   • Yodo-131:       8.02 días
   • Tecnecio-99m:   6.01 horas

📝 APLICACIONES:
   • Datación por radiocarbono (arqueología)
   • Medicina nuclear (diagnóstico y tratamiento)
   • Generación de energía nuclear
   • Datación geológica
   • Seguridad y manejo de residuos radiactivos
""")
    input("\nPresione ENTER para continuar...")
