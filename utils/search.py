def SEARCH_PLAYER(player: str, loadedPlayers: list[tuple[str, int]]):
    for i, elemento in enumerate(loadedPlayers):
        if elemento[0] == player:
            return i
    return -1


def SEARCH_IP(ip: int, loadedIPs: list[tuple[str, int]]):
    for i, elemento in enumerate(loadedIPs):
        if elemento[0] == ip:
            return i
    return -1


def SEARCH_IP_ID(player_id: int, ip_id: int, loadedPlayerIPs: list[tuple[int, int]]):
    for i, elemento in enumerate(loadedPlayerIPs):
        if elemento[0] == player_id and elemento[1] == ip_id:
            return i
    return -1


def SEARCH_HASH(hash: str, loadedHashes: list[tuple[str, str, int]]):
    for i, elemento in enumerate(loadedHashes):
        if elemento[0] == hash:
            return i, elemento[1]
    return -1, None
