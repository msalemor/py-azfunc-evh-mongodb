import os
import pymongo
from dotenv import load_dotenv

def init_db(client, DB_NAME, COLLECTION_NAME, logging):
    # Create database if it doesn't exist
    db = client[DB_NAME]
    if DB_NAME not in client.list_database_names():
        # Create a database with 400 RU throughput that can be shared across
        # the DB's collections
        db.command({"customAction": "CreateDatabase", "offerThroughput": 400})
        logging.info("Created db '{}' with shared throughput.\n".format(DB_NAME))
    else:
        logging.info("Using database: '{}'.\n".format(DB_NAME))

    # Create collection if it doesn't exist
    collection = db[COLLECTION_NAME]    
    if COLLECTION_NAME not in db.list_collection_names():
        # Creates a unsharded collection that uses the DBs shared throughput
        db.command(
            {"customAction": "CreateCollection", "collection": COLLECTION_NAME}
        )
        logging.info("Created collection '{}'.\n".format(COLLECTION_NAME))
    else:
        logging.info ("Using collection: '{}'.\n".format(COLLECTION_NAME))

    return collection

def process_message(product,logging):
    try:
        load_dotenv()
        CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
        DB_NAME = os.getenv("DB_NAME")
        COLLECTION_NAME = os.getenv("COLLECTION_NAME")
        # Initialize the Cosmos client
        client = pymongo.MongoClient(CONNECTION_STRING)
        # Initialize the database
        collection = init_db(client, DB_NAME, COLLECTION_NAME, logging)
        # Insert product into collection
        result = collection.insert_one(product)
        #result = collection.update_one(
        #{"name": product["name"]}, {"$set": product}, upsert=True)
        logging.info("Inserted document with _id {}\n".format(result.inserted_id))
        return result.inserted_id
    except Exception as e:
        logging.error("Error: {}".format(str(e)))
        return None