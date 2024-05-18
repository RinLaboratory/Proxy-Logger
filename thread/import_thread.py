import os
import threading
import tkinter as tk
from queue import Queue, Empty
from tkinter import ttk
from pymongo.database import Database
from tkinter import messagebox
from file.import_from_files import IMPORT_FROM_FILES
from thread.wait_for_threads import WAIT_FOR_THREADS
from database.load_database import LOAD_DATABASE_BEFORE_NEW_IMPORT


def IMPORT_THREAD(
    db: Database,
    carpeta_entry_var: tk.StringVar,
    proxy_type_var: tk.StringVar,
    progress_var: tk.DoubleVar,
    importar_window: tk.Toplevel,
    iniciar_button: ttk.Button,
    carpeta_button: ttk.Button,
):
    queue = Queue()
    loadedPlayers: list[tuple[str, int]] = []
    loadedIPs: list[tuple[str, int]] = []
    loadedPlayerIPs: list[tuple[int, int]] = []
    loadedHashes: list[tuple[str, str, int]] = []

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

    LOAD_DATABASE_BEFORE_NEW_IMPORT(
        db, loadedPlayers, loadedIPs, loadedPlayerIPs, loadedHashes
    )
    list_logs_files = os.listdir(carpeta)

    total_files = len(list_logs_files)
    num_threads = 3

    # Lista para almacenar los threads
    threads: list[threading.Thread] = []

    # Crear tres colas para el progreso, una por cada hilo
    progress_queues: list[Queue] = [queue for _ in range(num_threads)]

    # Calcula cuántos archivos leerá cada thread
    files_per_thread = total_files // num_threads

    # Crear y comenzar 3 threads
    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = (
            start_index + files_per_thread if i < num_threads - 1 else total_files
        )
        thread_files = list_logs_files[start_index:end_index]

        import_thread = threading.Thread(
            target=IMPORT_FROM_FILES,
            args=(
                db,
                thread_files,
                proxy_type,
                carpeta,
                progress_queues[i],
                loadedPlayers,
                loadedIPs,
                loadedPlayerIPs,
                loadedHashes,
                i,
            ),
        )
        threads.append(import_thread)
        import_thread.start()

    # iniciar cuarto thread para actualizar la info de la gui sin atascarse
    wait_for_threads = threading.Thread(
        target=WAIT_FOR_THREADS,
        args=(
            threads,
            progress_queues,
            progress_var,
            importar_window,
            iniciar_button,
            carpeta_button,
        ),
    )
    wait_for_threads.start()
