import json
from aiokafka import AIOKafkaConsumer
import asyncio
import ssl
from .mail import send_email
from datetime import datetime
from ..worker import CronJob

def json_deserializer(data):
    return json.loads(data.decode("utf-8"))



async def consume():
    consumer=AIOKafkaConsumer('start-cron', 'error-mail', value_deserializer=json_deserializer,bootstrap_servers=['pkc-q283m.af-south-1.aws.confluent.cloud:9092'], security_protocol="SASL_SSL", sasl_mechanism="PLAIN", sasl_plain_username="SXAEPVRULWI46WQE", sasl_plain_password="o3ihTBJmb5nU4XFTW67bz1XfQqV4eejstFHkr/0e/9C1XX1Qnmo3lpqmI4tbqT72", ssl_context=ssl.create_default_context())

    
    try:
        await consumer.start()
        print("started consuming")
        async for msg in consumer:
            print(msg)
            if msg.topic == "start-cron":
                start=datetime.now()
                await CronJob()
                print(f'consumer ended time {start - datetime.now()}')
            elif msg.topic == "error-mail":
                data=msg.value
                await send_email(data['status_code'], data['recepient'])
    except Exception as e:
        print(e)
    finally:
        await consumer.stop()


if __name__ == '__main__':
    asyncio.run(consume())



