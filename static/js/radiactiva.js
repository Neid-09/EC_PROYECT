/* =====================================================================
   RADIACTIVA.JS - JavaScript para Desintegración Radiactiva
   ===================================================================== */

// Estado global para mantener datos entre cálculos
let estadoGlobal = {
    n: { N0: null, k: null },
    tiempo: { N0: null, k: null },
    k: { k: null, t_media: null },
    n0: { k: null },
    tabla: { N0: null, k: null }
};

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initForms();
    initBotonesUsar();
    initBotonesRapidos();
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

// =====================================================================
// INICIALIZAR FORMULARIOS
// =====================================================================

function initForms() {
    // Formulario: Calcular N(t)
    document.getElementById('form-calcular-n').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            N0: parseFloat(document.getElementById('n-N0').value),
            k: parseFloat(document.getElementById('n-k').value),
            t: parseFloat(document.getElementById('n-t').value)
        };
        
        // Guardar datos en estado global
        estadoGlobal.n = { N0: data.N0, k: data.k };
        
        await calcularN(data);
    });
    
    // Formulario: Calcular Tiempo
    document.getElementById('form-calcular-tiempo').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            N0: parseFloat(document.getElementById('tiempo-N0').value),
            N_objetivo: parseFloat(document.getElementById('tiempo-N-objetivo').value),
            k: parseFloat(document.getElementById('tiempo-k').value)
        };
        
        // Guardar datos en estado global
        estadoGlobal.tiempo = { N0: data.N0, k: data.k };
        
        await calcularTiempo(data);
    });
    
    // Formulario: Calcular K desde vida media
    document.getElementById('form-calcular-k-tmedia').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            t_media: parseFloat(document.getElementById('k-tmedia').value)
        };
        
        await calcularKDesdeTMedia(data);
    });
    
    // Formulario: Calcular K desde datos
    document.getElementById('form-calcular-k-datos').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            N0: parseFloat(document.getElementById('k-N0').value),
            N_en_t: parseFloat(document.getElementById('k-N-en-t').value),
            t: parseFloat(document.getElementById('k-t').value)
        };
        
        await calcularKDesdeDatos(data);
    });
    
    // Formulario: Calcular N0
    document.getElementById('form-calcular-n0').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            N: parseFloat(document.getElementById('n0-N').value),
            k: parseFloat(document.getElementById('n0-k').value),
            t: parseFloat(document.getElementById('n0-t').value)
        };
        
        // Guardar k en estado global
        estadoGlobal.n0 = { k: data.k };
        
        await calcularN0(data);
    });
    
    // Formulario: Generar Tabla
    document.getElementById('form-generar-tabla').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            N0: parseFloat(document.getElementById('tabla-N0').value),
            k: parseFloat(document.getElementById('tabla-k').value),
            tiempo_total: parseFloat(document.getElementById('tabla-tiempo-total').value),
            intervalo: parseFloat(document.getElementById('tabla-intervalo').value)
        };
        
        // Guardar datos en estado global
        estadoGlobal.tabla = { N0: data.N0, k: data.k };
        
        await generarTabla(data);
    });
}

// =====================================================================
// BOTONES RÁPIDOS
// =====================================================================

function initBotonesRapidos() {
    // Botón 50%
    document.getElementById('btn-50-percent').addEventListener('click', () => {
        const N0 = parseFloat(document.getElementById('tiempo-N0').value);
        if (N0 && N0 > 0) {
            document.getElementById('tiempo-N-objetivo').value = (N0 * 0.5).toFixed(4);
        }
    });
    
    // Botón 25%
    document.getElementById('btn-25-percent').addEventListener('click', () => {
        const N0 = parseFloat(document.getElementById('tiempo-N0').value);
        if (N0 && N0 > 0) {
            document.getElementById('tiempo-N-objetivo').value = (N0 * 0.25).toFixed(4);
        }
    });
    
    // Botón 10%
    document.getElementById('btn-10-percent').addEventListener('click', () => {
        const N0 = parseFloat(document.getElementById('tiempo-N0').value);
        if (N0 && N0 > 0) {
            document.getElementById('tiempo-N-objetivo').value = (N0 * 0.1).toFixed(4);
        }
    });
}

