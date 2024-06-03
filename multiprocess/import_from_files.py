import hashlib
import multiprocessing
from bson import objectid
from file.read_file import READ_FILE
from utils.types import TypesLoadedData, TypesInsertedData
from file.chech_file_is_from_latest_log import CHECK_FILE_IS_FROM_LATEST_LOG
from log_processing.process_log_data_velocity import PROCESS_LOG_DATA_VELOCITY
from log_processing.process_log_data_bungeecord import PROCESS_LOG_DATA_BUNGEECORD
from country_processing.parse_countries_as_dictionary import (
    PARSE_COUNTRIES_AS_DICTIONARY,
)


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
        "ip_record": [],
        "player_ip": [],
        "file": [],
        "activity": [],
        "latest_file": [],
        "latest_activity": [],
        "file_marked_for_deletion": [],
    }

    countries = PARSE_COUNTRIES_AS_DICTIONARY()

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

            if log_file == "latest.log":
                insert_data["latest_file"].append(
                    {
                        "_id": log_file_id,
                        "file_name": log_file,
                        "hash": file_hash,
                        "proxy_type": proxy_type,
                    }
                )
            else:
                latest_activity_comparison = CHECK_FILE_IS_FROM_LATEST_LOG(
                    loaded_data, file_lines, log_file
                )
                if latest_activity_comparison is not None:
                    insert_data["file_marked_for_deletion"].append(
                        latest_activity_comparison
                    )

            for merged_line in file_lines:
                if proxy_type == "velocity":
                    PROCESS_LOG_DATA_VELOCITY(
                        merged_line,
                        log_file,
                        log_file_id,
                        insert_data,
                        loaded_data,
                        countries,
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

        progress_queue.put((1, {}))
    progress_queue.put((100, insert_data))
