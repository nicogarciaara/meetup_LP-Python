# Código obtenido desde el repo de PuLP y traducido:
# Original en https://github.com/coin-or/pulp/blob/master/examples/Sudoku2.py

from pulp import (
    LpProblem,
    LpStatus,
    lpSum,
    LpVariable,
    value,
)

# Todas las filas, columnas y valores posibles están entre 1 y 9
VALS = ROWS = COLS = range(1, 10)

# Generamos la lista de cajas que tendremos, de acuerdo a los índices que las ocupan
Boxes = [
    [(3 * i + k + 1, 3 * j + l + 1) for k in range(3) for l in range(3)]
    for i in range(3) for j in range(3)
]

# La variable LpProblem se genera para almacenar toda la información del problema
prob = LpProblem("Sudoku")

# Creamos las variables de decisión
choices = LpVariable.dicts("Choice", (VALS, ROWS, COLS), cat='Binary')

# No necesitamos definir una función objetivo! Contraint Programming!

# Debemos asegurar que solamente llenamos un casillero con un valor a la vez
for r in ROWS:
    for c in COLS:
        prob += lpSum([choices[v][r][c] for v in VALS]) == 1

# Agregamos las restricciones de un único valor en cada fila, columna y caja
for v in VALS:
    for r in ROWS:
        prob += lpSum([choices[v][r][c] for c in COLS]) == 1

    for c in COLS:
        prob += lpSum([choices[v][r][c] for r in ROWS]) == 1

    for b in Boxes:
        prob += lpSum([choices[v][r][c] for (r, c) in b]) == 1

# Armemos el sudoku, como en la imagen.
input_data = [
    (5, 1, 1),
    (6, 2, 1),
    (8, 4, 1),
    (4, 5, 1),
    (7, 6, 1),
    (3, 1, 2),
    (9, 3, 2),
    (6, 7, 2),
    (8, 3, 3),
    (1, 2, 4),
    (8, 5, 4),
    (4, 8, 4),
    (7, 1, 5),
    (9, 2, 5),
    (6, 4, 5),
    (2, 6, 5),
    (1, 8, 5),
    (8, 9, 5),
    (5, 2, 6),
    (3, 5, 6),
    (9, 8, 6),
    (2, 7, 7),
    (6, 3, 8),
    (8, 7, 8),
    (7, 9, 8),
    (3, 4, 9),
#    Si activamos estos 3 lugares, lo podemos hacer único
#    (1, 5, 9),
#    (6, 6, 9),
#    (5, 8, 9)
]

for (v, r, c) in input_data:
    prob += choices[v][r][c] == 1

# Podemos escribir el problema en un archivo de texto (cuidado, puede marear)
prob.writeLP("Sudoku.lp")

# Vamos a buscar soluciones del problema hasta que falle
while True:
    prob.solve()
    # Podemos anotar el estado del problema
    print("Status:", LpStatus[prob.status], "\n")
    # Imprimimos si cumplimos con las restricciones, o sea la solución es óptima
    if LpStatus[prob.status] == "Optimal":
        # Escribimos la solución en pantalla, avanzando por fila
        for r in ROWS:
            # Le metemos las barritas cuando corresponde
            if r in [1, 4, 7]:
                print("+-------+-------+-------+")
            for c in COLS:
                for v in VALS:
                    if value(choices[v][r][c]) == 1:
                        if c in [1, 4, 7]:
                            # Imprimimos la barra vertical cuando corresponde
                            print("|", end=" ")
                        print(str(v), end=" ")
                        if c == 9:
                            print("|")
        print("+-------+-------+-------+\n")
        # Con esto le decimos al problema que ya no puede tener la última solución usada
        prob += lpSum([choices[v][r][c] for v in VALS for r in ROWS for c in COLS
                       if value(choices[v][r][c]) == 1]) <= 80
    # Si no podemos encontrar una solución óptima, nos vamos
    else:
        print("No encontré más soluciones, hice lo que pude, chauchis")
        break
