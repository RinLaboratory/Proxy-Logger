from typing import TypedDict
from bson import ObjectId  # Asegúrate de tener PyMongo instalado para importar ObjectId
from datetime import datetime


class TypesConfig(TypedDict):
    mongodb_connection_string: str


class TypesMongoFile(TypedDict):
    _id: ObjectId
    file_name: str
    hash: str
    proxy_type: str


class TypesMongoPlayer(TypedDict):
    _id: ObjectId
    playername: str


class TypesMongoIpAddress(TypedDict):
    _id: ObjectId
    ip: str


class TypesMongoPlayerIp(TypedDict):
    _id: ObjectId
    player_id: ObjectId
    ip_id: ObjectId


class TypesMongoActivity(TypedDict):
    _id: ObjectId
    player_id: ObjectId
    file_id: ObjectId
    text: str
    timestamp: datetime


class TypesLoadedData(TypedDict):
    player: dict[str, tuple[str, ObjectId]]
    player_as_id: dict[ObjectId, tuple[str, ObjectId]]
    ip_address: dict[str, tuple[str, ObjectId]]
    ip_address_as_id: dict[ObjectId, tuple[str, ObjectId]]
    player_ip: set[tuple[ObjectId, ObjectId]]
    file: dict[str, tuple[str, str]]


class TypesInsertedData(TypedDict):
    player: list[TypesMongoPlayer]
    ip_address: list[TypesMongoIpAddress]
    player_ip: list[TypesMongoPlayerIp]
    file: list[TypesMongoFile]
    activity: list[TypesMongoActivity]
