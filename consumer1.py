import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import ssl
# from CRON2.mail import send_email
from datetime import datetime
from .worker2 import CronJob, send_requests2
from ..CRON2.database import response_table
import aiohttp

from ..CRON2.mail import send_error_mail
import os
from dotenv import load_dotenv

load_dotenv()
def json_deserializer(data):
    return  json.loads(data.decode("utf-8"))

server=os.getenv('KAFKA_SERVER')
kafka_password=os.getenv("KAFKA_PASSWORD")
kafka_username= os.getenv("KAFKA_USERNAME")

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)
    
async def consume():
    consumer=AIOKafkaConsumer(
            'test','error-mail',
            value_deserializer=json_deserializer,bootstrap_servers=[server], 
            security_protocol="SASL_SSL", sasl_mechanism="PLAIN", 
            sasl_plain_username=kafka_username, 
            sasl_plain_password=kafka_password, 
            ssl_context=ssl.create_default_context(),
            max_poll_records=1000,
            auto_offset_reset='earliest',
            group_id="cron-consumers"
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
                mail_tasks=[]
                data=await consumer.getmany()
                for tp, messages in data.items():
                    if tp.topic == "cron-2":
                        for msg in messages:
                            cron_tasks.append(asyncio.create_task(send_requests2(session, msg.value, producer)))
                    elif tp.topic == "error-mail":
                        for msg in messages:
                            mail_tasks.append(asyncio.create_task(send_error_mail(msg.value)))                    
                start=datetime.now()
                data = await asyncio.gather(*cron_tasks)
                print(f" consuming finished {datetime.now() - start}")
                s=datetime.now()
                await response_table.insert_many(data)
                await asyncio.gather(*mail_tasks)
                print(f" response update finsished {datetime.now() - s}")
    finally:
        await consumer.stop()
        await producer.stop()


if __name__ == '__main__':
    asyncio.run(consume())
