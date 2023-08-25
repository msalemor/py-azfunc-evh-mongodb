import asyncio
import json
from random import randint

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient, EventHubSharedKeyCredential

EVENT_HUB_FULLY_QUALIFIED_NAMESPACE = "<NAME>.servicebus.windows.net"
EVENT_HUB_NAME = "<HUB_NAME>"
POLICY_NAME = "<POLICY_NAME>"
POLICY_KEY = "<POLICY_KEY>"

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

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

        # Close credential when no longer needed.
        # await credential.close()

asyncio.run(run())
