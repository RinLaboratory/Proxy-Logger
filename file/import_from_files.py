import hashlib
import multiprocessing
from bson import objectid
from file.read_file import READ_FILE
from utils.types import TypesLoadedData, TypesInsertedData
from log_processing.process_log_data_velocity import PROCESS_LOG_DATA_VELOCITY
from log_processing.process_log_data_bungeecord import PROCESS_LOG_DATA_BUNGEECORD


def IMPORT_FROM_FILES(
    list_logs_files: list[str],
    proxy_type: str,
    directory: str,
    progress_queue: multiprocessing.Queue,
    loaded_data: TypesLoadedData,
):
    insert_data: TypesInsertedData = {
        "player": [],
        "ip_address": [],
        "player_ip": [],
        "file": [],
        "activity": [],
    }

    for index, log_file in enumerate(list_logs_files):
        # print("[Queue " + str(queue_number) + "] " + log_file)
        file_lines = READ_FILE(directory + "\\" + log_file)

        # Hashear el archivo para ver su registro
        hash_obj = hashlib.new("sha256")
        hash_obj.update(str(file_lines).encode())
        file_hash = str(hash_obj.hexdigest())

        # cuando es == None significa que el hash no está presente.
        # Lo ideal es ignorar los archivos llamados latest.log porque todavia no
        # se manejan bien.
        fileIsLoaded = loaded_data["file"].get(file_hash)

        if log_file != "latest.log":
            if fileIsLoaded is None:
                # Creación del objeto
                log_file_id = objectid.ObjectId()
                insert_data["file"].append(
                    {
                        "_id": log_file_id,
                        "file_name": log_file,
                        "hash": file_hash,
                        "proxy_type": proxy_type,
                    }
                )

                for merged_line in file_lines:
                    if proxy_type == "velocity":
                        PROCESS_LOG_DATA_VELOCITY(
                            merged_line,
                            log_file,
                            log_file_id,
                            insert_data,
                            loaded_data,
                        )
                    else:
                        PROCESS_LOG_DATA_BUNGEECORD(
                            merged_line,
                            log_file,
                            log_file_id,
                            insert_data,
                            loaded_data,
                        )
            else:
                print("skipped file " + log_file + " as it was already loaded.")
        else:
            print("ignored latest.log")

        progress_queue.put((1, {}))
    progress_queue.put((100, insert_data))
