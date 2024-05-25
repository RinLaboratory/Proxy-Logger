from bson import objectid
from utils.types import TypesLoadedData, TypesInsertedData
from log_processing.get_log_hours import GET_LOG_DATEHOURS


def PROCESS_LOG_DATA_VELOCITY(
    line: str,
    log_filename: str,
    log_file_id: objectid.ObjectId,
    insertData: TypesInsertedData,
    loadedData: TypesLoadedData,
):
    try:
        if line.startswith("[") and ("[connected player]" in line):
            log_datetime = GET_LOG_DATEHOURS(line, log_filename)
            splited_line = line.split()
            playername = splited_line[splited_line.index("player]") + 1]
            playername_lower = playername.lower()
            ip_and_port: list[str] = splited_line[
                splited_line.index("player]") + 2
            ].split("/")
            ip = ip_and_port[1].split(":")[0]

            playername_isPresent = loadedData["player"].get(playername_lower)
            ip_isPresent = loadedData["ip_address"].get(ip + playername_lower)

            if playername_isPresent is not None:
                # El jugador está presente desde antes
                inserted_playername = playername_isPresent[0]
            else:
                # El jugador no está presente y se debe ingresar en la db
                inserted_playername = playername_lower
                insertData["player"].append(
                    {"playername": playername, "subplayername": playername_lower}
                )

            if ip_isPresent is None:
                insertData["ip_address"].append(
                    {"ip": ip, "subplayername": inserted_playername}
                )

            insertData["activity"].append(
                {
                    "_id": objectid.ObjectId(),
                    "file_id": log_file_id,
                    "text": "".join(line),
                    "timestamp": log_datetime,
                    "subplayername": playername_lower,
                }
            )

        elif line.startswith("[") and ("[server connection]" in line):
            log_datetime = GET_LOG_DATEHOURS(line, log_filename)
            splited_line = line.split()
            playername = splited_line[splited_line.index("connection]") + 1]
            playername_lower = playername.lower()

            playername_isPresent = loadedData["player"].get(playername_lower)

            if playername_isPresent is not None:
                # El jugador está presente desde antes
                inserted_playername = playername_isPresent[0]
            else:
                # El jugador no está presente y se debe ingresar en la db
                inserted_playername = playername_lower
                insertData["player"].append(
                    {"playername": playername, "subplayername": playername_lower}
                )

            insertData["activity"].append(
                {
                    "_id": objectid.ObjectId(),
                    "file_id": log_file_id,
                    "text": "".join(line),
                    "timestamp": log_datetime,
                    "subplayername": playername_lower,
                }
            )

        elif line.startswith("[") and ("[nlogin]" in line):
            if (
                "has successfully logged in." in line
                or "has successfully registered." in line
                or "logged in automatically" in line
            ):
                log_datetime = GET_LOG_DATEHOURS(line, log_filename)
                splited_line = line.split()
                playername = splited_line[splited_line.index("user") + 1]
                playername_lower = playername.lower()

                playername_isPresent = loadedData["player"].get(playername_lower)

                if playername_isPresent is not None:
                    # El jugador está presente desde antes
                    inserted_playername = playername_isPresent[0]
                else:
                    # El jugador no está presente y se debe ingresar en la db
                    inserted_playername = playername_lower
                    insertData["player"].append(
                        {"playername": playername, "subplayername": playername_lower}
                    )

                insertData["activity"].append(
                    {
                        "_id": objectid.ObjectId(),
                        "file_id": log_file_id,
                        "text": "".join(line),
                        "timestamp": log_datetime,
                        "subplayername": playername_lower,
                    }
                )

    except Exception as e:
        print(f"Error processing line: {line}")
        print(e)
        print(f"Ignoring invalid line.")
