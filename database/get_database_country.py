from pymongo import MongoClient


def GET_DATABASE(CONNECTION_STRING: str):
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    mydb = client["Countries"]

    return mydb
