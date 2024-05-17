import os
import sqlite3
import threading
import tkinter as tk
from queue import Queue
from tkinter import ttk
from tkinter import messagebox
from file.import_from_files import IMPORT_FROM_FILES
from database.load_database import LOAD_DATABASE_BEFORE_NEW_IMPORT


def IMPORT_THREAD(
    cur: sqlite3.Cursor,
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
        cur, loadedPlayers, loadedIPs, loadedPlayerIPs, loadedHashes
    )
    list_logs_files = os.listdir(carpeta)

    # Crear tres colas para el progreso, una por cada hilo
    queue = Queue()

    import_thread = threading.Thread(
        target=IMPORT_FROM_FILES,
        args=(
            list_logs_files,
            proxy_type,
            carpeta,
            queue,
            loadedPlayers,
            loadedIPs,
            loadedPlayerIPs,
            loadedHashes,
            progress_var,
            importar_window,
            iniciar_button,
            carpeta_button,
        ),
    )
    import_thread.start()
