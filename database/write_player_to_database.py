from pymongo.database import Database
from log_processing.get_log_hours import GET_LOG_DATEHOURS


def WRITE_PLAYER_TO_DATABASE(
    db: Database,
    line: str,
    log_filename: str,
    log_file_id: int,
    loadedPlayers: list[tuple[str, int]],
    loadedIPs: list[tuple[str, int]],
    loadedPlayerIPs: list[tuple[int, int]],
):
    try:
        if (line.startswith("[") and "[connected player]") in line:
            log_datetime = GET_LOG_DATEHOURS(line, log_filename)
            splited_line = line.split()
            playername = splited_line[splited_line.index("player]") + 1]
            ip_and_port: list[str] = splited_line[
                splited_line.index("player]") + 2
            ].split("/")
            ip = ip_and_port[1].split(":")[0]

            # Using dictionaries for faster lookups
            loadedIPs_dict = {ip: id for ip, id in loadedIPs}
            loadedPlayers_dict = {player: id for player, id in loadedPlayers}
            loadedPlayerIPs_set = set(
                (player_id, ip_id) for player_id, ip_id in loadedPlayerIPs
            )

            inserted_ip_address_id = ""
            inserted_playername_id = ""

            ip_address_isPresent = loadedIPs_dict.get(ip)
            playername_isPresent = loadedPlayers_dict.get(playername)

            if ip_address_isPresent is not None:
                inserted_ip_address_id = ip_address_isPresent
            else:
                inserted_ip_address_result = db["ip_address"].insert_one(
                    {"ip": str(ip)}
                )
                inserted_ip_address_id = inserted_ip_address_result.inserted_id
                loadedIPs.append([ip, inserted_ip_address_id])

            if playername_isPresent is not None:
                inserted_playername_id = playername_isPresent
            else:
                inserted_playername_result = db["player"].insert_one(
                    {"playername": str(playername)}
                )
                inserted_playername_id = inserted_playername_result.inserted_id
                loadedPlayers.append([playername, inserted_playername_id])

            db["activity"].insert_one(
                {
                    "text": "".join(line),
                    "player_id": inserted_playername_id,
                    "timestamp": log_datetime,
                    "file_id": log_file_id,
                }
            )

            if (
                inserted_playername_id,
                inserted_ip_address_id,
            ) not in loadedPlayerIPs_set:
                db["player_ip"].insert_one(
                    {
                        "player_id": inserted_playername_id,
                        "ip_id": inserted_ip_address_id,
                    }
                )
                loadedPlayerIPs.append([inserted_playername_id, inserted_ip_address_id])

        elif (line.startswith("[") and "[server connection]") in line:
            log_datetime = GET_LOG_DATEHOURS(line, log_filename)
            splited_line = line.split()
            playername = splited_line[splited_line.index("connection]") + 1]

            inserted_playername_id = 0

            loadedPlayers_dict = {player: id for player, id in loadedPlayers}
            playername_isPresent = loadedPlayers_dict.get(playername)

            if playername_isPresent is not None:
                inserted_playername_id = playername_isPresent
            else:
                inserted_playername_result = db["player"].insert_one(
                    {"playername": str(playername)}
                )
                inserted_playername_id = inserted_playername_result.inserted_id
                loadedPlayers.append([playername, inserted_playername_id])

            db["activity"].insert_one(
                {
                    "text": "".join(line),
                    "player_id": inserted_playername_id,
                    "timestamp": log_datetime,
                    "file_id": log_file_id,
                }
            )

        elif line.startswith("[") and "[nlogin]" in line:
            if (
                "has successfully logged in." in line
                or "has successfully registered." in line
            ):
                log_datetime = GET_LOG_DATEHOURS(line, log_filename)
                splited_line = line.split()
                playername = splited_line[splited_line.index("user") + 1]

                loadedPlayers_dict = {player: id for player, id in loadedPlayers}
                playername_isPresent = loadedPlayers_dict.get(playername)
                inserted_playername_id = ""

                if playername_isPresent is not None:
                    inserted_playername_id = playername_isPresent
                else:
                    inserted_playername_result = db["player"].insert_one(
                        {"playername": str(playername)}
                    )
                    inserted_playername_id = inserted_playername_result.inserted_id
                    loadedPlayers.append([playername, inserted_playername_id])

                db["activity"].insert_one(
                    {
                        "text": "".join(line),
                        "player_id": inserted_playername_id,
                        "timestamp": log_datetime,
                        "file_id": log_file_id,
                    }
                )

    except Exception as e:
        print(f"Error processing line: {line}")
        print(e)
