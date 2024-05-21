from utils.types import (
    TypesLoadedData,
    TypesMongoFile,
    TypesMongoPlayer,
    TypesMongoIpAddress,
    TypesMongoPlayerIp,
)
from utils.types import TypesConfig
from database.get_database import GET_DATABASE


def LOAD_DATABASE_BEFORE_NEW_IMPORT(config: TypesConfig, loadedData: TypesLoadedData):
    db = GET_DATABASE(config["mongodb_connection_string"])

    # Using dictionaries for faster lookups
    # Originally db[""].find() returns a Cursor object that can be iterated.
    # and Cursor has a method called clone() that allows to copy the result of the query.
    playername_query: list[TypesMongoPlayer] = db["player"].find()
    playername_query_as_id = playername_query.clone()
    loadedData["player"] = {
        playerData["playername"]: (playerData["playername"], playerData["_id"])
        for playerData in playername_query
    }
    loadedData["player_as_id"] = {
        playerData["_id"]: (playerData["playername"], playerData["_id"])
        for playerData in playername_query_as_id
    }

    ip_query: list[TypesMongoIpAddress] = db["ip_address"].find()
    ip_query_to_id = ip_query.clone()
    loadedData["ip_address"] = {
        ip["ip"]: (ip["ip"], ip["_id"]) for ip in ip_query_to_id
    }
    loadedData["ip_address_as_id"] = {
        ip["_id"]: (ip["ip"], ip["_id"]) for ip in ip_query
    }

    player_query: list[TypesMongoPlayerIp] = db["player_ip"].find()
    loadedData["player_ip"] = set(
        (player["player_id"], player["ip_id"]) for player in player_query
    )

    file_hash: list[TypesMongoFile] = db["file"].find()
    loadedData["file"] = {
        fileData["hash"]: (fileData["file_name"], fileData["hash"])
        for fileData in file_hash
    }
