"""
=====================================================================
    APP - Aplicación Web Flask
=====================================================================
    APLICACIÓN WEB: LEY DE ENFRIAMIENTO DE NEWTON
    
    Versión web de la aplicación de consola.
    
    Autor: Neider Duvan Guindigua Machoa
    Fecha: 3 de Noviembre de 2025
=====================================================================
"""

from flask import Flask, render_template, request, jsonify
from newton_cooling.core.calculations import (
    calcular_temperatura,
    calcular_tiempo_para_temperatura,
    calcular_constante_K,
    calcular_constante_C,
    generar_tabla_enfriamiento
)
from desintegracion_radiactiva.core.calculations import (
    calcular_constante_k,
    calcular_N_en_tiempo_t,
    calcular_tiempo_t,
    calcular_N0,
    calcular_media_vida,
    calcular_k_desde_datos,
    generar_tabla_desintegracion
)

app = Flask(__name__)


@app.route('/')
def index():
    """Página principal - Panel de bienvenida."""
    return render_template('index.html')


@app.route('/newton')
def newton():
    """Página de Ley de Enfriamiento de Newton."""
    return render_template('newton.html')


@app.route('/radiactiva')
def radiactiva():
    """Página de Desintegración Radiactiva."""
    return render_template('radiactiva.html')


@app.route('/api/calcular-temperatura', methods=['POST'])
def api_calcular_temperatura():
    """
    Endpoint para calcular temperatura en un tiempo específico.
    
    Espera: {Tm, C, K, t}
    Retorna: {temperatura, exito}
    """
    try:
        data = request.get_json()
        Tm = float(data['Tm'])
        C = float(data['C'])
        K = float(data['K'])
        t = float(data['t'])
        
        if t < 0:
            return jsonify({
                'exito': False,
                'error': 'El tiempo debe ser mayor o igual a 0'
            }), 400
        
        temperatura = calcular_temperatura(Tm, C, K, t)
        
        return jsonify({
            'exito': True,
            'temperatura': round(temperatura, 2),
            'tiempo': t,
            'formula': f"T({t}) = {Tm} + {C} * e^({K}*{t})"
        })
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({
            'exito': False,
            'error': 'Datos inválidos. Por favor verifica los valores ingresados.'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error en el cálculo: {str(e)}'
        }), 500


@app.route('/api/calcular-tiempo', methods=['POST'])
def api_calcular_tiempo():
    """
    Endpoint para calcular tiempo necesario para alcanzar temperatura objetivo.
    
    Espera: {Tm, C, K, T_objetivo}
    Retorna: {tiempo, exito}
    """
    try:
        data = request.get_json()
        Tm = float(data['Tm'])
        C = float(data['C'])
        K = float(data['K'])
        T_objetivo = float(data['T_objetivo'])
        
        tiempo = calcular_tiempo_para_temperatura(Tm, C, K, T_objetivo)
        
        if tiempo is None:
            return jsonify({
                'exito': False,
                'error': 'No es posible alcanzar esa temperatura con estos parámetros.'
            })
        elif tiempo == float('inf'):
            return jsonify({
                'exito': False,
                'error': 'El objeto nunca alcanzará exactamente esa temperatura.',
                'infinito': True
            })
        else:
            return jsonify({
                'exito': True,
                'tiempo': round(tiempo, 2),
                'tiempo_horas': round(tiempo / 60, 2),
                'temperatura_objetivo': T_objetivo
            })
    except (KeyError, ValueError, TypeError):
        return jsonify({
            'exito': False,
            'error': 'Datos inválidos. Por favor verifica los valores ingresados.'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error en el cálculo: {str(e)}'
        }), 500


@app.route('/api/calcular-k', methods=['POST'])
def api_calcular_k():
    """
    Endpoint para calcular constante K con datos conocidos.
    
    Espera: {T0, Tm, T_en_t, t}
    Retorna: {K, C, exito}
    """
    try:
        data = request.get_json()
        T0 = float(data['T0'])
        Tm = float(data['Tm'])
        T_en_t = float(data['T_en_t'])
        t = float(data['t'])
        
        if t <= 0:
            return jsonify({
                'exito': False,
                'error': 'El tiempo debe ser mayor a 0'
            }), 400
        
        K, C = calcular_constante_K(T0, Tm, T_en_t, t)
        
        if K is None:
            return jsonify({
                'exito': False,
                'error': 'No es posible calcular K con estos datos. Verifica que los datos sean consistentes.'
            })
        
        # Verificación
        T_verificacion = calcular_temperatura(Tm, C, K, t)
        
        tipo_proceso = ""
        if K < 0:
            tipo_proceso = "enfriamiento"
        elif K > 0:
            tipo_proceso = "calentamiento"
        else:
            tipo_proceso = "temperatura constante"
        
        return jsonify({
            'exito': True,
            'K': round(K, 6),
            'C': round(C, 2),
            'Tm': Tm,
            'T0': T0,
            'T_verificacion': round(T_verificacion, 2),
            't_verificacion': t,
            'tipo_proceso': tipo_proceso,
            'formula': f"T(t) = {Tm} + {round(C, 2)} * e^({round(K, 6)}*t)"
        })
    except (KeyError, ValueError, TypeError):
        return jsonify({
            'exito': False,
            'error': 'Datos inválidos. Por favor verifica los valores ingresados.'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error en el cálculo: {str(e)}'
        }), 500


