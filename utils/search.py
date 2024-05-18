def SEARCH_HASH(hash: str, loadedHashes: list[tuple[str, str, int]]):
    for i, elemento in enumerate(loadedHashes):
        if elemento[0] == hash:
            return i, elemento[1]
    return -1, None