// =====================================================================
// SISTEMA DE BOTONES "USAR ESTOS DATOS"
// =====================================================================

function initBotonesUsar() {
    // Este se inicializa dinámicamente cuando se muestran resultados
}

function agregarBotonUsar(contenedorId, datosParaTransferir) {
    const contenedor = document.getElementById(contenedorId);
    if (!contenedor) return;
    
    // Remover botón anterior si existe
    const botonAnterior = contenedor.querySelector('.btn-usar-datos');
    if (botonAnterior) {
        botonAnterior.remove();
    }
    
    // Crear nuevo botón
    const divBotones = document.createElement('div');
    divBotones.style.marginTop = '20px';
    divBotones.style.textAlign = 'center';
    
    for (const destino in datosParaTransferir) {
        const btn = document.createElement('button');
        btn.textContent = destino;
        btn.className = 'btn btn-secondary btn-usar-datos';
        btn.style.margin = '5px';
        btn.addEventListener('click', () => transferirDatos(datosParaTransferir[destino]));
        divBotones.appendChild(btn);
    }
    
    contenedor.appendChild(divBotones);
}

function transferirDatos(config) {
    const { tab, campos } = config;
    
    // Cambiar a la pestaña objetivo
    document.querySelector(`[data-tab="${tab}"]`).click();
    
    // Llenar los campos
    for (const [fieldId, value] of Object.entries(campos)) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.value = value;
        }
    }
    
    // Mostrar mensaje de éxito
    mostrarNotificacion('✅ Datos transferidos correctamente');
}

// =====================================================================
// FUNCIONES DE CÁLCULO - API CALLS
// =====================================================================

async function calcularN(data) {
    try {
        const response = await fetch('/api/radiactiva/calcular-n', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.exito) {
            mostrarResultadoN(result);
        } else {
            mostrarError('resultado-n', result.error);
        }
    } catch (error) {
        mostrarError('resultado-n', 'Error de conexión con el servidor');
    }
}

async function calcularTiempo(data) {
    try {
        const response = await fetch('/api/radiactiva/calcular-tiempo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.exito) {
            mostrarResultadoTiempo(result);
        } else {
            mostrarError('resultado-tiempo', result.error);
        }
    } catch (error) {
        mostrarError('resultado-tiempo', 'Error de conexión con el servidor');
    }
}

async function calcularKDesdeTMedia(data) {
    try {
        const response = await fetch('/api/radiactiva/calcular-k', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.exito) {
            mostrarResultadoKTMedia(result);
        } else {
            mostrarError('resultado-k-tmedia', result.error);
        }
    } catch (error) {
        mostrarError('resultado-k-tmedia', 'Error de conexión con el servidor');
    }
}

async function calcularKDesdeDatos(data) {
    try {
        const response = await fetch('/api/radiactiva/calcular-k', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.exito) {
            mostrarResultadoKDatos(result);
        } else {
            mostrarError('resultado-k-datos', result.error);
        }
    } catch (error) {
        mostrarError('resultado-k-datos', 'Error de conexión con el servidor');
    }
}

async function calcularN0(data) {
    try {
        const response = await fetch('/api/radiactiva/calcular-n0', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.exito) {
            mostrarResultadoN0(result);
        } else {
            mostrarError('resultado-n0', result.error);
        }
    } catch (error) {
        mostrarError('resultado-n0', 'Error de conexión con el servidor');
    }
}