@app.route('/api/calcular-c', methods=['POST'])
def api_calcular_c():
    """
    Endpoint para calcular constante C.
    
    Espera: {T_inicial, Tm}
    Retorna: {C, interpretacion, exito}
    """
    try:
        data = request.get_json()
        T_inicial = float(data['T_inicial'])
        Tm = float(data['Tm'])
        
        C = calcular_constante_C(T_inicial, Tm)
        
        # Interpretación del resultado
        if C > 0:
            interpretacion = {
                'tipo': 'positivo',
                'descripcion': 'El objeto está más caliente que el ambiente',
                'comportamiento': 'Con K negativo, el objeto se enfriará hacia Tm'
            }
        elif C < 0:
            interpretacion = {
                'tipo': 'negativo',
                'descripcion': 'El objeto está más frío que el ambiente',
                'comportamiento': 'Con K positivo, el objeto se calentará hacia Tm'
            }
        else:
            interpretacion = {
                'tipo': 'cero',
                'descripcion': 'El objeto ya está a la temperatura ambiente',
                'comportamiento': 'La temperatura no cambiará con el tiempo'
            }
        
        return jsonify({
            'exito': True,
            'C': round(C, 2),
            'T_inicial': T_inicial,
            'Tm': Tm,
            'interpretacion': interpretacion,
            'formula': f"C = {T_inicial} - {Tm} = {round(C, 2)}"
        })
    except (KeyError, ValueError, TypeError):
        return jsonify({
            'exito': False,
            'error': 'Datos inválidos. Por favor verifica los valores ingresados.'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error en el cálculo: {str(e)}'
        }), 500


@app.route('/api/generar-tabla', methods=['POST'])
def api_generar_tabla():
    """
    Endpoint para generar tabla de enfriamiento.
    
    Espera: {Tm, C, K, tiempo_total, intervalo}
    Retorna: {tabla, exito}
    """
    try:
        data = request.get_json()
        Tm = float(data['Tm'])
        C = float(data['C'])
        K = float(data['K'])
        tiempo_total = float(data['tiempo_total'])
        intervalo = float(data['intervalo'])
        
        if tiempo_total <= 0:
            return jsonify({
                'exito': False,
                'error': 'El tiempo total debe ser mayor a 0'
            }), 400
        
        if intervalo <= 0:
            return jsonify({
                'exito': False,
                'error': 'El intervalo debe ser mayor a 0'
            }), 400
        
        # Limitar el número de puntos para evitar respuestas muy grandes
        num_puntos = int(tiempo_total / intervalo) + 1
        if num_puntos > 1000:
            return jsonify({
                'exito': False,
                'error': f'Demasiados puntos de datos ({num_puntos}). El máximo es 1000. Aumenta el intervalo o reduce el tiempo total.'
            }), 400
        
        tabla = generar_tabla_enfriamiento(Tm, C, K, tiempo_total, intervalo)
        
        # Convertir a formato JSON-friendly
        tabla_json = [
            {
                'tiempo': round(t, 2),
                'temperatura': round(temp, 2)
            }
            for t, temp in tabla
        ]
        
        return jsonify({
            'exito': True,
            'tabla': tabla_json,
            'Tm': Tm,
            'C': C,
            'K': K,
            'num_puntos': len(tabla_json)
        })
    except (KeyError, ValueError, TypeError):
        return jsonify({
            'exito': False,
            'error': 'Datos inválidos. Por favor verifica los valores ingresados.'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error en el cálculo: {str(e)}'
        }), 500


# =====================================================================
# API ENDPOINTS - DESINTEGRACIÓN RADIACTIVA
# =====================================================================

