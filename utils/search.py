from utils.types import (
    TypesMongoPlayerIp,
    TypesMongoIpAddress,
    TypesMongoPlayer,
    TypesMongoFile,
)
from bson import objectid


def SEARCH_PLAYER(playername: str, listPlayers: list[TypesMongoPlayer]):
    for elemento in listPlayers:
        if elemento["playername"] == playername:
            return 1
    return -1


def SEARCH_IP(ip: int, listIPs: list[TypesMongoIpAddress]):
    for elemento in listIPs:
        if elemento["ip"] == ip:
            return 1
    return -1


def SEARCH_IP_ID(
    player_id: objectid.ObjectId,
    ip_id: objectid.ObjectId,
    listPlayerIPs: list[TypesMongoPlayerIp],
):
    for elemento in listPlayerIPs:
        if (elemento["player_id"] == player_id) and (elemento["ip_id"] == ip_id):
            return 1
    return -1


def SEARCH_HASH(hash: str, listHashes: list[TypesMongoFile]):
    for element in listHashes:
        if element["hash"] == hash:
            return 1
    return -1
