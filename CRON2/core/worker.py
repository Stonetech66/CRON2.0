from ..database import cron_table
from datetime import datetime, timedelta 
import asyncio
import pytz, ssl
import aiohttp
from ..utils import next_execution, error_code
from bson.objectid import ObjectId
from json import JSONEncoder
from aiokafka import AIOKafkaProducer
import os
from dotenv import load_dotenv
import os
load_dotenv()
KAFKA_SERVER = os.getenv('KAFKA_SERVER')
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
CRON_TOPIC = 'cron-2'
CRON_MAX_FAILURES=3 
REQUEST_TIMEOUT=30 #time in seconds
logger = logging.getLogger(__name__)

class CustomJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
max_failures=CRON_MAX_FAILURES



async def send_request(session, data, producer):
    method=data['method']
    header=data['header']
    schedule= data['schedule']
    schedule.update({'next_execution': datetime.fromisoformat(schedule['next_execution'])})
    url= data['url']
    cron_id= ObjectId(data['cron_id'])
    body= data['body']
    email=data["email"]
    logger.info(f"{url} {datetime.now()}")
    # sending http requests to the specified endpoint
    try:
        async with getattr(session, method)(url, timeout=timeout, headers=header, json=body) as response:
            status_code = response.status
    except aiohttp.ClientResponseError as e:
        status_code = e.status
    except Exception as e:
        status_code = 500
        logger.error(f"request error {e} ") 

    await save_response(schedule, cron_id, status_code,email, producer)
    return {"status":status_code, "url":url, "cron_id":cron_id, "timestamp":datetime.utcnow()}


async def save_response(schedule:dict, cron_id, status_code, email, producer):
    year= schedule["years"]
    month=schedule["month"]
    weekday=schedule["weekday"]
    day=schedule["days"]
    hours=schedule["hours"]
    minute=schedule["minutes"]
    timezone=schedule["timezone"]
    # finding the next execution of the cron and updating the table
    upper_execution= next_execution(timezone, year, month, weekday, day, hours, minute)

    if error_code(status_code):
        try:
            await cron_table.update_one({"_id": ObjectId(cron_id)}, {"$set": {"schedule.next_execution": upper_execution}, "$inc": {"error_count": 1}})
            if schedule['notify_on_error']:
                await producer.send("error-mail",{"code":status_code, "email":email})
        except Exception as e:
            logger.exception(f"An exception occurred while updating cron table for cron {cron_id}: {str(e)}")
    else:
        try:
            await cron_table.update_one({"_id":ObjectId(cron_id)}, {"$set": {"schedule.next_execution":upper_execution}})
        except Exception as e:
            logger.exception(f"An exception occurred while updating cron table for cron {cron_id}: {str(e)}")



async def cron_job(producer):
      try:
        tasks=[]
        # filtering through the database to find crons whose schedule time are less than or equal to the current UTC time
        async for cron in cron_table.find({"schedule.next_execution":{"$lte": datetime.now(tz=pytz.timezone("UTC"))}, "error_count":{"$lt":max_failures}}):
            next_execution=cron['schedule']["next_execution"]
            timezone=cron["schedule"]["timezone"]

            #converting the time to the specified timezone because timezones change. and checking if the scheduled time is equal to the current time in that cron timezone
            if datetime.now(tz=pytz.timezone(timezone)) >= next_execution.replace(tzinfo=pytz.timezone(timezone)):
                url=cron["url"]
                cron_id=str(cron["_id"])
                method=cron["method"]
                schedule=cron["schedule"]
                header=cron["headers"]
                body=cron["body"]
                email=cron["user"]["email"]
                task = asyncio.create_task(producer.send(CRON_TOPIC, {"url":url, "cron_id":cron_id, "method":method, "schedule":schedule, "header":header, "body":body, "email":email}))
                tasks.append(task)
        await asyncio.gather(*tasks)
      except Exception as e:
        logger.error(f"Error in CronJob: {e}")




async def start_cron():
    producer_conf = {
        'bootstrap_servers': [KAFKA_SERVER],
        'security_protocol': "SASL_SSL",
        'sasl_mechanism': "PLAIN",
        'sasl_plain_username': KAFKA_USERNAME,
        'sasl_plain_password': KAFKA_PASSWORD,
        'ssl_context': ssl.create_default_context(),
        'compression_type': "gzip",
        'batch_size':32768, 
        'value_serializer': lambda x: json.dumps(x, cls=CustomJsonEncoder).encode('utf-8'),
    }

    async with AIOKafkaProducer(**producer_conf) as producer:
      try:
        await producer.start()
        logger.info("worker started 🚀")
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
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
    asyncio.run(start_cron())




