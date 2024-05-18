from pymongo.database import Database


def LOAD_DATABASE_BEFORE_NEW_IMPORT(
    db: Database,
    loadedPlayers: list[tuple[str, int]],
    loadedIPs: list[tuple[str, int]],
    loadedPlayerIPs: list[tuple[int, int]],
    loadedHashes: list[tuple[str, str, int]],
):
    playername_query = db["player"].find()
    for playername in playername_query:
        loadedPlayers.append([playername["playername"], playername["_id"]])

    ip_query = db["ip_address"].find()
    for ip in ip_query:
        loadedIPs.append([ip["ip"], ip["_id"]])

    player_query = db["player_ip"].find()
    for player in player_query:
        loadedPlayerIPs.append([player["player_id"], player["ip_id"]])

    file_hash = db["file"].find()
    for file in file_hash:
        loadedHashes.append([file["hash"], file["filename"], file["_id"]])
