# Smart Horses

Un juego de estrategia para dos jugadores donde debes mover tu caballo y acumular más puntos que la computadora. El juego utiliza el algoritmo **Minimax con poda Alpha-Beta** para la inteligencia artificial del oponente.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Descripción

Smart Horses es un juego de estrategia inspirado en el movimiento del caballo del ajedrez. Los jugadores se turnan para mover sus caballos por un tablero, buscando acumular puntos al aterrizar en casillas especiales. El juego termina cuando ninguno de los dos jugadores puede realizar un movimiento válido, y gana quien tenga más puntos.

La computadora utiliza un algoritmo de búsqueda **Minimax con poda Alpha-Beta** y una **heurística avanzada** para tomar decisiones estratégicas en tres niveles de dificultad diferentes.

## Características

-  **Interfaz gráfica moderna** construida con Tkinter
-  **IA inteligente** con algoritmo Minimax y poda Alpha-Beta
-  **Tres niveles de dificultad**: Principiante, Amateur y Experto
-  **Música de fondo y efectos de sonido**
-  **Diseño visual atractivo** con colores y efectos de hover
-  **Sistema de puntuación** con casillas positivas y negativas
-  **Visualización de movimientos válidos** con resaltado interactivo

##  Objetivo del Juego

Acumula más puntos que la computadora moviendo tu caballo estratégicamente por el tablero. El juego termina cuando ninguno de los dos jugadores puede realizar un movimiento válido, y gana quien tenga más puntos.

##  Reglas del Juego

### Movimiento
- Los caballos se mueven en forma de **"L"** (como en ajedrez): 2 casillas en una dirección + 1 casilla perpendicular
- Solo puedes moverte a casillas válidas que no estén destruidas ni ocupadas

### Puntos
- **Casillas verdes**: Suman puntos (+1, +3, +4, +5, +10)
- **Casillas rojas**: Restan puntos (-1, -3, -4, -5, -10)
- **Casillas visitadas**: Se destruyen (marcadas en rojo oscuro) y ya no son accesibles

### Penalización
- Si un jugador no puede moverse pero su oponente sí, recibe **-4 puntos** de penalización

### Victoria
- Gana quien tenga más puntos cuando ninguno de los dos jugadores pueda realizar un movimiento válido

## Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**:
```bash
git clone https://github.com/felipegarcialondono/smart_horses
cd smart_horse
```

2. **Crear un entorno virtual** (recomendado):
```bash
python -m venv venv
```

3. **Activar el entorno virtual**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar las dependencias**:
```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `tk` - Interfaz gráfica (incluida en Python)
- `Pillow` - Manejo de imágenes
- `pygame` - Reproducción de audio

## Cómo Jugar

1. **Ejecutar el juego**:
```bash
python main.py
```

2. **En el menú principal**:
   - Haz clic en **"INICIAR JUEGO"** para comenzar
   - Revisa las **"INSTRUCCIONES"** si necesitas ayuda
   - Ajusta el **volumen** con el control deslizante

3. **Seleccionar dificultad**:
   - **Principiante**: Profundidad 2 (ideal para empezar)
   - **Amateur**: Profundidad 4 (desafío moderado)
   - **Experto**: Profundidad 6 (para jugadores avanzados)

4. **Jugar**:
   - Haz clic en una casilla resaltada (movimiento válido) para mover tu caballo
   - La computadora jugará automáticamente después de tu turno
   - Observa tu puntuación y la de la computadora en el panel lateral

## Estructura del Proyecto

```
smart_horse/
│
├── app/
│   ├── models/
│   │   ├── game.py          # Lógica del juego y heurística
│   │   ├── machine.py       # Implementación Minimax con Alpha-Beta
│   │   ├── match.py         # Modelo del juego y tablero
│   │   ├── node.py          # Estructura de nodos del árbol Minimax
│   │   └── player.py        # Lógica del jugador humano
│   │
│   ├── utils/
│   │   ├── constants.py     # Constantes del juego
│   │   └── music_player.py  # Reproducción de música y sonidos
│   │
│   ├── views/
│   │   ├── home_view.py         # Vista del menú principal
│   │   ├── difficulty_view.py   # Vista de selección de dificultad
│   │   └── game_view.py         # Vista del tablero de juego
│   │
│   └── controller.py        # Controlador principal (MVC)
│
├── assets/
│   ├── icons/              # Iconos para instrucciones
│   ├── music/              # Archivos de música de fondo
│   └── sounds/             # Efectos de sonido
│
├── tests/
│   └── test_heuristic.py   # Pruebas de la heurística
│
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## Algoritmo de IA

