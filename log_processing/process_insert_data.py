from bson import ObjectId
from utils.types import (
    TypesInsertedData,
    TypesMongoPlayer,
    TypesMongoIpAddress,
    TypesMongoActivity,
    TypesConfig,
)
from database.get_database_country import GET_DATABASE
from country_processing.ip_to_country import IP_TO_COUNTRY


# Función para procesar los datos duplicados
def PROCESS_INSERT_DATA(
    insert_data: TypesInsertedData, config: TypesConfig
) -> TypesInsertedData:
    # Diccionario de todo lo que viene para despues hacer la comparación.
    processed_players_as_subplayername: dict[str, TypesMongoPlayer] = {}
    processed_ip_addresses_as_ip_and_subplayername: dict[str, TypesMongoIpAddress] = {}
    processed_ip_addresses: dict[str, TypesMongoIpAddress] = {}
    processed_activity: dict[ObjectId, TypesMongoActivity] = {}
    processed_latest_activity: dict[ObjectId, TypesMongoActivity] = {}

    db = GET_DATABASE(config["mongodb_connection_string"])

    for unprocessed_ip in insert_data["ip_record"]:
        processed_ip_addresses[unprocessed_ip["ip"]] = {
            "country": unprocessed_ip["country"],
            "ip": unprocessed_ip["ip"],
            "_id": ObjectId(),
        }

    for unprocessed_player_data in insert_data["player"]:
        if (
            processed_players_as_subplayername.get(
                unprocessed_player_data["subplayername"]
            )
            is not None
        ):
            processed_players_as_subplayername[
                unprocessed_player_data["subplayername"]
            ] = {
                **processed_players_as_subplayername[
                    unprocessed_player_data["subplayername"]
                ],
                **unprocessed_player_data,
                "_id": ObjectId(),
            }
        else:
            processed_players_as_subplayername[
                unprocessed_player_data["subplayername"]
            ] = {
                **unprocessed_player_data,
                "_id": ObjectId(),
            }

    print("fetched " + str(len(insert_data["ip_record"])) + " ip addresses.")
    print("starting ip fetching, this may take a while...")
    for unprocessed_ip_data in insert_data["ip_address"]:
        if (
            processed_ip_addresses_as_ip_and_subplayername.get(
                unprocessed_ip_data["ip"] + unprocessed_ip_data["subplayername"]
            )
            is not None
        ):
            if processed_ip_addresses.get(unprocessed_ip_data["ip"]) is not None:
                latest_ip_activity_before = (
                    processed_ip_addresses_as_ip_and_subplayername[
                        unprocessed_ip_data["ip"] + unprocessed_ip_data["subplayername"]
                    ]["latest_activity"]
                )
                latest_ip_activity_after = unprocessed_ip_data["latest_activity"]
                latest_ip_activity = None
                if latest_ip_activity_after > latest_ip_activity_before:
                    latest_ip_activity = latest_ip_activity_after
                else:
                    latest_ip_activity = latest_ip_activity_before
                processed_ip_addresses_as_ip_and_subplayername[
                    unprocessed_ip_data["ip"] + unprocessed_ip_data["subplayername"]
                ] = {
                    **processed_ip_addresses_as_ip_and_subplayername[
                        unprocessed_ip_data["ip"] + unprocessed_ip_data["subplayername"]
                    ],
                    **unprocessed_ip_data,
                    "_id": ObjectId(),
                    "country": processed_ip_addresses[unprocessed_ip_data["ip"]][
                        "country"
                    ],
                    "latest_activity": latest_ip_activity,
                }
            else:
                latest_ip_activity = unprocessed_ip_data["latest_activity"]
                country = IP_TO_COUNTRY(unprocessed_ip_data["ip"], db)
                processed_ip_addresses[unprocessed_ip_data["ip"]] = {
                    "ip": unprocessed_ip_data["ip"],
                    "country": country,
                    "_id": ObjectId(),
                }
                processed_ip_addresses_as_ip_and_subplayername[
                    unprocessed_ip_data["ip"] + unprocessed_ip_data["subplayername"]
                ] = {
                    **processed_ip_addresses_as_ip_and_subplayername[
                        unprocessed_ip_data["ip"] + unprocessed_ip_data["subplayername"]
                    ],
                    **unprocessed_ip_data,
                    "_id": ObjectId(),
                    "country": country,
                    "latest_activity": latest_ip_activity,
                }
        else:
            if processed_ip_addresses.get(unprocessed_ip_data["ip"]) is not None:
                latest_ip_activity = unprocessed_ip_data["latest_activity"]
                processed_ip_addresses_as_ip_and_subplayername[
                    unprocessed_ip_data["ip"] + unprocessed_ip_data["subplayername"]
                ] = {
                    **unprocessed_ip_data,
                    "_id": ObjectId(),
                    "country": processed_ip_addresses[unprocessed_ip_data["ip"]][
                        "country"
                    ],
                    "latest_activity": latest_ip_activity,
                }
            else:
                latest_ip_activity = unprocessed_ip_data["latest_activity"]
                country = IP_TO_COUNTRY(unprocessed_ip_data["ip"], db)
                processed_ip_addresses[unprocessed_ip_data["ip"]] = {
                    "ip": unprocessed_ip_data["ip"],
                    "country": country,
                    "_id": ObjectId(),
                }
                processed_ip_addresses_as_ip_and_subplayername[
                    unprocessed_ip_data["ip"] + unprocessed_ip_data["subplayername"]
                ] = {
                    **unprocessed_ip_data,
                    "_id": ObjectId(),
                    "country": country,
                    "latest_activity": latest_ip_activity,
                }

    print("starting activity...")
    for unprocessed_activity_data in insert_data["activity"]:
        processed_activity[unprocessed_activity_data["_id"]] = unprocessed_activity_data

    for unprocessed_latest_activity_data in insert_data["latest_activity"]:
        processed_latest_activity[
            unprocessed_latest_activity_data["_id"]
        ] = unprocessed_latest_activity_data

    # Reconstruye las listas finales a partir de los diccionarios temporales
    insert_data["player"] = list(processed_players_as_subplayername.values())
    insert_data["ip_address"] = list(
        processed_ip_addresses_as_ip_and_subplayername.values()
    )
    insert_data["ip_record"] = list(processed_ip_addresses.values())
    insert_data["activity"] = list(processed_activity.values())
    insert_data["latest_activity"] = list(processed_latest_activity.values())

    return insert_data
