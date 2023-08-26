from typing import List
import azure.functions as func
import logging
import json
from library import process_message

app = func.FunctionApp()


@app.event_hub_message_trigger(arg_name="events", event_hub_name="hub1",
                               connection="EVENTHUB_STR", cardinality="many")
def eventhub_trigger(events: List[func.EventHubEvent]):
    for event in events:
        message_body: str = event.get_body().decode('utf-8')
        logging.info(
            'Python EventHub trigger processed an event: %s', message_body)
        product = json.loads(message_body)
        process_message(product, logging)