async function generarTabla(data) {
    try {
        const response = await fetch('/api/radiactiva/generar-tabla', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.exito) {
            mostrarTablaResultado(result);
        } else {
            mostrarError('resultado-tabla', result.error);
        }
    } catch (error) {
        mostrarError('resultado-tabla', 'Error de conexión con el servidor');
    }
}

// =====================================================================
// FUNCIONES DE VISUALIZACIÓN DE RESULTADOS
// =====================================================================

function mostrarResultadoN(result) {
    const contenedor = document.getElementById('resultado-n');
    contenedor.classList.remove('hidden');
    contenedor.classList.add('resultado-exito');
    
    contenedor.innerHTML = `
        <h3>✅ Resultado - Cantidad N(t)</h3>
        <div class="resultado-card">
            <div class="resultado-item">
                <span class="label">Cantidad en t = ${result.t}:</span>
                <span class="value">${result.N}</span>
            </div>
            <div class="resultado-item">
                <span class="label">Porcentaje restante:</span>
                <span class="value">${result.porcentaje}%</span>
            </div>
            <div class="resultado-item">
                <span class="label">Porcentaje desintegrado:</span>
                <span class="value">${(100 - result.porcentaje).toFixed(2)}%</span>
            </div>
            <div class="formula-resultado">
                <strong>Fórmula usada:</strong><br>
                ${result.formula}
            </div>
        </div>
        <div class="info-adicional">
            <p><strong>Parámetros:</strong></p>
            <p>• N₀ = ${result.N0}</p>
            <p>• k = ${result.k}</p>
            <p>• t = ${result.t}</p>
        </div>
    `;
    
    agregarBotonUsar('resultado-n', {
        'Usar en Generar Tabla': {
            tab: 'generar-tabla',
            campos: {
                'tabla-N0': result.N0,
                'tabla-k': result.k
            }
        }
    });
}

function mostrarResultadoTiempo(result) {
    const contenedor = document.getElementById('resultado-tiempo');
    contenedor.classList.remove('hidden');
    contenedor.classList.add('resultado-exito');
    
    // Calcular vidas medias
    const t_media = 0.693 / result.k;
    const vidas_medias = result.tiempo / t_media;
    
    contenedor.innerHTML = `
        <h3>✅ Resultado - Tiempo Necesario</h3>
        <div class="resultado-card">
            <div class="resultado-item">
                <span class="label">Tiempo necesario:</span>
                <span class="value destacado">${result.tiempo}</span>
            </div>
            <div class="resultado-item">
                <span class="label">Para alcanzar N =</span>
                <span class="value">${result.N_objetivo} (${result.porcentaje}% de N₀)</span>
            </div>
            <div class="resultado-item">
                <span class="label">Equivale a:</span>
                <span class="value">${vidas_medias.toFixed(2)} vidas medias</span>
            </div>
            <div class="formula-resultado">
                <strong>Vida media (t½):</strong> ${t_media.toFixed(4)}
            </div>
        </div>
        <div class="info-adicional">
            <p><strong>Parámetros:</strong></p>
            <p>• N₀ = ${result.N0}</p>
            <p>• k = ${result.k}</p>
            <p>• N objetivo = ${result.N_objetivo}</p>
        </div>
    `;
    
    agregarBotonUsar('resultado-tiempo', {
        'Usar en Generar Tabla': {
            tab: 'generar-tabla',
            campos: {
                'tabla-N0': result.N0,
                'tabla-k': result.k,
                'tabla-tiempo-total': result.tiempo
            }
        }
    });
}

