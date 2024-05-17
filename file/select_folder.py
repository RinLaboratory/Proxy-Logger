from tkinter import filedialog


# Campo de selección de carpeta
def SELECT_IMPORT_FOLDER(importar_window, carpeta_entry_var):
    importar_window.attributes("-topmost", False)
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_entry_var.set(carpeta)
    importar_window.attributes("-topmost", True)
