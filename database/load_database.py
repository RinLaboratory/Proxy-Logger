import sqlite3


def LOAD_DATABASE_BEFORE_NEW_IMPORT(
    cur: sqlite3.Cursor,
    loadedPlayers: list[tuple[str, int]],
    loadedIPs: list[tuple[str, int]],
    loadedPlayerIPs: list[tuple[int, int]],
    loadedHashes: list[tuple[str, str, int]],
):
    playername_query: list[tuple[str, int]] = cur.execute(
        "SELECT playername, id FROM player"
    ).fetchall()
    for playername, id in playername_query:
        loadedPlayers.append([playername, id])

    ip_query: list[tuple[str, int]] = cur.execute(
        "SELECT ip, id FROM ip_address"
    ).fetchall()
    for ip, id in ip_query:
        loadedIPs.append([ip, id])

    player_query: list[tuple[int, int]] = cur.execute(
        "SELECT player_id, ip_id FROM player_ip"
    ).fetchall()
    for player_element, ip_id in player_query:
        loadedPlayerIPs.append([player_element, ip_id])

    file_hash: list[tuple[str, str, int]] = cur.execute(
        "SELECT hash, filename, id FROM file"
    ).fetchall()
    for hash, filename, id in file_hash:
        loadedHashes.append([hash, filename, id])

    # print(loadedPlayers)