function mostrarResultadoKTMedia(result) {
    const contenedor = document.getElementById('resultado-k-tmedia');
    contenedor.classList.remove('hidden');
    contenedor.classList.add('resultado-exito');
    
    estadoGlobal.k = { k: result.k, t_media: result.t_media };
    
    contenedor.innerHTML = `
        <h3>✅ Constante k Calculada</h3>
        <div class="resultado-card">
            <div class="resultado-item">
                <span class="label">Constante k:</span>
                <span class="value destacado">${result.k}</span>
            </div>
            <div class="resultado-item">
                <span class="label">Vida media (t½):</span>
                <span class="value">${result.t_media}</span>
            </div>
            <div class="formula-resultado">
                <strong>Fórmula:</strong><br>
                ${result.formula}
            </div>
        </div>
    `;
    
    agregarBotonUsar('resultado-k-tmedia', {
        'Usar en Calcular N(t)': {
            tab: 'calcular-n',
            campos: {
                'n-k': result.k
            }
        },
        'Usar en Calcular Tiempo': {
            tab: 'calcular-tiempo',
            campos: {
                'tiempo-k': result.k
            }
        },
        'Usar en Generar Tabla': {
            tab: 'generar-tabla',
            campos: {
                'tabla-k': result.k
            }
        }
    });
}

function mostrarResultadoKDatos(result) {
    const contenedor = document.getElementById('resultado-k-datos');
    contenedor.classList.remove('hidden');
    contenedor.classList.add('resultado-exito');
    
    estadoGlobal.k = { k: result.k, t_media: result.t_media };
    
    contenedor.innerHTML = `
        <h3>✅ Constante k Calculada desde Datos</h3>
        <div class="resultado-card">
            <div class="resultado-item">
                <span class="label">Constante k:</span>
                <span class="value destacado">${result.k}</span>
            </div>
            <div class="resultado-item">
                <span class="label">Vida media (t½):</span>
                <span class="value">${result.t_media}</span>
            </div>
            <div class="resultado-item">
                <span class="label">Porcentaje medido:</span>
                <span class="value">${result.porcentaje}%</span>
            </div>
            <div class="formula-resultado">
                <strong>Fórmula:</strong><br>
                ${result.formula}
            </div>
        </div>
        <div class="info-adicional">
            <p><strong>Verificación:</strong></p>
            <p>Con k = ${result.k}, en t = ${result.t}:</p>
            <p>N calculado = ${result.N_verificacion} (esperado: ${result.N_en_t})</p>
        </div>
    `;
    
    agregarBotonUsar('resultado-k-datos', {
        'Usar en Calcular N(t)': {
            tab: 'calcular-n',
            campos: {
                'n-N0': result.N0,
                'n-k': result.k
            }
        },
        'Usar en Calcular Tiempo': {
            tab: 'calcular-tiempo',
            campos: {
                'tiempo-N0': result.N0,
                'tiempo-k': result.k
            }
        },
        'Usar en Generar Tabla': {
            tab: 'generar-tabla',
            campos: {
                'tabla-N0': result.N0,
                'tabla-k': result.k
            }
        }
    });
}

function mostrarResultadoN0(result) {
    const contenedor = document.getElementById('resultado-n0');
    contenedor.classList.remove('hidden');
    contenedor.classList.add('resultado-exito');
    
    contenedor.innerHTML = `
        <h3>✅ Cantidad Inicial N₀ Calculada</h3>
        <div class="resultado-card">
            <div class="resultado-item">
                <span class="label">Cantidad inicial N₀:</span>
                <span class="value destacado">${result.N0}</span>
            </div>
            <div class="resultado-item">
                <span class="label">Cantidad actual N:</span>
                <span class="value">${result.N}</span>
            </div>
            <div class="resultado-item">
                <span class="label">Tiempo transcurrido:</span>
                <span class="value">${result.t}</span>
            </div>
            <div class="formula-resultado">
                <strong>Fórmula usada:</strong><br>
                ${result.formula}
            </div>
        </div>
        <div class="info-adicional">
            <p><strong>Interpretación:</strong></p>
            <p>En t=0 había ${result.N0} unidades de sustancia.</p>
            <p>Después de ${result.t} unidades de tiempo, quedaron ${result.N} unidades.</p>
        </div>
    `;
    
    agregarBotonUsar('resultado-n0', {
        'Usar en Calcular N(t)': {
            tab: 'calcular-n',
            campos: {
                'n-N0': result.N0,
                'n-k': result.k
            }
        },
        'Usar en Generar Tabla': {
            tab: 'generar-tabla',
            campos: {
                'tabla-N0': result.N0,
                'tabla-k': result.k
            }
        }
    });
}

