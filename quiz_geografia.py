import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

FUENTE = "Times New Roman"
LIMITE_SEGUNDOS = 5


class Quiz:
    def __init__(self, root):
        self.root = root
        root.title("Quiz de Geografía Mundial")
        root.geometry("550x350")
        root.resizable(False, False)
        self.inicio()

    def limpiar(self):
        for w in self.root.winfo_children():
            w.destroy()

    def etiqueta(self, texto, tam, negrita=False, **pack):
        estilo = "bold" if negrita else "normal"
        tk.Label(self.root, text=texto, font=(FUENTE, tam, estilo),
                 wraplength=480).pack(**pack)

    def cargar_preguntas(self):
        try:
            with open("preguntas.txt", encoding="utf-8") as f:
                lineas = [l.strip().split("|") for l in f if l.strip()]
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró 'preguntas.txt'.")
            return None

        # Cada pregunta: texto | op1 | op2 | op3 | op4 | correcta
        preguntas = [[p.strip() for p in l] for l in lineas if len(l) == 6]
        if len(preguntas) < 5:
            messagebox.showerror("Error", "Se necesitan al menos 5 preguntas.")
            return None
        return random.sample(preguntas, 5)

    # ---------- Pantalla de inicio ----------
    def inicio(self):
        self.limpiar()
        self.etiqueta("Quiz de Geografía Mundial", 20, True, pady=60)
        tk.Button(self.root, text="Empezar", font=(FUENTE, 14), width=15,
                  command=self.empezar).pack(pady=20)

    def empezar(self):
        preguntas = self.cargar_preguntas()
        if preguntas:
            self.preguntas = preguntas
            self.indice = 0
            self.puntaje = 0
            self.vidas = 5
            self.t_total = time.time()
            self.juego()

    # ---------- Pantalla de juego ----------
    def juego(self):
        self.limpiar()
        if self.vidas <= 0 or self.indice >= len(self.preguntas):
            self.resultados()
            return

        texto, *opciones, self.correcta = self.preguntas[self.indice]

        barra = tk.Frame(self.root)
        barra.pack(fill="x", padx=20, pady=15)
        tk.Label(barra, text=f"Vidas: {self.vidas}",
                 font=(FUENTE, 12, "bold")).pack(side="left")
        self.lbl_tiempo = tk.Label(barra, text="Tiempo: 0s", font=(FUENTE, 12))
        self.lbl_tiempo.pack(side="left", padx=90)
        tk.Label(barra, text=f"Puntos: {self.puntaje}",
                 font=(FUENTE, 12, "bold")).pack(side="right")

        self.etiqueta(texto, 15, pady=25)

        self.combo = ttk.Combobox(self.root, values=opciones, state="readonly",
                                  font=(FUENTE, 12), width=30)
        self.combo.set("Selecciona una respuesta")
        self.combo.pack(pady=10)

        tk.Button(self.root, text="Responder", font=(FUENTE, 12), width=15,
                  command=self.responder).pack(pady=25)

        self.t_pregunta = time.time()
        self.actualizar_reloj()

    def actualizar_reloj(self):
        if self.lbl_tiempo.winfo_exists():
            self.lbl_tiempo.config(text=f"Tiempo: {int(time.time() - self.t_total)}s")
            self.root.after(1000, self.actualizar_reloj)

    def responder(self):
        eleccion = self.combo.get()
        if eleccion == "Selecciona una respuesta":
            messagebox.showwarning("Aviso", "Por favor selecciona una opción.")
            return

        tardanza = time.time() - self.t_pregunta
        if tardanza > LIMITE_SEGUNDOS:
            self.vidas -= 1
            messagebox.showinfo(
                "Tiempo agotado",
                f"Tardaste {tardanza:.1f}s (máximo {LIMITE_SEGUNDOS}s). Pierdes 1 vida.")
        elif eleccion == self.correcta:
            self.puntaje += 10
        else:
            self.vidas -= 1

        self.indice += 1
        self.juego()

    # ---------- Pantalla de resultados ----------
    def resultados(self):
        self.limpiar()
        total = time.time() - self.t_total
        messagebox.showinfo("Fin del juego", "¡La partida ha terminado!")

        self.etiqueta("Resultados Finales", 18, True, pady=30)
        self.etiqueta(f"Puntaje obtenido: {self.puntaje}", 14, pady=10)
        self.etiqueta(f"Tiempo total: {total:.2f} segundos", 14, pady=10)
        tk.Button(self.root, text="Jugar de nuevo", font=(FUENTE, 12),
                  command=self.inicio).pack(pady=25)


if __name__ == "__main__":
    ventana = tk.Tk()
    Quiz(ventana)
    ventana.mainloop()