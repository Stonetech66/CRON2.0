import asyncio
import ssl
from datetime import datetime
from .worker import send_request
from ..database import response_table
from ..mail import send_error_email
import aiohttp
import os
import pytz
import logging
from dotenv import load_dotenv
from json import JSONEncoder
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json 
load_dotenv() 
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

def json_deserializer(data):
    return  json.loads(data.decode("utf-8"))

class CustomJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)
timeout=aiohttp.ClientTimeout(total=30)  
KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
CRON_TOPIC = 'cron-2'
ERROR_TOPIC = 'error-mail'

async def consume():
    consumer_conf = {
        'bootstrap_servers': [KAFKA_SERVER],
        'security_protocol': "SASL_SSL",
        'sasl_mechanism': "PLAIN",
        'sasl_plain_username': KAFKA_USERNAME,
        'sasl_plain_password': KAFKA_PASSWORD,
        'ssl_context': ssl.create_default_context(),
        'auto_offset_reset': 'earliest',
        'group_id': "cron-consumers",
        'session_timeout_ms': 50000,
        'heartbeat_interval_ms': 15000,
        'value_deserializer': json_deserializer,
        'max_poll_records':500,
        'max_poll_interval_ms':50000,
        'enable_auto_commit': False, 
        
    }
    producer_conf = {
        'bootstrap_servers': [KAFKA_SERVER],
        'security_protocol': "SASL_SSL",
        'sasl_mechanism': "PLAIN",
        'sasl_plain_username': KAFKA_USERNAME,
        'sasl_plain_password': KAFKA_PASSWORD,
        'ssl_context': ssl.create_default_context(),
        'compression_type': "gzip",
        'max_batch_size':32768, 
        'value_serializer': lambda x: json.dumps(x, cls=CustomJsonEncoder).encode('utf-8'),
    }

    async with AIOKafkaConsumer(CRON_TOPIC, ERROR_TOPIC, **consumer_conf) as consumer, AIOKafkaProducer(**producer_conf) as producer:
      try:
            logger.info("Started consuming 🚀")
            while True:
              async with aiohttp.ClientSession() as session:
                cron_tasks=[]
                err_tasks=[]
                data=await consumer.getmany(max_records=500, timeout_ms=50000)   
                for tp, messages in data.items():
                    for msg in messages:
                        if msg.topic == CRON_TOPIC:
                            schedule=msg.value['schedule'] 
                            schedule.update({'next_execution': datetime.fromisoformat(schedule['next_execution'])})
                            if schedule['next_execution'].astimezone(pytz.timezone(schedule['timezone'])) > datetime.now(tz=pytz.timezone(schedule['timezone'])):
                               pass
                            else:
                               cron_tasks.append(asyncio.create_task(send_request(session,msg.value, producer)))
                
                        elif msg.topic == ERROR_TOPIC:
                            logger.info("error-mail {msg.value}") 
                            err_tasks.append(asyncio.create_task(send_error_email(msg.value)))
                start=datetime.now()

                cron_response = await asyncio.gather(*cron_tasks)
                await asyncio.gather(*err_tasks)
                if cron_response != []:
                    await response_table.insert_many(cron_response)
                await consumer.commit()
                logger.info(f"batch consuming finished finsished {len(cron_tasks)} {datetime.now() - start}")
               
      except Exception as e:
        logger.exception(f"Consumer error {e}")
         
      finally:
        await consumer.stop()
        await producer.stop()
        await session.close() 


if __name__ == '__main__':
    asyncio.run(consume())
    