function mostrarTablaResultado(result) {
    const contenedor = document.getElementById('resultado-tabla');
    contenedor.classList.remove('hidden');
    contenedor.classList.add('resultado-exito');
    
    // Crear tabla HTML
    let tablaHTML = `
        <h3>📊 Tabla de Desintegración Radiactiva</h3>
        <div class="info-adicional">
            <p><strong>Parámetros:</strong></p>
            <p>• N₀ = ${result.N0}</p>
            <p>• k = ${result.k}</p>
            <p>• Vida media (t½) = ${result.t_media}</p>
            <p>• Puntos de datos: ${result.num_puntos}</p>
        </div>
        <div class="tabla-wrapper">
            <table class="tabla-datos">
                <thead>
                    <tr>
                        <th>Tiempo (t)</th>
                        <th>Cantidad N(t)</th>
                        <th>Porcentaje (%)</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    result.tabla.forEach(row => {
        tablaHTML += `
            <tr>
                <td>${row.tiempo}</td>
                <td>${row.N}</td>
                <td>${row.porcentaje}%</td>
            </tr>
        `;
    });
    
    tablaHTML += `
                </tbody>
            </table>
        </div>
        <div id="grafica-container">
            <canvas id="grafica-desintegracion"></canvas>
        </div>
    `;
    
    contenedor.innerHTML = tablaHTML;
    
    // Crear gráfica
    crearGrafica(result);
}

function crearGrafica(result) {
    const ctx = document.getElementById('grafica-desintegracion');
    
    if (!ctx) return;
    
    // Extraer datos
    const tiempos = result.tabla.map(row => row.tiempo);
    const cantidades = result.tabla.map(row => row.N);
    const porcentajes = result.tabla.map(row => row.porcentaje);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: tiempos,
            datasets: [
                {
                    label: 'Cantidad N(t)',
                    data: cantidades,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    yAxisID: 'y'
                },
                {
                    label: 'Porcentaje (%)',
                    data: porcentajes,
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Desintegración Radiactiva en el Tiempo',
                    color: '#f1f5f9',
                    font: { size: 18 }
                },
                legend: {
                    labels: {
                        color: '#f1f5f9'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#3b82f6',
                    bodyColor: '#fff',
                    borderColor: '#3b82f6',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Tiempo (t)',
                        color: '#cbd5e1'
                    },
                    ticks: { color: '#cbd5e1' },
                    grid: { color: 'rgba(51, 65, 85, 0.5)' }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Cantidad N(t)',
                        color: '#cbd5e1'
                    },
                    ticks: { color: '#cbd5e1' },
                    grid: { color: 'rgba(51, 65, 85, 0.5)' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Porcentaje (%)',
                        color: '#cbd5e1'
                    },
                    ticks: { color: '#cbd5e1' },
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });
}

// =====================================================================
// FUNCIONES AUXILIARES
// =====================================================================

function mostrarError(contenedorId, mensaje) {
    const contenedor = document.getElementById(contenedorId);
    contenedor.classList.remove('hidden');
    contenedor.classList.remove('resultado-exito');
    contenedor.classList.add('resultado-error');
    
    contenedor.innerHTML = `
        <h3>❌ Error</h3>
        <p>${mensaje}</p>
    `;
}

function mostrarNotificacion(mensaje) {
    // Crear elemento de notificación
    const notif = document.createElement('div');
    notif.className = 'notificacion';
    notif.textContent = mensaje;
    notif.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        color: #fff;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        z-index: 10000;
        font-weight: bold;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notif);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notif.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}

// Agregar animaciones CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
