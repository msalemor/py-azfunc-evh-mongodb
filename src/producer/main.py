import asyncio
import json
from random import randint
from dotenv import load_dotenv
import os

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient, EventHubSharedKeyCredential

load_dotenv()
EVENT_HUB_FULLY_QUALIFIED_NAMESPACE = os.getenv(
    "EVENT_HUB_FULLY_QUALIFIED_NAMESPACE")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")
POLICY_NAME = os.getenv("POLICY_NAME")
POLICY_KEY = os.getenv("POLICY_KEY")

credential = EventHubSharedKeyCredential(
    POLICY_NAME, POLICY_KEY)


async def run():
    producer = EventHubProducerClient(
        fully_qualified_namespace=EVENT_HUB_FULLY_QUALIFIED_NAMESPACE,
        eventhub_name=EVENT_HUB_NAME,
        credential=credential,
    )
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

      # Add events to the batch.
        product = {
            "category": "gear-surf-surfboards",
            "name": "Yamba Surfboard-{}".format(randint(50, 5000)),
            "quantity": 1,
            "sale": False,
        }
        event_data_batch.add(EventData(json.dumps(product)))
        product1 = {
            "category": "gear-surf-surfboards",
            "name": "Lemba Skateboard-{}".format(randint(50, 5000)),
            "quantity": 1,
            "sale": False,
        }
        event_data_batch.add(EventData(json.dumps(product1)))
        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

        # Close credential when no longer needed.
        # await credential.close()

asyncio.run(run())
