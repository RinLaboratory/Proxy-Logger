import tkinter as tk
import multiprocessing
from tkinter import ttk
from queue import Queue, Empty
from tkinter import messagebox


def WAIT_FOR_PROCESS(
    process: list[multiprocessing.Process],
    progress_queues: list[Queue],
    progress_var: tk.DoubleVar,
    importar_window: tk.Toplevel,
    iniciar_button: ttk.Button,
    carpeta_button: ttk.Button,
    total_files: int,  # Número total de archivos a procesar
):
    # Total de archivos procesados por todos los procesos
    total_processed_files = 0

    # Actualizar la barra de progreso mientras se reciben actualizaciones desde las colas
    while any(import_process.is_alive() for import_process in process):
        for i, import_process in enumerate(process):
            try:
                progress: int = progress_queues[i].get_nowait()
                total_processed_files += progress

                # Calcular el progreso global
                global_progress = (total_processed_files * 100) // total_files
                progress_var.set(global_progress)
                print(
                    "progreso global: "
                    + str(global_progress)
                    + " | archivos procesados: "
                    + str(total_processed_files)
                    + " | total de archivos: "
                    + str(total_files)
                )
                importar_window.update_idletasks()
            except Empty:
                pass  # La cola está vacía, continuar

    # Esperar a que todos los process terminen
    for p in process:
        p.join()

    # Rehabilitar botones
    iniciar_button.config(state="normal")
    carpeta_button.config(state="normal")

    messagebox.showinfo("Importar", "Importación completada.")
    progress_var.set(0)
    importar_window.update_idletasks()
