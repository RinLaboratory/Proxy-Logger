from bson import ObjectId
from utils.types import (
    TypesInsertedData,
    TypesMongoPlayer,
    TypesMongoIpAddress,
    TypesMongoActivity,
)


# Función para procesar los datos duplicados
def PROCESS_INSERT_DATA(insertData: TypesInsertedData) -> TypesInsertedData:
    # Diccionario de todo lo que viene para despues hacer la comparación.
    processed_players_as_subplayername: dict[str, TypesMongoPlayer] = {}
    processed_ip_addresses_as_ip_and_subplayername: dict[str, TypesMongoIpAddress] = {}
    processed_activity: dict[ObjectId, TypesMongoActivity] = {}

    for unprocessed_player_data in insertData["player"]:
        processed_players_as_subplayername[unprocessed_player_data["subplayername"]] = {
            **unprocessed_player_data,
            "_id": ObjectId(),
        }

    for unprocessed_ip_data in insertData["ip_address"]:
        processed_ip_addresses_as_ip_and_subplayername[
            unprocessed_ip_data["ip"] + unprocessed_ip_data["subplayername"]
        ] = {**unprocessed_ip_data, "_id": ObjectId()}

    for unprocessed_activity_data in insertData["activity"]:
        processed_activity[unprocessed_activity_data["_id"]] = unprocessed_activity_data

    # Reconstruye las listas finales a partir de los diccionarios temporales
    insertData["player"] = list(processed_players_as_subplayername.values())
    insertData["ip_address"] = list(
        processed_ip_addresses_as_ip_and_subplayername.values()
    )
    insertData["activity"] = list(processed_activity.values())

    return insertData
