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

    playername_query: list[TypesMongoPlayer] = db["player"].find()
    for playername in playername_query:
        loadedData["player"].append(playername)

    ip_query: list[TypesMongoIpAddress] = db["ip_address"].find()
    for ip in ip_query:
        loadedData["ip_address"].append(ip)

    player_query: TypesMongoPlayerIp = db["player_ip"].find()
    for player in player_query:
        loadedData["player_ip"].append(player)

    file_hash: list[TypesMongoFile] = db["file"].find()
    for file in file_hash:
        loadedData["file"].append(file)
