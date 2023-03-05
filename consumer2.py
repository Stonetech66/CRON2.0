import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import ssl
from datetime import datetime
from worker2 import send_requests2
from CRON2.database import response_table
import aiohttp
import os
from dotenv import load_dotenv
load_dotenv()

def json_deserializer(data):
    return  json.loads(data.decode("utf-8"))

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)
    
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
    # producer=AIOKafkaProducer(
    # bootstrap_servers=[server], 
    # security_protocol="SASL_SSL", sasl_mechanism="PLAIN", 
    # sasl_plain_username=kafka_username, 
    # sasl_plain_password=kafka_password, 
    # ssl_context=ssl.create_default_context(),compression_type="gzip", value_serializer=lambda x: json.dumps(x, cls=CustomJsonEncoder).encode('utf-8'))


    try:
        await consumer.start()
        # await producer.start()
        async with aiohttp.ClientSession() as session:
            print("started consuming")

            while True:
                tasks=[]
                data=await consumer.getmany(timeout_ms=2000, max_records=2)
                for tp, messages in data.items():
                    for msg in messages:
                        # tasks.append(asyncio.create_task(send_requests2(session, msg.value)))
                        print(msg.value)

                # start=datetime.now()

                # data = await asyncio.gather(*tasks)
                # print(f" consuming finished {datetime.now() - start}")
                # s=datetime.now()
                # await response_table.insert_many(data)
                # print(f" response update finsished {datetime.now() - s}")
    finally:
        await consumer.stop()
        # await producer.stop()


if __name__ == '__main__':
    asyncio.run(consume())
