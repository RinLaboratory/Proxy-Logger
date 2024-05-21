from bson import objectid
from utils.types import TypesLoadedData, TypesInsertedData
from log_processing.get_log_hours import GET_LOG_DATEHOURS


def WRITE_PLAYER_TO_DATABASE(
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
            ip_and_port: list[str] = splited_line[
                splited_line.index("player]") + 2
            ].split("/")
            ip = ip_and_port[1].split(":")[0]

            inserted_ip_address_id: objectid.ObjectId = ""
            inserted_playername_id: objectid.ObjectId = ""

            ip_address_isPresent = loadedData["ip_address"].get(ip)
            playername_isPresent = loadedData["player"].get(playername)

            if ip_address_isPresent is not None:
                # La ip está presente desde antes
                inserted_ip_address_id = ip_address_isPresent[1]
            else:
                # La ip no está presente y se debe ingresar en la db
                # Creación del objeto
                inserted_ip_address_id = objectid.ObjectId()
                insertData["ip_address"].append(
                    {
                        "_id": inserted_ip_address_id,
                        "ip": ip,
                    }
                )

            if playername_isPresent is not None:
                # El jugador está presente desde antes
                inserted_playername_id = playername_isPresent[1]
            else:
                # El jugador no está presente y se debe ingresar en la db
                # Creación del objeto
                inserted_playername_id = objectid.ObjectId()
                insertData["player"].append(
                    {"_id": inserted_playername_id, "playername": playername}
                )

            insertData["activity"].append(
                {
                    "_id": objectid.ObjectId(),
                    "file_id": log_file_id,
                    "player_id": inserted_playername_id,
                    "text": "".join(line),
                    "timestamp": log_datetime,
                }
            )

            player_ip_isPresent = -1
            if (inserted_ip_address_id, inserted_playername_id) in loadedData[
                "player_ip"
            ]:
                player_ip_isPresent = 1

            if player_ip_isPresent == -1:
                # No está presente
                insertData["player_ip"].append(
                    {
                        "_id": objectid.ObjectId(),
                        "ip_id": inserted_ip_address_id,
                        "player_id": inserted_playername_id,
                    }
                )

        elif line.startswith("[") and ("[server connection]" in line):
            log_datetime = GET_LOG_DATEHOURS(line, log_filename)
            splited_line = line.split()
            playername = splited_line[splited_line.index("connection]") + 1]

            inserted_playername_id: objectid.ObjectId = ""

            playername_isPresent = loadedData["player"].get(playername)

            if playername_isPresent is not None:
                # El jugador está presente desde antes
                inserted_playername_id = playername_isPresent[1]
            else:
                # El jugador no está presente y se debe ingresar en la db
                # Creación del objeto
                inserted_playername_id = objectid.ObjectId()
                insertData["player"].append(
                    {"_id": inserted_playername_id, "playername": playername}
                )

            insertData["activity"].append(
                {
                    "_id": objectid.ObjectId(),
                    "file_id": log_file_id,
                    "player_id": inserted_playername_id,
                    "text": "".join(line),
                    "timestamp": log_datetime,
                }
            )

        elif line.startswith("[") and ("[nlogin]" in line):
            if (
                "has successfully logged in." in line
                or "has successfully registered." in line
            ):
                log_datetime = GET_LOG_DATEHOURS(line, log_filename)
                splited_line = line.split()
                playername = splited_line[splited_line.index("user") + 1]

                inserted_playername_id: objectid.ObjectId = ""
                playername_isPresent = loadedData["player"].get(playername)

                if playername_isPresent is not None:
                    # El jugador está presente desde antes
                    inserted_playername_id = playername_isPresent[1]
                else:
                    # El jugador no está presente y se debe ingresar en la db
                    # Creación del objeto
                    inserted_playername_id = objectid.ObjectId()
                    insertData["player"].append(
                        {"_id": inserted_playername_id, "playername": playername}
                    )

                insertData["activity"].append(
                    {
                        "_id": objectid.ObjectId(),
                        "file_id": log_file_id,
                        "player_id": inserted_playername_id,
                        "text": "".join(line),
                        "timestamp": log_datetime,
                    }
                )

    except Exception as e:
        print(f"Error processing line: {line}")
        print(e)
        print(f"Ignoring invalid line.")
