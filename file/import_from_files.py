import hashlib
import multiprocessing
from file.read_file import READ_FILE
from database.get_database import GET_DATABASE
from database.write_player_to_database import WRITE_PLAYER_TO_DATABASE


def IMPORT_FROM_FILES(
    config: dict[str, str],
    list_logs_files: list[str],
    proxy_type: str,
    directory: str,
    progress_queue: multiprocessing.Queue,
):
    db = GET_DATABASE(config["mongodb_connection_string"])
    for index, log_file in enumerate(list_logs_files):
        # print("[Queue " + str(queue_number) + "] " + log_file)
        file_lines = READ_FILE(directory + "\\" + log_file)

        # Hashear el archivo para ver su registro
        hash_obj = hashlib.new("sha256")
        hash_obj.update(str(file_lines).encode())
        file_hash = str(hash_obj.hexdigest())

        # cuando es ==-1 significa que el hash no está presente.
        # Lo ideal es ignorar los archivos llamados latest.log porque todavia no
        # se manejan bien.
        if log_file != "latest.log":
            log_file_result = db["file"].update_one(
                {"hash": file_hash},
                {
                    "$set": {
                        "filename": log_file,
                        "proxy_type": proxy_type,
                        "hash": file_hash,
                    }
                },
                upsert=True,
            )
            log_file_id = log_file_result.upserted_id

            if log_file_id is not None:
                # El archivo es nuevo y se insertó en la db
                for merged_line in file_lines:
                    WRITE_PLAYER_TO_DATABASE(
                        db,
                        merged_line,
                        log_file,
                        log_file_id,
                    )
            else:
                print("skipped file " + log_file + " as it was already loaded.")
        else:
            print("ignored latest.log")

        progress_queue.put(1)
