from pymongo import database


def IP_TO_COUNTRY(ip: str, db: database.Database):
    #
    # For more info on how this works visit
    # https://lite.ip2location.com/faq
    #

    ip_splitted = ip.split(".")

    w = int(ip_splitted[0])
    x = int(ip_splitted[1])
    y = int(ip_splitted[2])
    z = int(ip_splitted[3])

    ip_number = (16777216 * w) + (65536 * x) + (256 * y) + z

    country_iso2 = db["country"].find_one(
        {
            "$and": [
                {"start": {"$lte": ip_number}},
                {"end": {"$gte": ip_number}},
            ]
        }
    )

    return country_iso2["iso2"]
