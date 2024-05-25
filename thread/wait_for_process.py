import tkinter as tk
import multiprocessing
from tkinter import ttk
from queue import Queue, Empty
from tkinter import messagebox
from pymongo import DESCENDING
from utils.types import TypesInsertedData, TypesConfig, TypesLoadedData
from database.get_database import GET_DATABASE
from log_processing.process_insert_data import PROCESS_INSERT_DATA


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

    unprocessed_insert_data: TypesInsertedData = {
        "player": [],
        "ip_address": [],
        "file": [],
        "activity": [],
    }

    # Actualizar la barra de progreso mientras se reciben actualizaciones desde las colas
    while any(import_process.is_alive() for import_process in process):
        for i, import_process in enumerate(process):
            try:
                progress: int
                insert_data: TypesInsertedData
                progress, insert_data = progress_queues[i].get_nowait()

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
                    unprocessed_insert_data["activity"] = (
                        unprocessed_insert_data["activity"] + insert_data["activity"]
                    )
                    unprocessed_insert_data["file"] = (
                        unprocessed_insert_data["file"] + insert_data["file"]
                    )
                    unprocessed_insert_data["ip_address"] = (
                        unprocessed_insert_data["ip_address"] + insert_data["ip_address"]
                    )
                    unprocessed_insert_data["player"] = (
                        unprocessed_insert_data["player"] + insert_data["player"]
                    )
            except Empty:
                pass  # La cola está vacía, continuar

    # Esperar a que todos los process terminen
    for p in process:
        p.join()

    print("procesando...")
    processed_insert_data = PROCESS_INSERT_DATA(unprocessed_insert_data)

    db = GET_DATABASE(config["mongodb_connection_string"])

    print("insertando en mongo...")
    if len(processed_insert_data["player"]) > 0:
        db["player"].insert_many(processed_insert_data["player"], ordered=False)
    else:
        print("ignored insert_many in player collection as processed data it was empty")
    if len(processed_insert_data["ip_address"]) > 0:
        db["ip_address"].insert_many(processed_insert_data["ip_address"], ordered=False)
    else:
        print(
            "ignored insert_many in ip_address collection as processed data it was empty"
        )
    if len(processed_insert_data["file"]) > 0:
        db["file"].insert_many(processed_insert_data["file"], ordered=False)
    else:
        print("ignored insert_many in file collection as processed data it was empty")
    if len(processed_insert_data["activity"]) > 0:
        db["activity"].insert_many(processed_insert_data["activity"], ordered=False)
    else:
        print(
            "ignored insert_many in activity collection as processed data it was empty"
        )
    
    db["activity"].create_index([('subplayername', DESCENDING)])
    db["ip_address"].create_index([('subplayername', DESCENDING), ('ip', DESCENDING)])
    db["player"].create_index([('subplayername', DESCENDING)])

    # Rehabilitar botones
    iniciar_button.config(state="normal")
    carpeta_button.config(state="normal")

    messagebox.showinfo("Importar", "Importación completada.")
    progress_var.set(0)
    importar_window.update_idletasks()
