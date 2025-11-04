/* =====================================================================
   NEWTON.JS - JavaScript para la aplicación de Ley de Enfriamiento de Newton
   ===================================================================== */

// Estado global para mantener datos entre cálculos
let estadoGlobal = {
    temperatura: { Tm: null, C: null, K: null },
    tiempo: { Tm: null, C: null, K: null },
    k: { K: null, C: null, Tm: null, T0: null },
    tabla: { Tm: null, C: null, K: null }
};

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initForms();
    initBotonesUsar();
});

// =====================================================================
// SISTEMA DE PESTAÑAS
// =====================================================================

function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.dataset.tab;
            
            // Remover clase active de todos los botones y paneles
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanels.forEach(panel => panel.classList.remove('active'));
            
            // Agregar clase active al botón y panel seleccionado
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Inicializar formularios
function initForms() {
    // Formulario: Calcular Temperatura
    document.getElementById('form-calcular-temp').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            Tm: parseFloat(document.getElementById('temp-Tm').value),
            C: parseFloat(document.getElementById('temp-C').value),
            K: parseFloat(document.getElementById('temp-K').value),
            t: parseFloat(document.getElementById('temp-t').value)
        };
        
        // Guardar datos en estado global
        estadoGlobal.temperatura = { Tm: data.Tm, C: data.C, K: data.K };
        
        await calcularTemperatura(data);
    });
    
    // Formulario: Calcular Tiempo
    document.getElementById('form-calcular-tiempo').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            Tm: parseFloat(document.getElementById('tiempo-Tm').value),
            C: parseFloat(document.getElementById('tiempo-C').value),
            K: parseFloat(document.getElementById('tiempo-K').value),
            T_objetivo: parseFloat(document.getElementById('tiempo-T-objetivo').value)
        };
        
        // Guardar datos en estado global
        estadoGlobal.tiempo = { Tm: data.Tm, C: data.C, K: data.K };
        
        await calcularTiempo(data);
    });
    
    // Formulario: Calcular K
    document.getElementById('form-calcular-k').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            T0: parseFloat(document.getElementById('k-T0').value),
            Tm: parseFloat(document.getElementById('k-Tm').value),
            T_en_t: parseFloat(document.getElementById('k-T-en-t').value),
            t: parseFloat(document.getElementById('k-t').value)
        };
        
        await calcularK(data);
    });
    
    // Formulario: Generar Tabla
    document.getElementById('form-generar-tabla').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            Tm: parseFloat(document.getElementById('tabla-Tm').value),
            C: parseFloat(document.getElementById('tabla-C').value),
            K: parseFloat(document.getElementById('tabla-K').value),
            tiempo_total: parseFloat(document.getElementById('tabla-tiempo-total').value),
            intervalo: parseFloat(document.getElementById('tabla-intervalo').value)
        };
        
        // Guardar datos en estado global
        estadoGlobal.tabla = { Tm: data.Tm, C: data.C, K: data.K };
        
        await generarTabla(data);
    });
}

// Función: Calcular Temperatura
async function calcularTemperatura(data) {
    const resultadoDiv = document.getElementById('resultado-temp');
    const submitBtn = document.querySelector('#form-calcular-temp button[type="submit"]');
    
    try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Calculando... <span class="loading"></span>';
        
        const response = await fetch('/api/calcular-temperatura', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.exito) {
            resultadoDiv.className = 'resultado success';
            resultadoDiv.innerHTML = `
                <h3>✅ Resultado</h3>
                <p class="resultado-valor">
                    Temperatura después de ${result.tiempo} minutos: ${result.temperatura}°C
                </p>
                <p class="formula-resultado">${result.formula}</p>
                <button onclick="usarValoresTemperatura()" class="btn btn-secondary" style="margin-top: 10px;">
                    📋 Usar estos valores en otro cálculo
                </button>
            `;
        } else {
            mostrarError(resultadoDiv, result.error);
        }
    } catch (error) {
        mostrarError(resultadoDiv, 'Error de conexión con el servidor');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Calcular';
        resultadoDiv.classList.remove('hidden');
    }
}

