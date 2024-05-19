import os
import threading
import tkinter as tk
import multiprocessing
from tkinter import ttk
from tkinter import messagebox
from file.import_from_files import IMPORT_FROM_FILES
from multiprocess.wait_for_process import WAIT_FOR_PROCESS


def IMPORT_PROCESS(
    carpeta_entry_var: tk.StringVar,
    proxy_type_var: tk.StringVar,
    progress_var: tk.DoubleVar,
    importar_window: tk.Toplevel,
    iniciar_button: ttk.Button,
    carpeta_button: ttk.Button,
    config: dict[str, str],
):
    # Deshabilitar botones
    iniciar_button.config(state="disabled")
    carpeta_button.config(state="disabled")

    carpeta = carpeta_entry_var.get()

    if not carpeta:
        messagebox.showerror("Error", "Seleccione una carpeta.")
        # Rehabilitar botones
        iniciar_button.config(state="normal")
        carpeta_button.config(state="normal")
        return
    proxy_type = proxy_type_var.get()
    messagebox.showinfo(
        "Importar",
        f"Iniciando importación desde {carpeta} con tipo {proxy_type}.",
    )

    list_logs_files = os.listdir(carpeta)

    total_files = len(list_logs_files)

    # Dejamos que la cpu respire con 1 core para maximizar el rendimiento.
    # Sin matar a la pc
    num_process: int = os.cpu_count() - 1

    # Lista para almacenar los procesos
    process: list[multiprocessing.Process] = []

    # Crear colas para el progreso, una por cada proceso
    progress_queues: list[multiprocessing.Queue] = [
        multiprocessing.Queue() for _ in range(num_process)
    ]

    # Calcula cuántos archivos leerá cada process
    files_per_process = total_files // num_process

    # Crear y comenzar los procesos
    for i in range(num_process):
        start_index = i * files_per_process
        end_index = (
            start_index + files_per_process if i < num_process - 1 else total_files
        )
        process_files = list_logs_files[start_index:end_index]

        import_process = multiprocessing.Process(
            target=IMPORT_FROM_FILES,
            args=(
                config,
                process_files,
                proxy_type,
                carpeta,
                progress_queues[i],
            ),
        )
        process.append(import_process)
        import_process.start()

    # iniciar thread para actualizar la info de la gui sin atascarse
    wait_for_threads = threading.Thread(
        target=WAIT_FOR_PROCESS,
        args=(
            process,
            progress_queues,
            progress_var,
            importar_window,
            iniciar_button,
            carpeta_button,
            total_files,
        ),
    )
    wait_for_threads.start()
