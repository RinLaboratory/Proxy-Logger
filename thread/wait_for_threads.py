import threading
import tkinter as tk
from tkinter import ttk
from queue import Queue, Empty
from tkinter import messagebox


def WAIT_FOR_THREADS(
    threads: list[threading.Thread],
    progress_queues: list[Queue],
    progress_var: tk.DoubleVar,
    importar_window: tk.Toplevel,
    iniciar_button: ttk.Button,
    carpeta_button: ttk.Button,
):
    # Actualizar la barra de progreso mientras se reciben actualizaciones desde las colas
    while any(import_thread.is_alive() for import_thread in threads):
        for i, import_thread in enumerate(threads):
            try:
                progress: int = progress_queues[i].get_nowait()
                # Actualizar la barra de progreso correspondiente
                # (puedes tener tres barras de progreso o combinarlas en una)
                progress_var.set(progress)
                importar_window.update_idletasks()
            except Empty:
                pass  # La cola está vacía, continuar

    # Esperar a que todos los threads terminen
    for thread in threads:
        thread.join()

    # Rehabilitar botones
    iniciar_button.config(state="normal")
    carpeta_button.config(state="normal")

    messagebox.showinfo("Importar", "Importación completada.")
    progress_var.set(0)
    importar_window.update_idletasks()
