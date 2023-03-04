from aiokafka import AIOKafkaConsumer
import asyncio

import ssl
import json
from datetime import datetime
def json_deserializer(data):
    return json.loads(data.decode("utf-8"))

async def consume():
    consume=AIOKafkaConsumer('test', value_deserializer=json_deserializer,bootstrap_servers=['pkc-q283m.af-south-1.aws.confluent.cloud:9092'], security_protocol="SASL_SSL", sasl_mechanism="PLAIN", sasl_plain_username="SXAEPVRULWI46WQE", sasl_plain_password="o3ihTBJmb5nU4XFTW67bz1XfQqV4eejstFHkr/0e/9C1XX1Qnmo3lpqmI4tbqT72", ssl_context=ssl.create_default_context())
    try:
        await consume.start()
        print("started consuming")
        start=datetime.now()
        async for msg in consume:
            print(msg)
        print(datetime.now() - start)
    finally:
     await consume.stop()

if __name__ == "__main__":
    asyncio.run(consume())
