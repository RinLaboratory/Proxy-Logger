import tkinter as tk
import multiprocessing
from tkinter import ttk
from queue import Queue, Empty
from tkinter import messagebox
from utils.types import TypesInsertedData, TypesConfig
from database.get_database import GET_DATABASE
from log_processing.processInsertData import PROCESS_INSERT_DATA


def WAIT_FOR_PROCESS(
    config: TypesConfig,
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

    unprocessedInsertData: TypesInsertedData = {
        "player": [],
        "ip_address": [],
        "player_ip": [],
        "file": [],
        "activity": [],
    }

    # Actualizar la barra de progreso mientras se reciben actualizaciones desde las colas
    while any(import_process.is_alive() for import_process in process):
        for i, import_process in enumerate(process):
            try:
                progress: int
                insertData: TypesInsertedData
                progress, insertData = progress_queues[i].get_nowait()

                if progress == 1:
                    total_processed_files += 1

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
                else:
                    unprocessedInsertData["activity"] = (
                        unprocessedInsertData["activity"] + insertData["activity"]
                    )
                    unprocessedInsertData["file"] = (
                        unprocessedInsertData["file"] + insertData["file"]
                    )
                    unprocessedInsertData["ip_address"] = (
                        unprocessedInsertData["ip_address"] + insertData["ip_address"]
                    )
                    unprocessedInsertData["player"] = (
                        unprocessedInsertData["player"] + insertData["player"]
                    )
                    unprocessedInsertData["player_ip"] = (
                        unprocessedInsertData["player_ip"] + insertData["player_ip"]
                    )

            except Empty:
                pass  # La cola está vacía, continuar

    # Esperar a que todos los process terminen
    for p in process:
        p.join()

    print("procesando...")
    processedInsertData = PROCESS_INSERT_DATA(unprocessedInsertData)

    db = GET_DATABASE(config["mongodb_connection_string"])

    print("insertando en mongo...")
    db["player"].insert_many(processedInsertData["player"], ordered=False)
    db["ip_address"].insert_many(processedInsertData["ip_address"], ordered=False)
    db["player_ip"].insert_many(processedInsertData["player_ip"], ordered=False)
    db["file"].insert_many(processedInsertData["file"], ordered=False)
    db["activity"].insert_many(processedInsertData["activity"], ordered=False)

    # Rehabilitar botones
    iniciar_button.config(state="normal")
    carpeta_button.config(state="normal")

    messagebox.showinfo("Importar", "Importación completada.")
    progress_var.set(0)
    importar_window.update_idletasks()
