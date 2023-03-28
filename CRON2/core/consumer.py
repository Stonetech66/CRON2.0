import json
import sys
import os
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import ssl
from datetime import datetime
from .worker import send_requests
from ..database import response_table
from ..mail import send_error_email
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
            'cron-2','error-mail',
            value_deserializer=json_deserializer,bootstrap_servers=[server], 
            security_protocol="SASL_SSL", sasl_mechanism="PLAIN", 
            sasl_plain_username=kafka_username, 
            sasl_plain_password=kafka_password, 
            ssl_context=ssl.create_default_context(),
            auto_offset_reset='earliest',
            group_id="cron-consumers",
            session_timeout_ms=50000,
            heartbeat_interval_ms=15000

            )
    producer=AIOKafkaProducer(
        bootstrap_servers=[server], 
        security_protocol="SASL_SSL", sasl_mechanism="PLAIN", 
        sasl_plain_username=kafka_username, 
        sasl_plain_password=kafka_password, 
        ssl_context=ssl.create_default_context(),compression_type="gzip", value_serializer=lambda x: json.dumps(x, cls=CustomJsonEncoder).encode('utf-8'))


    try:
        await consumer.start()
        await producer.start()
        async with aiohttp.ClientSession() as session:
            print("started consuming")

            while True:
                cron_tasks=[]
                err_tasks=[]
                data=await consumer.getmany(max_records=500, timeout_ms=30000)   
                for tp, messages in data.items():
                    for msg in messages:
                        if msg.topic == "cron-2":
                            cron_tasks.append(asyncio.create_task(send_requests(session,msg.value, producer)))
                        elif msg.topic == "error-mail":
                            err_tasks.append(asyncio.create_task(send_error_email(msg.value)))
                start=datetime.now()

                data = await asyncio.gather(*cron_tasks)
                await asyncio.gather(*err_tasks)
                print(f" consuming finished {datetime.now() - start}")
                s=datetime.now()
                if not data ==[]:
                    await response_table.insert_many(data)
                print(f" response update finsished {datetime.now() - s}")
    finally:
        await consumer.stop()
        await producer.stop()


if __name__ == '__main__':
    asyncio.run(consume())
