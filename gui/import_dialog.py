import sqlite3
import tkinter as tk
from tkinter import ttk

from thread.import_thread import IMPORT_THREAD
from file.select_folder import SELECT_IMPORT_FOLDER


def IMPORT(root: tk.Tk, cur: sqlite3.Cursor):
    # Crear ventana secundaria
    importar_window = tk.Toplevel(root)
    importar_window.title("Importar Logs")
    importar_window.attributes("-topmost", True)  # Mantener la ventana en primer plano
    importar_window.resizable(False, False)

    # Frame principal
    frame_importar = ttk.Frame(importar_window, padding="10")
    frame_importar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    carpeta_label = ttk.Label(frame_importar, text="Seleccione la carpeta de logs:")
    carpeta_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    carpeta_entry_var = tk.StringVar()
    carpeta_entry = ttk.Entry(frame_importar, textvariable=carpeta_entry_var, width=50)
    carpeta_entry.grid(row=1, column=0, padx=5, pady=5, sticky="we")

    carpeta_button = ttk.Button(
        frame_importar,
        text="Seleccionar carpeta",
        command=lambda: SELECT_IMPORT_FOLDER(importar_window, carpeta_entry_var),
    )
    carpeta_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Checkboxes
    proxy_type_var = tk.StringVar(value="bungeecord")
    bungeecord_checkbox = ttk.Radiobutton(
        frame_importar,
        text="Bungeecord",
        variable=proxy_type_var,
        value="bungeecord",
    )
    bungeecord_checkbox.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    velocity_checkbox = ttk.Radiobutton(
        frame_importar, text="Velocity", variable=proxy_type_var, value="velocity"
    )
    velocity_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    # Barra de progreso
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(frame_importar, variable=progress_var, maximum=100)
    progress_bar.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Botón de iniciar importación
    iniciar_button = ttk.Button(
        frame_importar,
        text="Iniciar Importación",
        command=lambda: IMPORT_THREAD(
            cur,
            carpeta_entry_var,
            proxy_type_var,
            progress_var,
            importar_window,
            iniciar_button,
            carpeta_button,
        ),
    )
    iniciar_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="e")

    # Configurar el tamaño de las filas y columnas
    importar_window.rowconfigure(0, weight=1)
    importar_window.columnconfigure(0, weight=1)
    frame_importar.rowconfigure(0, weight=1)
    frame_importar.columnconfigure(0, weight=1)