// Función: Calcular Tiempo
async function calcularTiempo(data) {
    const resultadoDiv = document.getElementById('resultado-tiempo');
    const submitBtn = document.querySelector('#form-calcular-tiempo button[type="submit"]');
    
    try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Calculando... <span class="loading"></span>';
        
        const response = await fetch('/api/calcular-tiempo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.exito) {
            resultadoDiv.className = 'resultado success';
            resultadoDiv.innerHTML = `
                <h3>✅ Resultado</h3>
                <p class="resultado-valor">
                    Tiempo necesario: ${result.tiempo} minutos (${result.tiempo_horas} horas)
                </p>
                <p>Para alcanzar la temperatura objetivo de ${result.temperatura_objetivo}°C</p>
                <button onclick="usarValoresTiempo()" class="btn btn-secondary" style="margin-top: 10px;">
                    📋 Usar estos valores en otro cálculo
                </button>
            `;
        } else {
            if (result.infinito) {
                resultadoDiv.className = 'resultado error';
                resultadoDiv.innerHTML = `
                    <h3>⚠️ Advertencia</h3>
                    <p>${result.error}</p>
                `;
            } else {
                mostrarError(resultadoDiv, result.error);
            }
        }
    } catch (error) {
        mostrarError(resultadoDiv, 'Error de conexión con el servidor');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Calcular';
        resultadoDiv.classList.remove('hidden');
    }
}

// Función: Calcular K
async function calcularK(data) {
    const resultadoDiv = document.getElementById('resultado-k');
    const submitBtn = document.querySelector('#form-calcular-k button[type="submit"]');
    
    try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Calculando... <span class="loading"></span>';
        
        const response = await fetch('/api/calcular-k', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.exito) {
            // Guardar en estado global
            estadoGlobal.k = { K: result.K, C: result.C, Tm: result.Tm, T0: result.T0 };
            
            let iconoProceso = '';
            if (result.tipo_proceso === 'enfriamiento') {
                iconoProceso = '📉';
            } else if (result.tipo_proceso === 'calentamiento') {
                iconoProceso = '📈';
            } else {
                iconoProceso = '➡️';
            }
            
            resultadoDiv.className = 'resultado success';
            resultadoDiv.innerHTML = `
                <h3>✅ Resultado</h3>
                <p><strong>Constante K:</strong> <span class="resultado-valor">${result.K}</span> (1/min)</p>
                <p><strong>Constante C:</strong> ${result.C} °C</p>
                <p class="formula-resultado">${result.formula}</p>
                <p>${iconoProceso} <strong>Tipo de proceso:</strong> ${result.tipo_proceso}</p>
                <p>✓ Verificación en t=${result.t_verificacion} min: T = ${result.T_verificacion}°C</p>
                <button onclick="usarValoresK()" class="btn btn-secondary" style="margin-top: 10px;">
                    📋 Usar estos valores en otro cálculo
                </button>
            `;
        } else {
            mostrarError(resultadoDiv, result.error);
        }
    } catch (error) {
        mostrarError(resultadoDiv, 'Error de conexión con el servidor');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Calcular';
        resultadoDiv.classList.remove('hidden');
    }
}

