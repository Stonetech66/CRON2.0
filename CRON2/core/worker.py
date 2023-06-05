from ..database import job_table
from datetime import datetime, timedelta 
import asyncio
import pytz, ssl
import aiohttp
from ..utils import next_execution
from bson.objectid import ObjectId
from json import JSONEncoder
import json
from aiokafka import AIOKafkaProducer
import os
from dotenv import load_dotenv
import logging
import os
load_dotenv()
KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
CRON_TOPIC = os.getenv('CRON_TOPIC')
ERROR_TOPIC= os.getenv('ERROR_TOPIC')
CRON_MAX_FAILURES=3 
REQUEST_TIMEOUT=30 #time in seconds
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
max_failures=CRON_MAX_FAILURES

class CustomJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)




async def send_request(session, data, producer):
    method=data['method']
    header=data['header']
    url= data['url']
    job_id= data['job_id']
    body= data['body']
    email=data["email"]
    # sending http requests to the specified endpoint
    try:
        async with getattr(session, method)(url, headers=header, json=body,timeout=timeout) as response:
            status_code = response.status
    except aiohttp.ClientResponseError as e:
        status_code = e.status
    except asyncio.TimeoutError:
        status_code= 408
    except Exception as e:
        logger.exception(f"{e}")
        status_code = 500
    try:
       await error_mail_producer(job_id, status_code,email, url, data['notify_on_error'], producer)
    except Exception as e:
       logger.exception(e) 
    return {"status":status_code, "url":url, "job_id":job_id, "timestamp":datetime.utcnow()}


async def error_mail_producer(job_id, status_code, email,url,notify_on_error, producer):
    if status_code > 400:
        try: 
            await job_table.update_one({"_id": ObjectId(job_id)}, {"$inc": {"error_count": 1}})
            if notify_on_error:
                await producer.send("error-mail",{"code":status_code, "email":email, "cron":url })
        except Exception as e:
            logger.exception(f"An exception occurred while updating cron table for cron {job_id}: {str(e)}")
    else:
      pass

async def update_cron(record, schedule):
    year= schedule["years"]
    month=schedule["month"]
    weekday=schedule["weekday"]
    day=schedule["days"]
    hours=schedule["hours"]
    minute=schedule["minutes"]
    timezone=schedule["timezone"]

    # finding the next execution of the cron and updating the table
    upper_execution= next_execution(timezone, year, month, weekday, day, hours, minute)
    job_table.update_one({"_id": record["_id"]}, {"$set": {"schedule.next_execution": upper_execution}})

      


async def cron_job(producer):
      try:
        tasks=[]
        update_crons=[] 
        # filtering through the database to find crons whose schedule time are less than or equal to the current UTC time
        async for cron in job_table.find({"schedule.next_execution":{"$lte": datetime.now(tz=pytz.timezone("UTC"))}, "error_count":{"$lt":max_failures}}):
            next_execution=cron['schedule']["next_execution"]
            timezone=cron["schedule"]["timezone"]

            #converting the time to the specified timezone because timezones change. and checking if the scheduled time is equal to the current time in that cron timezone
            if datetime.now(tz=pytz.timezone(timezone)) >= next_execution.replace(tzinfo=pytz.timezone(timezone)):
                url=cron["url"]
                job_id=str(cron["_id"])
                method=cron["method"]
                schedule=cron["schedule"]
                header=cron["headers"]
                body=cron["body"]
                email=cron["user"]["email"]
                task = asyncio.create_task(producer.send(CRON_TOPIC, {"url":url, "job_id":job_id, "method":method, "header":header, "body":body, "email":email, "notify_on_error":schedule["notify_on_error"]}))
                tasks.append(task)
                u_task=asyncio.create_task(update_cron(cron, schedule)) 
                update_crons.append(u_task)
        await asyncio.gather(*tasks)
        await asyncio.gather(*update_crons)
        if len(tasks) > 0:
           logger.info(len(tasks))
      except Exception as e:
        logger.error(f"Error in CronJob: {e}")




async def start_cron_job():
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

    async with AIOKafkaProducer(**producer_conf) as producer:
      try:
        await producer.start()
        logger.info("worker started 🚀.")
        while True:

            '''A loop that occurs every 1 minute , and calls the main coroutine 
            which then finds any cron which its scheduled time is at this particular minute
            '''
            st=datetime.utcnow()
            await cron_job(producer)
            logger.info(f"Producing finished {datetime.now() - st} ")
            next_minute = (datetime.utcnow() + timedelta(minutes=1)).replace(second=0, microsecond=0)
            delay = (next_minute - datetime.utcnow()).total_seconds()
            await asyncio.sleep(delay)
      except Exception as e:
        logger.error(f"Error in Producer: {e}")
      finally:
         await producer.stop()

if __name__ == "__main__":
    asyncio.run(start_cron_job())




