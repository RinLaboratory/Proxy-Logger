from pymongo import MongoClient, DESCENDING


def GET_DATABASE(CONNECTION_STRING: str):
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    mydb = client["Countries"]

    return mydb


def READ_FILE(file_path: str):
    with open(file_path, "r", encoding="utf8") as file:
        return file.readlines()


def COUNTRIES():
    db = GET_DATABASE("mongodb://localhost:27017")
    file_lines = READ_FILE("./country_processing/IP2LOCATION-LITE-DB3.CSV")

    ips = []
    for line in file_lines:
        splitted_line = line.replace('"', "").split(",")
        ips.append(
            {
                "start": int(splitted_line[0]),
                "end": int(splitted_line[1]),
                "iso2": splitted_line[2],
            }
        )

    db["country"].insert_many(ips)
    db["country"].create_index([("start", DESCENDING), ("end", DESCENDING)])


if __name__ == "__main__":
    COUNTRIES()
