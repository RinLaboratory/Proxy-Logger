from utils.types import (
    TypesLoadedData,
    TypesMongoFile,
    TypesMongoPlayer,
    TypesMongoIpAddress,
    TypesMongoActivity,
)
from utils.types import TypesConfig
from database.get_database import GET_DATABASE


def LOAD_DATABASE_BEFORE_NEW_IMPORT(config: TypesConfig, loaded_data: TypesLoadedData):
    db = GET_DATABASE(config["mongodb_connection_string"])

    # Using dictionaries for faster lookups
    # Originally db[""].find() returns a Cursor object that can be iterated.
    # and Cursor has a method called clone() that allows to copy the result of the query.
    playername_query: list[TypesMongoPlayer] = db["player"].find()
    loaded_data["player"] = {
        player_data["subplayername"]: (
            player_data["subplayername"],
            player_data["playername"],
        )
        for player_data in playername_query
    }

    ip_query: list[TypesMongoIpAddress] = db["ip_address"].find()
    loaded_data["ip_address"] = {
        ip["ip"] + ip["subplayername"]: (ip["ip"], ip["subplayername"])
        for ip in ip_query
    }

    ip_record_query: list[TypesMongoIpAddress] = db["ip_record"].find()
    loaded_data["ip_record"] = {
        ip_record["ip"]: (ip_record["ip"], ip_record["country"])
        for ip_record in ip_record_query
    }

    file_hash: list[TypesMongoFile] = db["file"].find()
    loaded_data["file"] = {
        file_data["hash"]: (file_data["file_name"], file_data["hash"])
        for file_data in file_hash
    }

    latest_file: list[TypesMongoFile] = db["latest_file"].find()
    loaded_data["latest_file"] = {
        latest_data["hash"]: (
            latest_data["file_name"],
            latest_data["hash"],
            latest_data["_id"],
        )
        for latest_data in latest_file
    }

    for latest_file_data in loaded_data["latest_file"].values():
        latest_file_id = latest_file_data[2]
        latest_activity: list[TypesMongoActivity] = (
            db["latest_activity"].find({"file_id": latest_file_id}).sort("timestamp")
        )
        latest_activity_data = [activity["text"] for activity in latest_activity]
        loaded_data["latest_activity"][latest_file_id] = latest_activity_data