@app.route('/api/radiactiva/calcular-n', methods=['POST'])
def api_calcular_n():
    """
    Endpoint para calcular cantidad de sustancia en un tiempo específico.
    
    Espera: {N0, k, t}
    Retorna: {N, porcentaje, exito}
    """
    try:
        data = request.get_json()
        N0 = float(data['N0'])
        k = float(data['k'])
        t = float(data['t'])
        
        if t < 0:
            return jsonify({
                'exito': False,
                'error': 'El tiempo debe ser mayor o igual a 0'
            }), 400
        
        if N0 <= 0:
            return jsonify({
                'exito': False,
                'error': 'La cantidad inicial N0 debe ser mayor a 0'
            }), 400
        
        if k <= 0:
            return jsonify({
                'exito': False,
                'error': 'La constante k debe ser mayor a 0'
            }), 400
        
        N = calcular_N_en_tiempo_t(N0, k, t)
        porcentaje = (N / N0) * 100
        
        return jsonify({
            'exito': True,
            'N': round(N, 4),
            'porcentaje': round(porcentaje, 2),
            'N0': N0,
            't': t,
            'k': k,
            'formula': f"N({t}) = {N0} * e^(-{k}*{t})"
        })
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({
            'exito': False,
            'error': 'Datos inválidos. Por favor verifica los valores ingresados.'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error en el cálculo: {str(e)}'
        }), 500


@app.route('/api/radiactiva/calcular-tiempo', methods=['POST'])
def api_calcular_tiempo_radiactiva():
    """
    Endpoint para calcular tiempo necesario para llegar a una cantidad objetivo.
    
    Espera: {N0, N_objetivo, k}
    Retorna: {tiempo, exito}
    """
    try:
        data = request.get_json()
        N0 = float(data['N0'])
        N_objetivo = float(data['N_objetivo'])
        k = float(data['k'])
        
        if N0 <= 0:
            return jsonify({
                'exito': False,
                'error': 'La cantidad inicial N0 debe ser mayor a 0'
            }), 400
        
        if N_objetivo <= 0:
            return jsonify({
                'exito': False,
                'error': 'La cantidad objetivo debe ser mayor a 0'
            }), 400
        
        if k <= 0:
            return jsonify({
                'exito': False,
                'error': 'La constante k debe ser mayor a 0'
            }), 400
        
        tiempo = calcular_tiempo_t(N0, N_objetivo, k)
        
        if tiempo is None:
            return jsonify({
                'exito': False,
                'error': 'No es posible alcanzar esa cantidad con estos parámetros. La cantidad objetivo debe ser menor que N0.'
            })
        elif tiempo == float('inf'):
            return jsonify({
                'exito': False,
                'error': 'Se necesita tiempo infinito para alcanzar exactamente 0.',
                'infinito': True
            })
        else:
            porcentaje = (N_objetivo / N0) * 100
            
            return jsonify({
                'exito': True,
                'tiempo': round(tiempo, 4),
                'N_objetivo': N_objetivo,
                'porcentaje': round(porcentaje, 2),
                'N0': N0,
                'k': k
            })
    except (KeyError, ValueError, TypeError):
        return jsonify({
            'exito': False,
            'error': 'Datos inválidos. Por favor verifica los valores ingresados.'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error en el cálculo: {str(e)}'
        }), 500


@app.route('/api/radiactiva/calcular-k', methods=['POST'])
def api_calcular_k_radiactiva():
    """
    Endpoint para calcular constante k desde datos conocidos.
    
    Espera: {N0, N_en_t, t} o {t_media}
    Retorna: {k, t_media, exito}
    """
    try:
        data = request.get_json()
        
        # Opción 1: Calcular desde t_media
        if 't_media' in data:
            t_media = float(data['t_media'])
            
            if t_media <= 0:
                return jsonify({
                    'exito': False,
                    'error': 'La vida media debe ser mayor a 0'
                }), 400
            
            k = calcular_constante_k(t_media)
            
            return jsonify({
                'exito': True,
                'k': round(k, 6),
                't_media': t_media,
                'formula': f"k = ln(2) / {t_media} = {round(k, 6)}",
                'desde_t_media': True
            })
        
        # Opción 2: Calcular desde datos experimentales
        N0 = float(data['N0'])
        N_en_t = float(data['N_en_t'])
        t = float(data['t'])
        
        if N0 <= 0 or N_en_t <= 0 or t <= 0:
            return jsonify({
                'exito': False,
                'error': 'Todos los valores deben ser mayores a 0'
            }), 400
        
        if N_en_t > N0:
            return jsonify({
                'exito': False,
                'error': 'La cantidad en tiempo t debe ser menor o igual a N0'
            }), 400
        
        k, t_media = calcular_k_desde_datos(N0, N_en_t, t)
        
        if k is None:
            return jsonify({
                'exito': False,
                'error': 'No es posible calcular k con estos datos. Verifica que N en t sea menor que N0.'
            })
        
        # Verificación
        N_verificacion = calcular_N_en_tiempo_t(N0, k, t)
        porcentaje = (N_en_t / N0) * 100
        
        return jsonify({
            'exito': True,
            'k': round(k, 6),
            't_media': round(t_media, 4) if t_media != float('inf') else 'infinito',
            'N0': N0,
            'N_en_t': N_en_t,
            't': t,
            'porcentaje': round(porcentaje, 2),
            'N_verificacion': round(N_verificacion, 4),
            'formula': f"N(t) = {N0} * e^(-{round(k, 6)}*t)",
            'desde_t_media': False
        })
    except (KeyError, ValueError, TypeError):
        return jsonify({
            'exito': False,
            'error': 'Datos inválidos. Por favor verifica los valores ingresados.'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error en el cálculo: {str(e)}'
        }), 500


