import tkinter as tk
import random
from collections import deque

# Estado objetivo
ESTADO_OBJETIVO = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', ' ']]

# Crear la ventana principal de tkinter
class AplicacionPuzzle:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Puzzle Deslizante 3x3")
        self.marco = tk.Frame(raiz, bg="lightblue")
        self.marco.grid(row=0, column=0)
        self.botones = []
        self.estado = self.generar_estado_aleatorio()
        self.crear_botones()

        # Botones para Resolver y Reiniciar
        self.boton_resolver = tk.Button(self.marco, text="Resolver", command=self.resolver_puzzle, bg="green", fg="white")
        self.boton_resolver.grid(row=4, column=0, padx=10, pady=10)
        self.boton_reiniciar = tk.Button(self.marco, text="Reiniciar", command=self.reiniciar_puzzle, bg="red", fg="white")
        self.boton_reiniciar.grid(row=4, column=2, padx=10, pady=10)

        self.ruta_solucion = []

    def crear_botones(self):
        for i in range(3):
            fila = []
            for j in range(3):
                boton = tk.Button(self.marco, text=self.estado[i][j], font=("Helvetica", 20), height=2, width=5)
                boton.grid(row=i, column=j)
                fila.append(boton)
            self.botones.append(fila)

    def actualizar_botones(self):
        for i in range(3):
            for j in range(3):
                self.botones[i][j].config(text=self.estado[i][j])

    def encontrar_posicion_vacia(self, estado):
        for i, fila in enumerate(estado):
            for j, valor in enumerate(fila):
                if valor == ' ':
                    return i, j

    def mover(self, estado, direccion):
        i, j = self.encontrar_posicion_vacia(estado)
        nuevo_estado = [fila[:] for fila in estado]

        if direccion == 'arriba' and i > 0:
            nuevo_estado[i][j], nuevo_estado[i-1][j] = nuevo_estado[i-1][j], nuevo_estado[i][j]
        elif direccion == 'abajo' and i < 2:
            nuevo_estado[i][j], nuevo_estado[i+1][j] = nuevo_estado[i+1][j], nuevo_estado[i][j]
        elif direccion == 'izquierda' and j > 0:
            nuevo_estado[i][j], nuevo_estado[i][j-1] = nuevo_estado[i][j-1], nuevo_estado[i][j]
        elif direccion == 'derecha' and j < 2:
            nuevo_estado[i][j], nuevo_estado[i][j+1] = nuevo_estado[i][j+1], nuevo_estado[i][j]

        return nuevo_estado

    def generar_estado_aleatorio(self):
        numeros = [str(i) for i in range(1, 9)] + [' ']
        random.shuffle(numeros)
        return [numeros[i:i+3] for i in range(0, 9, 3)]

    def reiniciar_puzzle(self):
        self.estado = self.generar_estado_aleatorio()  # Generar un nuevo estado aleatorio
        self.actualizar_botones()  # Actualizar los botones con el nuevo estado
        self.ruta_solucion = []  # Reiniciar la solución

    def resolver_puzzle(self):
        estado_inicial = self.estado
        cola = deque([(estado_inicial, [])])  # Cola para BFS
        visitados = set()  # Conjunto para rastrear estados visitados
        visitados.add(tuple(map(tuple, estado_inicial)))  # Añadir estado inicial

        while cola:
            estado, ruta = cola.popleft()

            if estado == ESTADO_OBJETIVO:
                self.ruta_solucion = ruta
                self.mostrar_solucion()
                return

            for direccion in ['arriba', 'abajo', 'izquierda', 'derecha']:
                nuevo_estado = self.mover(estado, direccion)
                estado_tupla = tuple(map(tuple, nuevo_estado))
                if estado_tupla not in visitados:
                    visitados.add(estado_tupla)
                    cola.append((nuevo_estado, ruta + [direccion]))

    def mostrar_solucion(self):
        for movimiento in self.ruta_solucion:
            self.estado = self.mover(self.estado, movimiento)  # Mover el puzzle
            self.actualizar_botones()  # Actualizar la interfaz gráfica
            self.raiz.update()
            self.raiz.after(2000)  # Añadir un retraso para visualizar los movimientos

# Crear la aplicación Tkinter
raiz = tk.Tk()
app = AplicacionPuzzle(raiz)
raiz.mainloop()
