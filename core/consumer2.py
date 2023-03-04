import json
from aiokafka import AIOKafkaConsumer
import asyncio
import ssl
from datetime import datetime
from .worker2 import send_requests2
from CRON2.database import response_table
import aiohttp
import os
from dotenv import load_dotenv
load_dotenv()

def json_deserializer(data):
    return  json.loads(data.decode("utf-8"))

server=os.getenv('KAFKA_SERVER')
kafka_password=os.getenv("KAFKA_PASSWORD")
kafka_username= os.getenv("KAFKA_USERNAME")

async def consume():
    consumer=AIOKafkaConsumer(
            'test',
            value_deserializer=json_deserializer,bootstrap_servers=[server], 
            security_protocol="SASL_SSL", sasl_mechanism="PLAIN", 
            sasl_plain_username=kafka_username, 
            sasl_plain_password=kafka_password, 
            ssl_context=ssl.create_default_context(),
            max_poll_records=1000,
            auto_offset_reset='earliest',
            group_id="cron-consumers"
            )


    try:
        await consumer.start()
        async with aiohttp.ClientSession() as session:
            print("started consuming")

            while True:
                tasks=[]
                data=await consumer.getmany(max_records=1000)
                for tp, messages in data.items():
                    for msg in messages:
                        tasks.append(asyncio.create_task(send_requests2(session, msg.value)))
                start=datetime.now()
                data = await asyncio.gather(*tasks)
                print(f" consuming finished {datetime.now() - start}")
                s=datetime.now()
                await response_table.insert_many(data)
                print(f" response update finsished {datetime.now() - s}")
    finally:
        await consumer.stop()


if __name__ == '__main__':
    asyncio.run(consume())
