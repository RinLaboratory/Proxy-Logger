import tkinter as tk
from tkinter import ttk
from pymongo.database import Database
from database.search_from_database import SEARCH
from gui.import_dialog import IMPORT


def CREATE_GUI(db: Database):
    # Crear ventana principal
    root = tk.Tk()
    root.title("Interfaz de Usuario")

    # Frame principal
    frame_principal = ttk.Frame(root, padding="10")
    frame_principal.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Label y campo de entrada
    label_input = ttk.Label(
        frame_principal,
        text="Ingrese nombre de usuario o dirección IP:",
        justify="left",
    )
    label_input.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_input = ttk.Entry(frame_principal, width=30, justify="left")
    entry_input.grid(row=1, column=0, padx=5, pady=5, sticky="we")

    # Botones
    button_buscar = ttk.Button(
        frame_principal,
        text="Buscar",
        command=lambda: SEARCH(db, entry_input, tree_logs, tree_dupeip, tree_alts),
    )
    button_buscar.grid(row=1, column=1, padx=5, pady=5)
    button_importar = ttk.Button(
        frame_principal, text="Importar", command=lambda: IMPORT(root, db)
    )
    button_importar.grid(row=1, column=2, padx=5, pady=5)

    # Frame para las tablas
    frame_tablas = ttk.Frame(frame_principal, padding="10")
    frame_tablas.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    # Tabla de logs relacionados
    label_logs = ttk.Label(frame_tablas, text="Logs relacionados")
    label_logs.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    columns = ("Fecha", "Actividad")
    tree_logs = ttk.Treeview(frame_tablas, columns=columns, show="headings")
    for col in columns:
        tree_logs.heading(col, text=col)
        if col == "Fecha":
            tree_logs.column(col, width=130, anchor="w", stretch=tk.NO)
        else:
            tree_logs.column(col, width=1000, anchor="w", stretch=tk.NO)
    tree_logs.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    # Barra de desplazamiento para la tabla de logs
    scroll_logs = ttk.Scrollbar(
        frame_tablas, orient="vertical", command=tree_logs.yview
    )
    scroll_logs.grid(row=1, column=1, sticky="nse")
    tree_logs.config(yscrollcommand=scroll_logs.set)

    # Barra de desplazamiento horizontal para la tabla de logs
    scroll_logs_horizontal = ttk.Scrollbar(
        frame_tablas, orient="horizontal", command=tree_logs.xview
    )
    scroll_logs_horizontal.grid(row=2, column=0, sticky="ew")
    tree_logs.config(xscrollcommand=scroll_logs_horizontal.set)

    # Tabla de IPs duplicadas
    label_dupeip = ttk.Label(frame_tablas, text="DupeIP")
    label_dupeip.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    columns_dupeip = "Jugador/IP"
    tree_dupeip = ttk.Treeview(frame_tablas, columns=columns_dupeip, show="headings")
    tree_dupeip.heading(columns_dupeip, text=col)
    tree_dupeip.column(columns_dupeip, width=140, anchor="w")
    tree_dupeip.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

    scroll_dupeip = ttk.Scrollbar(
        frame_tablas, orient="vertical", command=tree_dupeip.yview
    )
    scroll_dupeip.grid(row=1, column=3, sticky="ns")
    tree_dupeip.config(yscrollcommand=scroll_dupeip.set)

    # Barra de desplazamiento horizontal para la tabla de logs
    scroll_dupeip_horizontal = ttk.Scrollbar(
        frame_tablas, orient="horizontal", command=tree_dupeip.xview
    )
    scroll_dupeip_horizontal.grid(row=2, column=2, sticky="ew")
    tree_dupeip.config(xscrollcommand=scroll_dupeip_horizontal.set)

    # Tabla de historial
    label_alts = ttk.Label(frame_tablas, text="Historial")
    label_alts.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    columns_alts = "Jugador/IP"
    tree_alts = ttk.Treeview(frame_tablas, columns=columns_alts, show="headings")

    tree_alts.heading(columns_alts, text=col)
    tree_alts.column(columns_alts, width=140, anchor="w")
    tree_alts.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

    scroll_alts = ttk.Scrollbar(
        frame_tablas, orient="vertical", command=tree_alts.yview
    )
    scroll_alts.grid(row=1, column=4, sticky="ns")
    tree_alts.config(yscrollcommand=scroll_alts.set)

    # Barra de desplazamiento horizontal para la tabla de logs
    scroll_alts_horizontal = ttk.Scrollbar(
        frame_tablas, orient="horizontal", command=tree_alts.xview
    )
    scroll_alts_horizontal.grid(row=2, column=3, sticky="ew")
    tree_alts.config(xscrollcommand=scroll_alts_horizontal.set)

    # Configurar el tamaño de las filas y columnas
    frame_principal.rowconfigure(1, weight=3)
    frame_principal.columnconfigure(0, weight=1)
    frame_tablas.rowconfigure(1, weight=1, minsize=500)

    # Configurar la tabla para ajustar automáticamente el tamaño de las columnas y la vista
    def resize_columns(event):
        tree_logs.update_idletasks()

    frame_tablas.bind("<Configure>", resize_columns)

    # Ejecutar la aplicación
    root.mainloop()