### Minimax con Poda Alpha-Beta

El juego implementa el algoritmo **Minimax con poda Alpha-Beta** para la inteligencia artificial:

- **Minimax**: Algoritmo de búsqueda en árbol que encuentra el movimiento óptimo asumiendo que el oponente también juega de forma óptima
- **Poda Alpha-Beta**: Optimización que reduce significativamente el número de nodos evaluados cortando ramas que no afectarán el resultado final

### Heurística

La función de evaluación considera tres componentes principales:

1. **Puntuación Actual** (peso: 1.0)
   - Diferencia de puntos entre la máquina y el jugador
   - Incluye penalizaciones por quedarse sin movimientos

2. **Potencial de Puntuación** (peso: 0.5)
   - Casillas especiales accesibles desde la posición actual
   - Considera tanto casillas positivas como negativas

3. **Movilidad** (peso: 0.1)
   - Diferencia en el número de movimientos válidos disponibles
   - Favorece posiciones con más opciones estratégicas

### Niveles de Dificultad

- **Principiante**: Profundidad de búsqueda = 2 niveles
- **Amateur**: Profundidad de búsqueda = 4 niveles
- **Experto**: Profundidad de búsqueda = 6 niveles

A mayor profundidad, la IA puede ver más movimientos hacia adelante y tomar decisiones más estratégicas.

## Tecnologías Utilizadas

- **Python 3.8+** - Lenguaje de programación
- **Tkinter** - Interfaz gráfica de usuario
- **Pillow (PIL)** - Procesamiento de imágenes
- **Pygame** - Reproducción de audio
- **Algoritmos de IA** - Minimax con poda Alpha-Beta

## Notas de Desarrollo

### Modificar el Tamaño del Tablero

Se puede cambiar el tamaño del tablero editando `app/utils/constants.py`:
```python
ROWS = 8  # Número de filas
COLS = 8  # Número de columnas
```

### Ajustar la Heurística

Se pueden modificar los pesos de la heurística en `app/models/game.py`:
```python
W_SCORE = 1.0      # Peso de la puntuación actual
W_POTENTIAL = 0.5  # Peso del potencial de puntuación
W_MOVILITY = 0.1   # Peso de la movilidad
```

### Cambiar los Valores de las Casillas Especiales

Editar `VALUES_SQUARES` en `app/utils/constants.py`:
```python
VALUES_SQUARES = frozenset({-10, -5, -4, -3, -1, 1, 3, 4, 5, 10})
```

## Solución de Problemas

### Error al cargar imágenes
- Asegurarse de que los archivos en la carpeta `assets/` estén presentes
- Verificar que Pillow esté correctamente instalado

### Error de audio
- Verificar que pygame esté instalado correctamente
- Si hay problemas con el audio, el juego seguirá funcionando sin sonido

### La ventana se ve muy pequeña/grande
- Se puede ajustar el tamaño de la ventana en `app/controller.py`:
  ```python
  self.root.geometry("1400x900") 
  ```

## Licencia

Este proyecto está bajo la Licencia MIT. Puedes usar, modificar y distribuir libremente.

## Autores

- Juan Sebastian Sierra Cruz - 2343656
- Luis Felipe Garcia Londoño - 2343105
- Jhoan Sebastian Fernandez Velasquez - 2222772
- David Alejandro Enciso Gutierrez - 2240581

---

