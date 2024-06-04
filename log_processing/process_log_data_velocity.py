import re
from bson import objectid
from log_processing.get_log_hours import GET_LOG_DATEHOURS
from country_processing.search_country import SEARCH_COUNTRY
from utils.types import TypesLoadedData, TypesInsertedData, TypesCountryDictionary


def PROCESS_LOG_DATA_VELOCITY(
    line: str,
    log_filename: str,
    log_file_id: objectid.ObjectId,
    insert_data: TypesInsertedData,
    loaded_data: TypesLoadedData,
    countries: TypesCountryDictionary,
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

            playername_isPresent = loaded_data["player"].get(playername_lower)
            ip_isPresent = loaded_data["ip_address"].get(ip + playername_lower)

            if playername_isPresent is not None:
                # El jugador está presente desde antes
                inserted_playername = playername_isPresent[0]
            else:
                # El jugador no está presente y se debe ingresar en la db
                inserted_playername = playername_lower
                insert_data["player"].append(
                    {"playername": playername, "subplayername": playername_lower}
                )

            if ip_isPresent is None:
                if (
                    ("VPN o un Proxy" in line)
                    or ("VPN or Proxy" in line)
                    or ("VPN o Proxy" in line)
                ):
                    insert_data["ip_address"].append(
                        {
                            "ip": ip,
                            "subplayername": inserted_playername,
                            "isVPN": True,
                            "latest_activity": log_datetime,
                        }
                    )
                    if "desde: " in line:
                        start_index = splited_line.index("desde:") + 1
                        country_name = ""
                        # Asegúrate de que start_index es válido
                        if start_index < len(splited_line):
                            # Combina todas las partes del país que pueden estar divididas por espacios
                            country_parts = []
                            for i in range(start_index, len(splited_line)):
                                part = re.sub(r"§.", "", splited_line[i])

                                country_parts.append(part)
                                # Detener si encontramos el final del país o el comienzo de otra sección
                                if "." in part:
                                    break

                            # Unir las partes para obtener el nombre completo del país
                            country_name = " ".join(country_parts).replace(".", "")
                        country = SEARCH_COUNTRY(
                            country_name,
                            countries,
                        )
                        insert_data["ip_record"].append({"ip": ip, "country": country})
                else:
                    insert_data["ip_address"].append(
                        {
                            "ip": ip,
                            "subplayername": inserted_playername,
                            "latest_activity": log_datetime,
                        }
                    )

            if log_filename != "latest.log":
                insert_data["activity"].append(
                    {
                        "_id": objectid.ObjectId(),
                        "file_id": log_file_id,
                        "text": "".join(line),
                        "timestamp": log_datetime,
                        "subplayername": playername_lower,
                    }
                )
            else:
                insert_data["latest_activity"].append(
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

            playername_isPresent = loaded_data["player"].get(playername_lower)

            if playername_isPresent is not None:
                # El jugador está presente desde antes
                inserted_playername = playername_isPresent[0]
            else:
                # El jugador no está presente y se debe ingresar en la db
                inserted_playername = playername_lower
                insert_data["player"].append(
                    {"playername": playername, "subplayername": playername_lower}
                )

            if log_filename != "latest.log":
                insert_data["activity"].append(
                    {
                        "_id": objectid.ObjectId(),
                        "file_id": log_file_id,
                        "text": "".join(line),
                        "timestamp": log_datetime,
                        "subplayername": playername_lower,
                    }
                )
            else:
                insert_data["latest_activity"].append(
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

                playername_isPresent = loaded_data["player"].get(playername_lower)

                if playername_isPresent is not None:
                    # El jugador está presente desde antes
                    inserted_playername = playername_isPresent[0]
                else:
                    isPremium = False
                    if "premium account" in line:
                        isPremium = True
                    # El jugador no está presente y se debe ingresar en la db
                    inserted_playername = playername_lower
                    insert_data["player"].append(
                        {
                            "playername": playername,
                            "subplayername": playername_lower,
                            "isPremium": isPremium,
                        }
                    )

                if log_filename != "latest.log":
                    insert_data["activity"].append(
                        {
                            "_id": objectid.ObjectId(),
                            "file_id": log_file_id,
                            "text": "".join(line),
                            "timestamp": log_datetime,
                            "subplayername": playername_lower,
                        }
                    )
                else:
                    insert_data["latest_activity"].append(
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
