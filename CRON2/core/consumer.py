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
KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
CRON_TOPIC = 'cron-2'
ERROR_TOPIC = 'error-mail'
KAFKA_TIMEOUT=int(os.getenv("KAFKA_TIMEOUT", 40000)) 
KAFKA_MAX_RECORD=int(os.getenv("KAFKA_MAX_RECORD",500)) 
KAFKA_MAX_POLL_INTERVAL=int(os.getenv('KAFKA_MAX_POLL_INTERVAL',50000))

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
        'max_poll_records':KAFKA_MAX_RECORD,
        'max_poll_interval_ms':KAFKA_MAX_POLL_INTERVAL,
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
                messages=await consumer.getmany(max_records=KAFKA_MAX_RECORD, timeout_ms=KAFKA_TIMEOUT)
                if not messages:
                    continue
                for tp, msgs in messages.items():
                    for msg in msgs:
                        if msg.topic == CRON_TOPIC:                            
                           cron_tasks.append(asyncio.create_task(send_request(session,msg.value, producer)))
                
                        elif msg.topic == ERROR_TOPIC:                             
                            err_tasks.append(asyncio.create_task(send_error_email(msg.value)))
                            logger.info("error-mail")
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
    
