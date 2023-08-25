import azure.functions as func
import logging
import json
import os
import pymongo
from dotenv import load_dotenv
from library import init_db, process_message

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="hub1",
                               connection="EVENTHUB_STR") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    # Get the string message from hub
    msg : str = azeventhub.get_body().decode('utf-8')
    logging.info('Python EventHub trigger processed an event: %s',msg)
    product = json.loads(msg)
    process_message(product,logging)
