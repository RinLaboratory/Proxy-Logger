from utils.types import (
    TypesLoadedData,
    TypesMongoFile,
    TypesMongoPlayer,
    TypesMongoIpAddress,
)
from utils.types import TypesConfig
from database.get_database import GET_DATABASE


def LOAD_DATABASE_BEFORE_NEW_IMPORT(config: TypesConfig, loadedData: TypesLoadedData):
    db = GET_DATABASE(config["mongodb_connection_string"])

    # Using dictionaries for faster lookups
    # Originally db[""].find() returns a Cursor object that can be iterated.
    # and Cursor has a method called clone() that allows to copy the result of the query.
    playername_query: list[TypesMongoPlayer] = db["player"].find()
    loadedData["player"] = {
        playerData["subplayername"]: (
            playerData["subplayername"],
            playerData["playername"],
        )
        for playerData in playername_query
    }

    ip_query: list[TypesMongoIpAddress] = db["ip_address"].find()
    loadedData["ip_address"] = {
        ip["ip"] + ip["subplayername"]: (ip["ip"], ip["subplayername"])
        for ip in ip_query
    }

    file_hash: list[TypesMongoFile] = db["file"].find()
    loadedData["file"] = {
        fileData["hash"]: (fileData["file_name"], fileData["hash"])
        for fileData in file_hash
    }
