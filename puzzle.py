import tkinter as tk
import random
from collections import deque

# Estado objetivo
GOAL_STATE = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', ' ']]

# Crear la ventana principal de tkinter
class PuzzleSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle Deslizante 3x3")
        self.frame = tk.Frame(root, bg="lightblue")
        self.frame.grid(row=0, column=0)
        self.buttons = []
        self.state = self.generate_random_state()
        self.create_buttons()

        # Botones para Resolver y Reiniciar
        self.solve_button = tk.Button(self.frame, text="Resolver", command=self.solve_puzzle, bg="green", fg="white")
        self.solve_button.grid(row=4, column=0, padx=10, pady=10)
        self.reset_button = tk.Button(self.frame, text="Reiniciar", command=self.reset_puzzle, bg="red", fg="white")
        self.reset_button.grid(row=4, column=2, padx=10, pady=10)

        self.solution_path = []

    def create_buttons(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.frame, text=self.state[i][j], font=("Helvetica", 20), height=2, width=5)
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.state[i][j])

    def find_blank_position(self, state):
        for i, row in enumerate(state):
            for j, value in enumerate(row):
                if value == ' ':
                    return i, j

    def move(self, state, direction):
        i, j = self.find_blank_position(state)
        new_state = [row[:] for row in state]

        if direction == 'up' and i > 0:
            new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
        elif direction == 'down' and i < 2:
            new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
        elif direction == 'left' and j > 0:
            new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
        elif direction == 'right' and j < 2:
            new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]

        return new_state

    def generate_random_state(self):
        nums = [str(i) for i in range(1, 9)] + [' ']
        random.shuffle(nums)
        return [nums[i:i+3] for i in range(0, 9, 3)]

    def reset_puzzle(self):
        self.state = self.generate_random_state()  # Generar un nuevo estado aleatorio
        self.update_buttons()  # Actualizar los botones con el nuevo estado
        self.solution_path = []  # Reiniciar la solución

    def solve_puzzle(self):
        initial_state = self.state
        queue = deque([(initial_state, [])])  # Cola para BFS
        visited = set()  # Conjunto para rastrear estados visitados
        visited.add(tuple(map(tuple, initial_state)))  # Añadir estado inicial

        while queue:
            state, path = queue.popleft()

            if state == GOAL_STATE:
                self.solution_path = path
                self.show_solution()
                return

            for direction in ['up', 'down', 'left', 'right']:
                new_state = self.move(state, direction)
                state_tuple = tuple(map(tuple, new_state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    queue.append((new_state, path + [direction]))

    def show_solution(self):
        for move in self.solution_path:
            self.state = self.move(self.state, move)  # Mover el puzzle
            self.update_buttons()  # Actualizar la interfaz gráfica
            self.root.update()
            self.root.after(500)  # Añadir un retraso para visualizar los movimientos

# Crear la aplicación Tkinter
root = tk.Tk()
app = PuzzleSolverApp(root)
root.mainloop()
