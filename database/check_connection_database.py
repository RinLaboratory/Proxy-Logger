import tkinter as tk
from tkinter import ttk

from tkinter import messagebox
from pymongo import MongoClient
from config.save_config import SAVE_CONFIG


def CHECK_CONNECTION_DATABASE(connection_string: str):
    """Intenta conectarse a MongoDB y retorna True si la conexión es exitosa, de lo contrario False."""
    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=2000)
        client.server_info()  # Esta línea intentará conectar y obtener información del servidor
        return True
    except Exception:
        return False


def CHECK_DATABASE(entry_connection_string: ttk.Entry, root: tk.Tk):
    connection_string = entry_connection_string.get()
    if CHECK_CONNECTION_DATABASE(connection_string):
        SAVE_CONFIG(connection_string)
        messagebox.showinfo(
            "Éxito",
            "Conexión exitosa y configuración guardada,\nVuelva a iniciar la aplicación.",
        )
        root.destroy()
    else:
        messagebox.showerror(
            "Error", "No se pudo conectar a MongoDB. Verifique el connection string."
        )