// Función: Generar Tabla
async function generarTabla(data) {
    const resultadoDiv = document.getElementById('resultado-tabla');
    const submitBtn = document.querySelector('#form-generar-tabla button[type="submit"]');
    
    try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Generando... <span class="loading"></span>';
        
        const response = await fetch('/api/generar-tabla', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.exito) {
            // Determinar tipo de proceso
            const T0 = result.Tm + result.C;
            let tipoProceso = '';
            let iconoProceso = '';
            
            if (result.K < 0) {
                tipoProceso = 'Enfriamiento';
                iconoProceso = '📉';
            } else if (result.K > 0) {
                tipoProceso = 'Calentamiento';
                iconoProceso = '📈';
            } else {
                tipoProceso = 'Temperatura constante';
                iconoProceso = '➡️';
            }
            
            let tablaHTML = `
                <h3>📊 Tabla y Gráfico de ${tipoProceso}</h3>
                
                <div class="info-box" style="background: #f1f5f9; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <h4 style="margin: 0 0 10px 0; color: #1e293b;">📋 Datos del Proceso</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
                        <div><strong>Temperatura inicial (T₀):</strong> ${T0.toFixed(2)}°C</div>
                        <div><strong>Temperatura ambiente (Tₘ):</strong> ${result.Tm}°C</div>
                        <div><strong>Constante C:</strong> ${result.C}</div>
                        <div><strong>Constante K:</strong> ${result.K} (1/min)</div>
                        <div><strong>Tipo de proceso:</strong> ${iconoProceso} ${tipoProceso}</div>
                        <div><strong>Puntos de datos:</strong> ${result.num_puntos}</div>
                    </div>
                </div>
                
                <!-- Gráfico -->
                <div class="chart-container" style="position: relative; height: 400px; margin-bottom: 30px;">
                    <canvas id="grafico-temperatura"></canvas>
                </div>
                
                <!-- Tabla -->
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Tiempo (min)</th>
                                <th>Temperatura (°C)</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            result.tabla.forEach(fila => {
                tablaHTML += `
                    <tr>
                        <td>${fila.tiempo}</td>
                        <td>${fila.temperatura}</td>
                    </tr>
                `;
            });
            
            tablaHTML += `
                        </tbody>
                    </table>
                </div>
            `;
            
            resultadoDiv.className = 'resultado success';
            resultadoDiv.innerHTML = tablaHTML;
            
            // Crear el gráfico después de insertar el HTML
            crearGrafico(result.tabla, result.Tm, result.C, result.K, T0, tipoProceso);
            
        } else {
            mostrarError(resultadoDiv, result.error);
        }
    } catch (error) {
        mostrarError(resultadoDiv, 'Error de conexión con el servidor');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Generar Tabla';
        resultadoDiv.classList.remove('hidden');
    }
}

// Variable global para almacenar la instancia del gráfico
let graficoActual = null;

// Función para crear el gráfico con Chart.js
function crearGrafico(datos, Tm, C, K, T0, tipoProceso) {
    const ctx = document.getElementById('grafico-temperatura');
    
    if (!ctx) {
        console.error('Canvas no encontrado');
        return;
    }
    
    // Destruir gráfico anterior si existe
    if (graficoActual) {
        graficoActual.destroy();
    }
    
    // Extraer tiempos y temperaturas
    const tiempos = datos.map(fila => parseFloat(fila.tiempo));
    const temperaturas = datos.map(fila => parseFloat(fila.temperatura));
    
    // Determinar color según tipo de proceso (Tema Oscuro)
    let colorLinea = '#3b82f6';
    let colorFondo = 'rgba(59, 130, 246, 0.15)';
    
    if (K < 0) {
        colorLinea = '#06b6d4'; // Cyan para enfriamiento
        colorFondo = 'rgba(6, 182, 212, 0.15)';
    } else if (K > 0) {
        colorLinea = '#f59e0b'; // Ámbar para calentamiento
        colorFondo = 'rgba(245, 158, 11, 0.15)';
    }
    
    graficoActual = new Chart(ctx, {
        type: 'line',
        data: {
            labels: tiempos,
            datasets: [
                {
                    label: 'Temperatura (°C)',
                    data: temperaturas,
                    borderColor: colorLinea,
                    backgroundColor: colorFondo,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    pointBackgroundColor: colorLinea,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: colorLinea,
                    pointHoverBorderWidth: 3
                },
                {
                    label: 'Temperatura ambiente (Tₘ)',
                    data: tiempos.map(() => Tm),
                    borderColor: '#94a3b8',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [10, 5],
                    fill: false,
                    pointRadius: 0,
                    pointHoverRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        padding: 15,
                        font: {
                            size: 13,
                            family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
                        },
                        usePointStyle: true,
                        pointStyle: 'circle',
                        color: '#cbd5e1'
                    }
                },
                title: {
                    display: true,
                    text: `Curva de ${tipoProceso} - Ley de Newton`,
                    font: {
                        size: 18,
                        weight: 'bold',
                        family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    },
                    color: '#cbd5e1'
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    padding: 12,
                    cornerRadius: 8,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    displayColors: true,
                    borderColor: '#334155',
                    borderWidth: 1,
                    callbacks: {
                        title: function(context) {
                            return `⏱️ Tiempo: ${context[0].label} minutos`;
                        },
                        label: function(context) {
                            const label = context.dataset.label || '';
                            const value = context.parsed.y.toFixed(2);
                            
                            if (label.includes('Temperatura (')) {
                                return `🌡️ ${label}: ${value}°C`;
                            } else {
                                return `${label}: ${value}°C`;
                            }
                        },
                        afterBody: function(context) {
                            // Agregar información adicional
                            if (context[0].datasetIndex === 0) {
                                const tiempo = parseFloat(context[0].label);
                                const temp = parseFloat(context[0].parsed.y);
                                const diferencia = (temp - Tm).toFixed(2);
                                
                                return [
                                    '',
                                    `📊 Datos del proceso:`,
                                    `T₀ = ${T0.toFixed(2)}°C`,
                                    `Tₘ = ${Tm}°C`,
                                    `K = ${K} (1/min)`,
                                    `C = ${C}`,
                                    '',
                                    `Diferencia con Tₘ: ${diferencia}°C`
                                ];
                            }
                            return [];
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '⏱️ Tiempo (minutos)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        padding: 10,
                        color: '#cbd5e1'
                    },
                    grid: {
                        color: 'rgba(51, 65, 85, 0.5)',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        },
                        color: '#94a3b8'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '🌡️ Temperatura (°C)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        padding: 10,
                        color: '#cbd5e1'
                    },
                    grid: {
                        color: 'rgba(51, 65, 85, 0.5)',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        },
                        color: '#94a3b8',
                        callback: function(value) {
                            return value.toFixed(1) + '°C';
                        }
                    }
                }
            }
        }
    });
}

// Función auxiliar para mostrar errores
function mostrarError(elemento, mensaje) {
    elemento.className = 'resultado error';
    elemento.innerHTML = `
        <h3>❌ Error</h3>
        <p>${mensaje}</p>
    `;
}

// =====================================================================
// FUNCIONALIDAD: USAR DATOS CALCULADOS
// =====================================================================

function initBotonesUsar() {
    // Crear botones "Usar estos valores" dinámicamente después de cada resultado
    
    // No necesitamos crear botones aquí, los crearemos después de cada cálculo exitoso
}

// Función para usar valores de K calculado en otras pestañas
function usarValoresK() {
    if (estadoGlobal.k.K === null) {
        mostrarModal('⚠️ Error', 'Primero debes calcular la constante K', 'warning');
        return;
    }
    
    // Mostrar modal de selección
    mostrarModalOpciones(
        '¿Dónde quieres usar estos valores?',
        'Copiar Tm, C y K calculados a otra pestaña',
        [
            { texto: '🌡️ Calcular Temperatura', valor: 'temp' },
            { texto: '⏱️ Calcular Tiempo', valor: 'tiempo' },
            { texto: '📊 Generar Tabla', valor: 'tabla' }
        ],
        (opcion) => {
            if (opcion === 'temp') {
                document.getElementById('temp-Tm').value = estadoGlobal.k.Tm;
                document.getElementById('temp-C').value = estadoGlobal.k.C;
                document.getElementById('temp-K').value = estadoGlobal.k.K;
                cambiarTab('calcular-temp');
                mostrarNotificacion('✅ Valores copiados a "Calcular Temperatura"');
            } else if (opcion === 'tiempo') {
                document.getElementById('tiempo-Tm').value = estadoGlobal.k.Tm;
                document.getElementById('tiempo-C').value = estadoGlobal.k.C;
                document.getElementById('tiempo-K').value = estadoGlobal.k.K;
                cambiarTab('calcular-tiempo');
                mostrarNotificacion('✅ Valores copiados a "Calcular Tiempo"');
            } else if (opcion === 'tabla') {
                document.getElementById('tabla-Tm').value = estadoGlobal.k.Tm;
                document.getElementById('tabla-C').value = estadoGlobal.k.C;
                document.getElementById('tabla-K').value = estadoGlobal.k.K;
                cambiarTab('generar-tabla');
                mostrarNotificacion('✅ Valores copiados a "Generar Tabla"');
            }
        }
    );
}

// Función para usar valores de temperatura en otras pestañas
function usarValoresTemperatura() {
    if (estadoGlobal.temperatura.Tm === null) {
        mostrarModal('⚠️ Error', 'Primero debes calcular una temperatura', 'warning');
        return;
    }
    
    mostrarModalOpciones(
        '¿Dónde quieres usar estos valores?',
        'Copiar Tm, C y K a otra pestaña',
        [
            { texto: '⏱️ Calcular Tiempo', valor: 'tiempo' },
            { texto: '📊 Generar Tabla', valor: 'tabla' }
        ],
        (opcion) => {
            if (opcion === 'tiempo') {
                document.getElementById('tiempo-Tm').value = estadoGlobal.temperatura.Tm;
                document.getElementById('tiempo-C').value = estadoGlobal.temperatura.C;
                document.getElementById('tiempo-K').value = estadoGlobal.temperatura.K;
                cambiarTab('calcular-tiempo');
                mostrarNotificacion('✅ Valores copiados a "Calcular Tiempo"');
            } else if (opcion === 'tabla') {
                document.getElementById('tabla-Tm').value = estadoGlobal.temperatura.Tm;
                document.getElementById('tabla-C').value = estadoGlobal.temperatura.C;
                document.getElementById('tabla-K').value = estadoGlobal.temperatura.K;
                cambiarTab('generar-tabla');
                mostrarNotificacion('✅ Valores copiados a "Generar Tabla"');
            }
        }
    );
}

// Función para usar valores de tiempo en otras pestañas
function usarValoresTiempo() {
    if (estadoGlobal.tiempo.Tm === null) {
        mostrarModal('⚠️ Error', 'Primero debes calcular un tiempo', 'warning');
        return;
    }
    
    mostrarModalOpciones(
        '¿Dónde quieres usar estos valores?',
        'Copiar Tm, C y K a otra pestaña',
        [
            { texto: '🌡️ Calcular Temperatura', valor: 'temp' },
            { texto: '📊 Generar Tabla', valor: 'tabla' }
        ],
        (opcion) => {
            if (opcion === 'temp') {
                document.getElementById('temp-Tm').value = estadoGlobal.tiempo.Tm;
                document.getElementById('temp-C').value = estadoGlobal.tiempo.C;
                document.getElementById('temp-K').value = estadoGlobal.tiempo.K;
                cambiarTab('calcular-temp');
                mostrarNotificacion('✅ Valores copiados a "Calcular Temperatura"');
            } else if (opcion === 'tabla') {
                document.getElementById('tabla-Tm').value = estadoGlobal.tiempo.Tm;
                document.getElementById('tabla-C').value = estadoGlobal.tiempo.C;
                document.getElementById('tabla-K').value = estadoGlobal.tiempo.K;
                cambiarTab('generar-tabla');
                mostrarNotificacion('✅ Valores copiados a "Generar Tabla"');
            }
        }
    );
}

// Función auxiliar para cambiar de pestaña programáticamente
function cambiarTab(tabId) {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');
    
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabPanels.forEach(panel => panel.classList.remove('active'));
    
    const targetButton = document.querySelector(`[data-tab="${tabId}"]`);
    const targetPanel = document.getElementById(tabId);
    
    if (targetButton && targetPanel) {
        targetButton.classList.add('active');
        targetPanel.classList.add('active');
    }
}

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje) {
    // Crear elemento de notificación
    const notif = document.createElement('div');
    notif.className = 'notificacion';
    notif.textContent = mensaje;
    notif.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(71, 85, 105, 0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        font-weight: 500;
    `;
    
    document.body.appendChild(notif);
    
    // Eliminar después de 3 segundos
    setTimeout(() => {
        notif.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}

// =====================================================================
// SISTEMA DE MODALES MODERNOS
// =====================================================================

// Modal simple de información/advertencia/error
function mostrarModal(titulo, mensaje, tipo = 'info') {
    // Crear overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(30, 41, 59, 0.6);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        animation: fadeIn 0.2s ease-out;
        backdrop-filter: blur(4px);
    `;
    
    // Determinar color según tipo (Paleta gris/azulado)
    let iconoColor = '#475569'; // info
    let icono = 'ℹ️';
    
    if (tipo === 'warning') {
        iconoColor = '#0284c7';
        icono = '⚠️';
    } else if (tipo === 'error') {
        iconoColor = '#94a3b8';
        icono = '❌';
    } else if (tipo === 'success') {
        iconoColor = '#0891b2';
        icono = '✅';
    }
    
    // Crear modal
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.cssText = `
        background: white;
        border-radius: 12px;
        padding: 30px;
        max-width: 500px;
        width: 90%;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        animation: slideUp 0.3s ease-out;
    `;
    
    modal.innerHTML = `
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span style="font-size: 2rem; margin-right: 15px;">${icono}</span>
            <h2 style="margin: 0; color: ${iconoColor};">${titulo}</h2>
        </div>
        <p style="color: #64748b; margin-bottom: 25px; line-height: 1.6;">${mensaje}</p>
        <div style="display: flex; justify-content: flex-end;">
            <button class="btn btn-primary" onclick="cerrarModal(this)">Entendido</button>
        </div>
    `;
    
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    // Cerrar al hacer clic en el overlay
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            cerrarModal(overlay);
        }
    });
}

// Modal con opciones para seleccionar
function mostrarModalOpciones(titulo, subtitulo, opciones, callback) {
    // Crear overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(30, 41, 59, 0.6);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        animation: fadeIn 0.2s ease-out;
        backdrop-filter: blur(4px);
    `;
    
    // Crear modal
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.cssText = `
        background: #1e293b;
        border-radius: 12px;
        padding: 30px;
        max-width: 500px;
        width: 90%;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        animation: slideUp 0.3s ease-out;
    `;
    
    // Crear botones de opciones
    let botonesHTML = '';
    opciones.forEach(opcion => {
        botonesHTML += `
            <button class="modal-option-btn" data-valor="${opcion.valor}">
                ${opcion.texto}
            </button>
        `;
    });
    
    modal.innerHTML = `
        <h2 style="margin: 0 0 10px 0; color: #f1f5f9;">${titulo}</h2>
        <p style="color: #94a3b8; margin-bottom: 25px;">${subtitulo}</p>
        <div class="modal-options">
            ${botonesHTML}
        </div>
        <div style="display: flex; justify-content: flex-end; margin-top: 20px;">
            <button class="btn" style="background: #475569; color: white;" onclick="cerrarModal(this)">
                Cancelar
            </button>
        </div>
    `;
    
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    // Agregar eventos a los botones de opción
    modal.querySelectorAll('.modal-option-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const valor = btn.getAttribute('data-valor');
            cerrarModal(overlay);
            if (callback) callback(valor);
        });
    });
    
    // Cerrar al hacer clic en el overlay
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            cerrarModal(overlay);
        }
    });
}

// Función para cerrar modal
function cerrarModal(elemento) {
    // Encontrar el overlay más cercano
    const overlay = elemento.closest('.modal-overlay') || elemento;
    
    if (overlay) {
        overlay.style.animation = 'fadeOut 0.2s ease-out';
        setTimeout(() => overlay.remove(), 200);
    }
}
