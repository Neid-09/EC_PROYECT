# Ley de Enfriamiento de Newton

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Aplicación para calcular la temperatura de objetos utilizando la **Ley de Enfriamiento de Newton**.

## 📐 Fórmula

```text
T(t) = Tm + C * e^(K*t)
```

Donde:

- **T(t)**: Temperatura del objeto en el tiempo t
- **Tm**: Temperatura del medio ambiente
- **C**: Constante (diferencia inicial de temperatura: T0 - Tm)
- **K**: Constante de enfriamiento (negativa para enfriamiento)
- **t**: Tiempo transcurrido
- **e**: Constante de Euler (≈ 2.71828)

## 🚀 Características

- ✅ Calcular temperatura en un tiempo específico
- ✅ Calcular tiempo para alcanzar una temperatura objetivo
- ✅ Calcular constante K con datos conocidos
- ✅ Generar tablas de enfriamiento
- ✅ Submenús interactivos para múltiples cálculos
- ✅ Validación de datos de entrada
- ✅ Interfaz intuitiva con emojis

## 📁 Estructura del Proyecto

```text
EC_PROYECT/
│
├── newton_cooling/           # Paquete principal
│   ├── __init__.py          # Inicializador del paquete
│   │
│   ├── core/                # Módulo de lógica de negocio
│   │   ├── __init__.py
│   │   ├── calculations.py  # Funciones matemáticas
│   │   └── constants.py     # Constantes del proyecto
│   │
│   ├── ui/                  # Módulo de interfaz de usuario
│   │   ├── __init__.py
│   │   ├── menu.py         # Menú principal
│   │   ├── options.py      # Opciones del menú
│   │   └── display.py      # Funciones de visualización
│   │
│   └── utils/              # Módulo de utilidades
│       ├── __init__.py
│       ├── validators.py   # Validación de entradas
│       └── screen.py       # Utilidades de pantalla
│
├── main.py                 # Punto de entrada principal
├── README.md              # Este archivo
└── requirements.txt       # Dependencias (si las hay)
```

## 🔧 Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/Neid-09/EC_PROYECT.git
   cd EC_PROYECT
   ```

2. **Ejecutar la aplicación:**

   ```bash
   python main.py
   ```

## 💻 Uso

### Ejemplo 1: Calcular temperatura

```text
Datos:
- Temperatura ambiente (Tm): 20°C
- Constante C: 70
- Constante K: -0.05
- Tiempo: 10 minutos

Resultado: T(10) = 42.42°C
```

### Ejemplo 2: Calcular constante K

```text
Datos:
- Temperatura inicial T(0): 90°C
- Temperatura ambiente: 20°C
- Temperatura en t=5: 70°C
- Tiempo: 5 minutos

Resultado: K = -0.0539 (1/min)
```

## 📊 Valores Típicos de K

| Material/Situación | K (1/min) |
|-------------------|-----------|
| Agua en aire | -0.01 a -0.05 |
| Metal pequeño | -0.05 a -0.15 |
| Café en taza | -0.08 a -0.12 |

## 🎯 Aplicaciones

- 🔬 Ciencia forense (determinar hora de muerte)
- 🍕 Industria alimentaria (enfriamiento de productos)
- 🏭 Ingeniería térmica
- ⛅ Meteorología

## 👨‍💻 Autor

**Neider Duvan Guindigua Machoa**  

- GitHub: [Neid-09](https://github.com/Neid-09)
