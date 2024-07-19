import tkinter as tk
from tkinter import messagebox


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Queue:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def esta_vacia(self):
        return self.primero == None

    def encolar(self, dato):
        if self.esta_vacia():
            self.primero = self.ultimo = Nodo(dato)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = Nodo(dato)

    def desencolar(self):
        if self.esta_vacia():
            print("La cola está vacía")
        elif self.primero == self.ultimo:
            self.primero = self.ultimo = None
        else:
            aux = self.primero
            self.primero = aux.siguiente
            return aux.dato


class GatoRaton:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.geometry("400x400")
        self.ventana.title("Gato y Raton")
        self.turno = 0  # 0: player 1, 1: player 2
        self.tablero = [[None]*3 for _ in range(3)]
        self.cola = Queue()
        self.cola.encolar("Jugador 1")
        self.cola.encolar("Jugador 2")
        self.dibujar_tablero()

    def dibujar_tablero(self):
        self.botones = []
        for i in range(3):
            filas = []
            for j in range(3):
                button = tk.Button(self.ventana, width=5, height=2, font=('Helvetica', 30),
                                   command=lambda x=i, y=j: self.jugar_turno(x, y))
                button.grid(row=i, column=j)
                filas.append(button)
            self.botones.append(filas)

    def jugar_turno(self, fila, columna):
        jugador = self.cola.desencolar()
        self.botones[fila][columna].config(
            text="🐱" if self.turno == 0 else "🐀", state="disabled")
        self.tablero[fila][columna] = self.turno
        if self.checar_ganador():
            self.mostrar_mensaje(f"{jugador} ha ganado!")
            self.reiniciar_juego()
        elif all(all(celda is not None for celda in fila) for fila in self.tablero):
            self.mostrar_mensaje("Es un empate!")
            self.reiniciar_juego()
        else:
            self.turno = 1 - self.turno
            self.cola.encolar(jugador)

    def checar_ganador(self):
        # Check rows
        for i in range(3):
            if self.tablero[i][0] == self.tablero[i][1] == self.tablero[i][2] is not None:
                return True

        # Check columns
        for j in range(3):
            if self.tablero[0][j] == self.tablero[1][j] == self.tablero[2][j] is not None:
                return True

        # Check diagonals
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] is not None:
            return True

        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] is not None:
            return True

        return False

    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Game Over", mensaje)

    def reiniciar_juego(self):
        self.turno = 0
        self.tablero = [[None]*3 for _ in range(3)]
        self.cola = Queue()
        self.cola.encolar("Player 1")
        self.cola.encolar("Player 2")
        for i in range(3):
            for j in range(3):
                self.botones[i][j].config(text="", state="normal")


root = tk.Tk()
juego = GatoRaton(root)
root.mainloop()
