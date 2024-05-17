import sqlite3
from log_processing.get_log_hours import GET_LOG_DATEHOURS
from utils.search import SEARCH_IP, SEARCH_IP_ID, SEARCH_PLAYER


def WRITE_PLAYER_TO_DATABASE(
    line: str,
    log_filename: str,
    log_file_id: int,
    cur_thread: sqlite3.Cursor,
    loadedPlayers: list[tuple[str, int]],
    loadedIPs: list[tuple[str, int]],
    loadedPlayerIPs: list[tuple[int, int]],
):
    try:
        if (line.startswith("[") and "[connected player]") in line:
            log_datetime = GET_LOG_DATEHOURS(line, log_filename)
            splited_line = line.split()
            playername = splited_line[splited_line.index("player]") + 1]
            ip_and_port: list[str] = splited_line[
                splited_line.index("player]") + 2
            ].split("/")
            splited_ip = ip_and_port[1].split(":")
            ip = splited_ip[0]
            # print(playername + ' | ' + ip)
            inserted_ip_address_id = 0
            inserted_playername_id = 0

            ip_address_isPresent = SEARCH_IP(ip, loadedIPs)
            playername_isPresent = SEARCH_PLAYER(playername, loadedPlayers)

            if ip_address_isPresent != -1:
                # print(ip_address_isPresent)
                inserted_ip_address_id = loadedIPs[ip_address_isPresent][1]
            else:
                cur_thread.execute(
                    "INSERT INTO ip_address(ip,id) VALUES ('" + str(ip) + "', NULL)"
                )
                loadedIPs.append([ip, cur_thread.lastrowid])
                inserted_ip_address_id = cur_thread.lastrowid

            if playername_isPresent != -1:
                inserted_playername_id = loadedPlayers[playername_isPresent][1]

            else:
                cur_thread.execute(
                    "INSERT INTO player(playername,id) VALUES ('"
                    + str(playername)
                    + "', NULL)"
                )
                loadedPlayers.append([playername, cur_thread.lastrowid])
                inserted_playername_id = cur_thread.lastrowid

            cur_thread.execute(
                "INSERT INTO activity(text, player_id, timestamp, file_id, id) VALUES (?, ?, ?, ?, NULL)",
                ("".join(line), inserted_playername_id, log_datetime, log_file_id),
            )

            player_ip_address_isPresent = SEARCH_IP_ID(
                inserted_playername_id, inserted_ip_address_id, loadedPlayerIPs
            )
            if player_ip_address_isPresent == -1:
                cur_thread.execute(
                    "INSERT INTO player_ip(player_id, ip_id) VALUES (?, ?)",
                    (inserted_playername_id, inserted_ip_address_id),
                )
                loadedPlayerIPs.append([inserted_playername_id, inserted_ip_address_id])

        if (line.startswith("[") and "[server connection]") in line:
            log_datetime = GET_LOG_DATEHOURS(line, log_filename)
            splited_line = line.split()
            playername = splited_line[splited_line.index("connection]") + 1]

            inserted_playername_id = 0

            playername_isPresent = SEARCH_PLAYER(playername, loadedPlayers)

            if playername_isPresent != -1:
                inserted_playername_id = loadedPlayers[playername_isPresent][1]

            else:
                cur_thread.execute(
                    "INSERT INTO player(playername,id) VALUES ('"
                    + str(playername)
                    + "', NULL)"
                )
                loadedPlayers.append([playername, cur_thread.lastrowid])
                inserted_playername_id = cur_thread.lastrowid

            cur_thread.execute(
                "INSERT INTO activity(text, player_id, timestamp, file_id, id) VALUES (?, ?, ?, ?, NULL)",
                ("".join(line), inserted_playername_id, log_datetime, log_file_id),
            )

        if line.startswith("[") and "[nlogin]" in line:
            if ("has successfully logged in." in line) or (
                "has successfully registered." in line
            ):
                log_datetime = GET_LOG_DATEHOURS(line, log_filename)
                splited_line = line.split()
                playername = splited_line[splited_line.index("user") + 1]
                playername_isPresent = SEARCH_PLAYER(playername, loadedPlayers)
                if playername_isPresent != -1:
                    inserted_playername_id = loadedPlayers[playername_isPresent][1]
                    cur_thread.execute(
                        "INSERT INTO activity(text, player_id, timestamp, file_id, id) VALUES (?, ?, ?, ?, NULL)",
                        (
                            "".join(line),
                            inserted_playername_id,
                            log_datetime,
                            log_file_id,
                        ),
                    )
                else:
                    cur_thread.execute(
                        "INSERT INTO player(playername,id) VALUES ('"
                        + str(playername)
                        + "', NULL)"
                    )
                    loadedPlayers.append([playername, cur_thread.lastrowid])
                    inserted_playername_id = cur_thread.lastrowid
                    cur_thread.execute(
                        "INSERT INTO activity(text, player_id, timestamp, file_id, id) VALUES (?, ?, ?, ?, NULL)",
                        (
                            "".join(line),
                            inserted_playername_id,
                            log_datetime,
                            log_file_id,
                        ),
                    )
    except Exception as e:
        # print('ignored invalid line. |'+line)
        print(e)
