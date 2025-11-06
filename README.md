# Ecuaciones Diferenciales Aplicadas: Newton y Desintegración Radiactiva

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Aplicación de consola para resolver problemas basados en ecuaciones diferenciales, incluyendo:

1. **Ley de Enfriamiento de Newton**: Para calcular la temperatura de objetos.
2. **Desintegración Radiactiva**: Para analizar la disminución de sustancias a lo largo del tiempo.

---

## � Estructura del Proyecto

El proyecto está organizado en dos paquetes principales, `newton_cooling` y `desintegracion_radiactiva`, cada uno con su propia lógica, interfaz y utilidades.

```text
EC_PROYECT/
│
├── newton_cooling/           # Paquete para Ley de Enfriamiento de Newton
├── desintegracion_radiactiva/  # Paquete para Desintegración Radiactiva
│
├── main.py                 # Punto de entrada principal
├── app.py                  # Configuración de la aplicación web (Flask)
├── templates/              # Plantillas HTML para la interfaz web
├── static/                 # Archivos estáticos (CSS, JS)
├── README.md               # Este archivo
└── requirements.txt        # Dependencias
```

## 🔧 Instalación

1. **Clonar el repositorio:**

    ```bash
    git clone https://github.com/Neid-09/EC_PROYECT.git
    cd EC_PROYECT
    ```

2. **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Ejecutar la aplicación de consola:**

    ```bash
    python main.py
    ```

4. **Ejecutar la aplicación web:**

    ```bash
    python app.py
    ```

    Y abre `http://127.0.0.1:5000` en tu navegador.

---

## 🧊 Ley de Enfriamiento de Newton

Módulo para calcular la temperatura de un objeto en un medio ambiente a temperatura constante.

### Fórmula de Newton

```text
T(t) = Tm + C * e^(K*t)
```

- **T(t)**: Temperatura del objeto en el tiempo `t`.
- **Tm**: Temperatura del medio ambiente.
- **C**: Constante de diferencia de temperatura inicial (`T0 - Tm`).
- **K**: Constante de enfriamiento (negativa).
- **t**: Tiempo transcurrido.

### Características (Newton)

- ✅ Calcular temperatura en un tiempo específico.
- ✅ Calcular tiempo para alcanzar una temperatura.
- ✅ Calcular la constante `K` con datos conocidos.
- ✅ Generar tablas de enfriamiento.

### Uso (Ejemplos de Newton)

Ejemplo 1: Calcular temperatura

```text
Datos:
- Temperatura ambiente (Tm): 20°C
- Constante C: 70
- Constante K: -0.05
- Tiempo: 10 minutos

Resultado: T(10) = 42.42°C
```

Ejemplo 2: Calcular constante K

```text
Datos:
- Temperatura inicial T(0): 90°C
- Temperatura ambiente: 20°C
- Temperatura en t=5: 70°C
- Tiempo: 5 minutos

Resultado: K = -0.0539 (1/min)
```

### Aplicaciones (Newton)

- 🔬 **Ciencia forense**: Determinar la hora de la muerte.
- 🍕 **Industria alimentaria**: Controlar el enfriamiento de productos.
- 🏭 **Ingeniería térmica**: Diseño de sistemas de disipación de calor.

---

## ⚛️ Desintegración Radiactiva

Módulo para resolver problemas de desintegración de isótopos radiactivos.

### Fórmula de Desintegración

```text
N(t) = N0 * e^(-k*t)
```

- **N(t)**: Cantidad de sustancia en el tiempo `t`.
- **N0**: Cantidad inicial de sustancia.
- **k**: Constante de desintegración (positiva).
- **t**: Tiempo transcurrido.

### Características (Desintegración)

- ✅ Calcular la cantidad de sustancia restante.
- ✅ Calcular el tiempo necesario para alcanzar una cantidad específica (datación).
- ✅ Calcular la cantidad inicial `N0`.
- ✅ Calcular la constante `k` a partir de la vida media.

### Uso (Ejemplos de Desintegración)

Ejemplo 1: Calcular cantidad restante

```text
Datos:
- Cantidad inicial (N0): 100g
- Vida media (t½): 5730 años (Carbono-14)
- Constante k: ln(2) / 5730 ≈ 0.0001209 (1/año)
- Tiempo: 2000 años

Resultado: N(2000) ≈ 78.52g
```

Ejemplo 2: Calcular tiempo transcurrido (Datación)

```text
Datos:
- Porcentaje restante de sustancia (N/N0): 65%
- Vida media (t½): 5730 años (Carbono-14)
- Constante k: ≈ 0.0001209 (1/año)

Resultado: t ≈ 3563 años
```

### Vida Media de Isótopos Comunes

| Isótopo           | Vida Media (t½)             |
|-------------------|-----------------------------|
| Carbono-14        | ~5,730 años                 |
| Uranio-235        | ~703.8 millones de años     |
| Uranio-238        | ~4.468 mil millones de años |
| Potasio-40        | ~1.251 mil millones de años |
| Radio-226         | ~1,600 años                 |
| Yodo-131          | ~8.02 días                  |

### Aplicaciones (Desintegración)

- 🌍 **Geología y Arqueología**: Datación de fósiles y rocas.
- ⚕️ **Medicina**: Diagnóstico por imágenes y radioterapia.
- ⚡ **Energía**: Generación en reactores nucleares.

---

## 👨‍💻 Autor

**Neider Duvan Guindigua Machoa**  

- GitHub: [Neid-09](https://github.com/Neid-09)
