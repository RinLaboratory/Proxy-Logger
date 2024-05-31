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
    playername: str
    subplayername: str


class TypesMongoIpAddress(TypedDict):
    ip: str
    subplayername: str


class TypesMongoActivity(TypedDict):
    _id: ObjectId
    subplayername: str
    file_id: ObjectId
    text: str
    timestamp: datetime


class TypesLoadedData(TypedDict):
    player: dict[str, tuple[str, str]]
    ip_address: dict[str, tuple[str, str]]
    file: dict[str, tuple[str, str]]
    latest_file: dict[str, tuple[str, str, ObjectId]]
    latest_activity: dict[str, list[str]]


class TypesInsertedData(TypedDict):
    player: list[TypesMongoPlayer]
    ip_address: list[TypesMongoIpAddress]
    file: list[TypesMongoFile]
    activity: list[TypesMongoActivity]
    latest_file: list[TypesMongoFile]
    latest_activity: list[TypesMongoActivity]
    file_marked_for_deletion: list[ObjectId]
