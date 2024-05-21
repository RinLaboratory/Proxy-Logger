from bson import ObjectId
from utils.types import (
    TypesInsertedData,
    TypesLoadedData,
    TypesMongoPlayer,
    TypesMongoIpAddress,
    TypesMongoActivity,
    TypesMongoPlayerIp,
)


# Función para procesar los datos duplicados
def PROCESS_INSERT_DATA(
    insertData: TypesInsertedData, loadedData: TypesLoadedData
) -> TypesInsertedData:
    # Diccionario de todo lo que viene para despues hacer la comparación.
    unprocessed_players_as_id: dict[str, TypesMongoPlayer] = {}
    unprocessed_ip_addresses_as_id: dict[str, TypesMongoIpAddress] = {}

    for unprocessed_player_data in insertData["player"]:
        unprocessed_players_as_id[
            unprocessed_player_data["_id"]
        ] = unprocessed_player_data

    for unprocessed_ip_data in insertData["ip_address"]:
        unprocessed_ip_addresses_as_id[unprocessed_ip_data["_id"]] = unprocessed_ip_data

    # Diccionarios temporales para realizar un seguimiento de las entradas únicas y sus referencias
    unique_players_as_playername: dict[str, TypesMongoPlayer] = {}
    unique_players_as_id: dict[ObjectId, TypesMongoPlayer] = {}
    unique_ip_addresses_as_id: dict[ObjectId, TypesMongoIpAddress] = {}
    unique_ip_addresses_as_ip: dict[str, TypesMongoIpAddress] = {}
    unique_player_ips: dict[str, TypesMongoPlayerIp] = {}
    rearranged_activity: dict[str, TypesMongoActivity] = {}
    unique_player_ips_ip: dict[str, None] = {}
    unique_player_ips_player: dict[str, None] = {}

    for player_data in insertData["player"]:
        if player_data["playername"] not in unique_players_as_playername:
            unique_players_as_playername[player_data["playername"]] = player_data
            unique_players_as_id[player_data["_id"]] = player_data

    for ip_data in insertData["ip_address"]:
        if ip_data["ip"] not in unique_ip_addresses_as_ip:
            unique_ip_addresses_as_ip[ip_data["ip"]] = ip_data
            unique_ip_addresses_as_id[ip_data["_id"]] = ip_data

    for player_ip_data in insertData["player_ip"]:
        player_ip_playername: TypesMongoPlayer | str = {}
        player_ip_ipaddress: TypesMongoIpAddress | str = {}
        try:
            player_ip_playername = unprocessed_players_as_id.get(
                player_ip_data["player_id"]
            )
            player_ip_ipaddress = unprocessed_ip_addresses_as_id.get(
                player_ip_data["ip_id"]
            )

            if player_ip_playername is None:
                player_ip_playername = loadedData["player_as_id"].get(
                    player_ip_data["player_id"]
                )[0]
            else:
                player_ip_playername = player_ip_playername.get("playername")

            if player_ip_ipaddress is None:
                player_ip_ipaddress = loadedData["ip_address_as_id"].get(
                    player_ip_data["ip_id"]
                )[0]
            else:
                player_ip_ipaddress = player_ip_ipaddress.get("ip")

            if (player_ip_playername not in unique_player_ips_player) or (
                player_ip_ipaddress not in unique_player_ips_ip
            ):
                ip_id = (
                    unique_ip_addresses_as_ip[player_ip_ipaddress]["_id"]
                    if player_ip_ipaddress in unique_ip_addresses_as_ip
                    else loadedData["ip_address"].get(player_ip_ipaddress)[1]
                )
                player_id = (
                    unique_players_as_playername[player_ip_playername]["_id"]
                    if player_ip_playername in unique_players_as_playername
                    else loadedData["player"].get(player_ip_playername)[1]
                )

                unique_player_ips[player_ip_data["_id"]] = {
                    "_id": player_ip_data["_id"],
                    "ip_id": ip_id,
                    "player_id": player_id,
                }
                unique_player_ips_ip[player_ip_ipaddress] = {}
                unique_player_ips_player[player_ip_playername] = {}
        except Exception as e:
            print(
                "unexpected error at: for player_ip_data in insertData[player_ip]: "
                + str(e)
            )

    for activity_data in insertData["activity"]:
        if activity_data["player_id"] in unique_players_as_id:
            rearranged_activity[activity_data["_id"]] = activity_data
        else:
            try:
                activity_playername = unprocessed_players_as_id[
                    activity_data["player_id"]
                ]["playername"]
                activity_updated_player = unique_players_as_playername[
                    activity_playername
                ]
                rearranged_activity[activity_data["_id"]] = {
                    "_id": activity_data["_id"],
                    "file_id": activity_data["file_id"],
                    "player_id": activity_updated_player["_id"],
                    "text": activity_data["text"],
                    "timestamp": activity_data["timestamp"],
                }
            except Exception as e:
                activity_playername = loadedData["player_as_id"].get(
                    activity_data["player_id"]
                )

                if activity_playername is not None:
                    rearranged_activity[activity_data["_id"]] = {
                        "_id": activity_data["_id"],
                        "file_id": activity_data["file_id"],
                        "player_id": activity_playername[1],
                        "text": activity_data["text"],
                        "timestamp": activity_data["timestamp"],
                    }
                else:
                    print("unexpected error at: if activity_playername is not None:")

    # Reconstruye las listas finales a partir de los diccionarios temporales
    insertData["player"] = list(unique_players_as_id.values())
    insertData["ip_address"] = list(unique_ip_addresses_as_id.values())
    insertData["player_ip"] = list(unique_player_ips.values())
    insertData["activity"] = list(rearranged_activity.values())

    return insertData
