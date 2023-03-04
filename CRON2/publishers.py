import pika
import json
from aiokafka import AIOKafkaProducer
import ssl
import asyncio
import aiohttp
import ssl
from datetime import datetime

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)




async def publish(topic, data:dict):
    producer=AIOKafkaProducer(
        bootstrap_servers=['pkc-q283m.af-south-1.aws.confluent.cloud:9092'], 
        security_protocol="SASL_SSL", sasl_mechanism="PLAIN", 
        sasl_plain_username="SXAEPVRULWI46WQE", 
        sasl_plain_password="o3ihTBJmb5nU4XFTW67bz1XfQqV4eejstFHkr/0e/9C1XX1Qnmo3lpqmI4tbqT72", 
        ssl_context=ssl.create_default_context(), value_serializer=lambda x: json.dumps(x, cls=CustomJsonEncoder).encode('utf-8'))

    
    try:
        await producer.start()
        await producer.send(topic, data)
    except Exception as e:
        print(e)

    finally:
       await  producer.stop()


# # async def publish(data:dict, producer):
# #     await producer.send("test", json.dumps(data),)
# #     # if data["status_code"].startswith("5") or data["status_code"].startswith("4"):
# #     #     await producer.send("error_mail", json.dumps(data))


# # async def publish3(data:dict, producer):
# #     producer.send("test", json.dumps(data))

