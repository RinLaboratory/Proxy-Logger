import threading
from tkinter import ttk
from tkinter import messagebox
from pymongo.database import Database
from thread.search_in_database import SEARCH_IN_DATABASE


def SEARCH(
    db: Database,
    entry_input: ttk.Entry,
    tree_logs: ttk.Treeview,
    tree_dupeip: ttk.Treeview,
    tree_alts: ttk.Treeview,
    button_buscar: ttk.Button,
):
    button_buscar.config(state="disabled")

    # Aquí implementarás la lógica para buscar según el nombre de usuario o dirección IP
    search_bar_text = entry_input.get()
    print(search_bar_text)

    # Borrar todos los elementos de las tablas
    for i in tree_logs.get_children():
        tree_logs.delete(i)
    for i in tree_dupeip.get_children():
        tree_dupeip.delete(i)

    if search_bar_text == "" or search_bar_text is None:
        messagebox.showerror("Error", "No hay nada que buscar.")
        button_buscar.config(state="normal")
        return

    # iniciar thread para actualizar la info de la gui sin atascarse
    wait_for_threads = threading.Thread(
        target=SEARCH_IN_DATABASE,
        args=(
            db,
            search_bar_text,
            tree_logs,
            tree_dupeip,
            tree_alts,
            button_buscar,
        ),
    )
    wait_for_threads.start()
