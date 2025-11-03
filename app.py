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
    generar_tabla_enfriamiento
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