@app.route('/api/radiactiva/calcular-n0', methods=['POST'])
def api_calcular_n0():
    """
    Endpoint para calcular cantidad inicial N0.
    
    Espera: {N, k, t}
    Retorna: {N0, exito}
    """
    try:
        data = request.get_json()
        N = float(data['N'])
        k = float(data['k'])
        t = float(data['t'])
        
        if N < 0:
            return jsonify({
                'exito': False,
                'error': 'La cantidad N debe ser mayor o igual a 0'
            }), 400
        
        if k <= 0:
            return jsonify({
                'exito': False,
                'error': 'La constante k debe ser mayor a 0'
            }), 400
        
        if t < 0:
            return jsonify({
                'exito': False,
                'error': 'El tiempo debe ser mayor o igual a 0'
            }), 400
        
        N0 = calcular_N0(N, k, t)
        
        if N0 is None:
            return jsonify({
                'exito': False,
                'error': 'No es posible calcular N0 con estos parámetros.'
            })
        
        return jsonify({
            'exito': True,
            'N0': round(N0, 4),
            'N': N,
            'k': k,
            't': t,
            'formula': f"N0 = {N} * e^({k}*{t}) = {round(N0, 4)}"
        })
    except (KeyError, ValueError, TypeError):
        return jsonify({
            'exito': False,
            'error': 'Datos inválidos. Por favor verifica los valores ingresados.'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error en el cálculo: {str(e)}'
        }), 500


@app.route('/api/radiactiva/generar-tabla', methods=['POST'])
def api_generar_tabla_radiactiva():
    """
    Endpoint para generar tabla de desintegración.
    
    Espera: {N0, k, tiempo_total, intervalo}
    Retorna: {tabla, exito}
    """
    try:
        data = request.get_json()
        N0 = float(data['N0'])
        k = float(data['k'])
        tiempo_total = float(data['tiempo_total'])
        intervalo = float(data['intervalo'])
        
        if N0 <= 0:
            return jsonify({
                'exito': False,
                'error': 'La cantidad inicial N0 debe ser mayor a 0'
            }), 400
        
        if k <= 0:
            return jsonify({
                'exito': False,
                'error': 'La constante k debe ser mayor a 0'
            }), 400
        
        if tiempo_total <= 0:
            return jsonify({
                'exito': False,
                'error': 'El tiempo total debe ser mayor a 0'
            }), 400
        
        if intervalo <= 0:
            return jsonify({
                'exito': False,
                'error': 'El intervalo debe ser mayor a 0'
            }), 400
        
        # Limitar el número de puntos
        num_puntos = int(tiempo_total / intervalo) + 1
        if num_puntos > 1000:
            return jsonify({
                'exito': False,
                'error': f'Demasiados puntos de datos ({num_puntos}). El máximo es 1000. Aumenta el intervalo o reduce el tiempo total.'
            }), 400
        
        tabla = generar_tabla_desintegracion(N0, k, tiempo_total, intervalo)
        
        # Convertir a formato JSON-friendly
        tabla_json = [
            {
                'tiempo': round(t, 4),
                'N': round(N, 4),
                'porcentaje': round(porcentaje, 2)
            }
            for t, N, porcentaje in tabla
        ]
        
        # Calcular vida media para información adicional
        t_media = calcular_media_vida(k)
        
        return jsonify({
            'exito': True,
            'tabla': tabla_json,
            'N0': N0,
            'k': k,
            't_media': round(t_media, 4),
            'num_puntos': len(tabla_json)
        })
    except (KeyError, ValueError, TypeError):
        return jsonify({
            'exito': False,
            'error': 'Datos inválidos. Por favor verifica los valores ingresados.'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error en el cálculo: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
