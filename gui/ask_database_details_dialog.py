import tkinter as tk
from tkinter import ttk
from database.check_connection_database import CHECK_DATABASE


def ASK_DATABASE_DETAILS_DIALOG():
    global root, entry_connection_string
    root = tk.Tk()
    root.title("Configuración de MongoDB")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, padx=10, pady=10)

    label = ttk.Label(frame, text="Ingrese el connection string de MongoDB:")
    label.grid(row=0, column=0, padx=5, pady=5)

    entry_connection_string = ttk.Entry(frame, width=50)
    entry_connection_string.grid(row=1, column=0, padx=5, pady=5)

    button_accept = ttk.Button(
        frame,
        text="Aceptar",
        command=lambda: CHECK_DATABASE(entry_connection_string, root),
    )
    button_accept.grid(row=2, column=0, padx=5, pady=5)

    root.mainloop()
