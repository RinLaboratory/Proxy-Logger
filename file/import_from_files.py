import hashlib
import tkinter as tk
from tkinter import ttk
from queue import Queue
from tkinter import messagebox
from utils.search import SEARCH_HASH
from file.read_file import READ_FILE
from pymongo.database import Database
from database.write_player_to_database import WRITE_PLAYER_TO_DATABASE


def IMPORT_FROM_FILES(
    db: Database,
    list_logs_files: list[str],
    proxy_type: str,
    directory: str,
    progress_queue: Queue,
    loadedPlayers: list[tuple[str, int]],
    loadedIPs: list[tuple[str, int]],
    loadedPlayerIPs: list[tuple[int, int]],
    loadedHashes: list[tuple[str, str, int]],
    queue_number: int,
):
    for index, log_file in enumerate(list_logs_files):
        print("[Queue " + str(queue_number) + "] " + log_file)
        file_lines = READ_FILE(directory + "\\" + log_file)

        # Hashear el archivo para ver su registro
        hash_obj = hashlib.new("sha256")
        hash_obj.update(str(file_lines).encode())
        file_hash = str(hash_obj.hexdigest())

        # Buscar el hash para ver si registrarlo o ignorarlo
        file_isPresent, file_name = SEARCH_HASH(file_hash, loadedHashes)

        # cuando es ==-1 significa que el hash no está presente.
        # Lo ideal es ignorar los archivos llamados latest.log porque todavia no
        # se manejan bien.
        if file_isPresent == -1 and file_name != "latest.log":
            log_file_result = db["file"].insert_one(
                {"filename": log_file, "proxy_type": proxy_type, "hash": file_hash}
            )
            log_file_id = log_file_result.inserted_id

            for merged_line in file_lines:
                WRITE_PLAYER_TO_DATABASE(
                    db,
                    merged_line,
                    log_file,
                    log_file_id,
                    loadedPlayers,
                    loadedIPs,
                    loadedPlayerIPs,
                )
        else:
            print("skipped file " + log_file + " as it was already loaded.")
        progress = ((index + 1) * 100) // len(list_logs_files)
        progress_queue.put(progress)
