from pymongo.database import Database
from log_processing.get_log_hours import GET_LOG_DATEHOURS


def WRITE_PLAYER_TO_DATABASE(
    db: Database,
    line: str,
    log_filename: str,
    log_file_id: int,
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

            inserted_ip_address_id = ""
            inserted_playername_id = ""

            ip_address_isPresent = db["ip_address"].update_one(
                {"ip": ip}, {"$set": {"ip": ip}}, upsert=True
            )

            playername_isPresent = db["player"].update_one(
                {"playername": playername},
                {"$set": {"playername": playername}},
                upsert=True,
            )

            if ip_address_isPresent.upserted_id is not None:
                # La ip es nueva y no está en la db
                inserted_ip_address_id = ip_address_isPresent.upserted_id
            else:
                # La ip está y se actualizó en la db
                inserted_ip_address_id = db["ip_address"].find_one({"ip": str(ip)})[
                    "_id"
                ]

            if playername_isPresent.upserted_id is not None:
                inserted_playername_id = playername_isPresent.upserted_id
            else:
                inserted_playername_id = db["player"].find_one(
                    {"playername": str(playername)}
                )["_id"]

            db["activity"].insert_one(
                {
                    "text": "".join(line),
                    "player_id": inserted_playername_id,
                    "timestamp": log_datetime,
                    "file_id": log_file_id,
                }
            )

            db["player_ip"].update_one(
                {"player_id": inserted_playername_id, "ip_id": inserted_ip_address_id},
                {
                    "$set": {
                        "player_id": inserted_playername_id,
                        "ip_id": inserted_ip_address_id,
                    }
                },
                upsert=True,
            )

        elif line.startswith("[") and ("[server connection]" in line):
            log_datetime = GET_LOG_DATEHOURS(line, log_filename)
            splited_line = line.split()
            playername = splited_line[splited_line.index("connection]") + 1]

            inserted_playername_id = ""

            playername_isPresent = db["player"].update_one(
                {"playername": playername},
                {"$set": {"playername": playername}},
                upsert=True,
            )

            if playername_isPresent.upserted_id is not None:
                inserted_playername_id = playername_isPresent.upserted_id
            else:
                inserted_playername_id = db["player"].find_one(
                    {"playername": str(playername)}
                )["_id"]

            db["activity"].insert_one(
                {
                    "text": "".join(line),
                    "player_id": inserted_playername_id,
                    "timestamp": log_datetime,
                    "file_id": log_file_id,
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

                inserted_playername_id = ""
                playername_isPresent = db["player"].update_one(
                    {"playername": playername},
                    {"$set": {"playername": playername}},
                    upsert=True,
                )

                if playername_isPresent.upserted_id is not None:
                    inserted_playername_id = playername_isPresent.upserted_id
                else:
                    inserted_playername_id = db["player"].find_one(
                        {"playername": str(playername)}
                    )["_id"]

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
        print(f"Ignoring invalid line.")
