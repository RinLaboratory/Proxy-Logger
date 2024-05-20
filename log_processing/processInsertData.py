from utils.types import TypesInsertedData


# Función para procesar los datos duplicados
def PROCESS_INSERT_DATA(insert_data: TypesInsertedData) -> TypesInsertedData:
    # Diccionario de todo lo que viene para despues hacer la comparación.
    unprocessed_players_as_id = {}
    unprocessed_ip_addresses_as_id = {}

    for unprocessed_player_data in insert_data["player"]:
        unprocessed_players_as_id[
            unprocessed_player_data["_id"]
        ] = unprocessed_player_data
    for unprocessed_ip_data in insert_data["ip_address"]:
        unprocessed_ip_addresses_as_id[unprocessed_ip_data["_id"]] = unprocessed_ip_data

    # Diccionarios temporales para realizar un seguimiento de las entradas únicas y sus referencias
    unique_players_as_playername = {}
    unique_players_as_id = {}
    unique_ip_addresses_as_id = {}
    unique_ip_addresses_as_ip = {}
    unique_player_ips = {}
    rearranged_activity = {}
    unique_player_ips_ip = {}
    unique_player_ips_player = {}

    for player_data in insert_data["player"]:
        if player_data["playername"] not in unique_players_as_playername:
            unique_players_as_playername[player_data["playername"]] = player_data
            unique_players_as_id[player_data["_id"]] = player_data

    for ip_data in insert_data["ip_address"]:
        if ip_data["ip"] not in unique_ip_addresses_as_ip:
            unique_ip_addresses_as_ip[ip_data["ip"]] = ip_data
            unique_ip_addresses_as_id[ip_data["_id"]] = ip_data

    for player_ip_data in insert_data["player_ip"]:
        player_ip_playername = unprocessed_players_as_id[player_ip_data["player_id"]][
            "playername"
        ]
        player_ip_ipaddress = unprocessed_ip_addresses_as_id[player_ip_data["ip_id"]][
            "ip"
        ]

        if (player_ip_playername not in unique_player_ips_player) or (
            player_ip_ipaddress not in unique_player_ips_ip
        ):
            unique_player_ips[player_ip_data["_id"]] = {
                "_id": player_ip_data["_id"],
                "ip_id": unique_ip_addresses_as_ip[player_ip_ipaddress]["_id"],
                "player_id": unique_players_as_playername[player_ip_playername]["_id"],
            }
            unique_player_ips_ip[player_ip_ipaddress] = {}
            unique_player_ips_player[player_ip_playername] = {}

    for activity_data in insert_data["activity"]:
        if activity_data["player_id"] in unique_players_as_id:
            rearranged_activity[activity_data["_id"]] = activity_data
        else:
            activity_playername = unprocessed_players_as_id[activity_data["player_id"]][
                "playername"
            ]
            activity_updated_player = unique_players_as_playername[activity_playername]
            rearranged_activity[activity_data["_id"]] = {
                "_id": activity_data["_id"],
                "file_id": activity_data["file_id"],
                "player_id": activity_updated_player["_id"],
                "text": activity_data["text"],
                "timestamp": activity_data["timestamp"],
            }

    # Reconstruye las listas finales a partir de los diccionarios temporales
    insert_data["player"] = list(unique_players_as_id.values())
    insert_data["ip_address"] = list(unique_ip_addresses_as_id.values())
    insert_data["player_ip"] = list(unique_player_ips.values())
    insert_data["activity"] = list(rearranged_activity.values())

    return insert_data
