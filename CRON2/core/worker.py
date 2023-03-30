from ..database import cron_table
from datetime import datetime, timedelta 
import asyncio
import pytz, ssl
import aiohttp
from ..utils import next_execution, error_code
from bson.objectid import ObjectId
import json
from aiokafka import AIOKafkaProducer
import os
from dotenv import load_dotenv
import os

load_dotenv()
server=os.getenv('KAFKA_SERVER')
kafka_password=os.getenv("KAFKA_PASSWORD")
kafka_username= os.getenv("KAFKA_USERNAME")
CRON_MAXIMUM_FAILURES=1 
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


timeout=aiohttp.ClientTimeout(total=30)




async def send_requests(session, data, producer):
    method=data['method']
    header=data['header']
    schedule= data['schedule']
    schedule.update({'next_execution': datetime.fromisoformat(schedule['next_execution'])})
    url= data['url']
    cron_id= ObjectId(data['cron_id'])
    body= data['body']
    email=data["email"]
    print(f"{url} {datetime.now()}")
    # sending http requests to the specified endpoint
    try:
            if method == "get":
                    async with session.get(url, timeout=timeout, headers=header) as response:
                        status_code= response.status
            elif method== "post":
                async with session.post(url, timeout=timeout, headers=header, json=body) as response:
                    status_code= response.status
            elif method == "put":
                async with session.put(url, timeout=timeout, headers=header, json=body) as response:
                    status_code= response.status
            elif method== "delete":
                async with session.delete(url, timeout=timeout, headers=header) as response:
                    status_code= response.status
            elif method == "head":
                async with session.head(url, timeout=timeout, headers=header) as response:
                    status_code= response.status
            elif method == "options":
                async with session.options(url, timeout=timeout, headers=header) as response:
                    status_code= response.status
            elif method == "patch":
                async with session.patch(url, timeout=timeout, headers=header) as response:
                    status_code= response.status
            else: 
                status_code = 500
    except:
        status_code=500


    await save_responses(schedule, cron_id, status_code,email, producer)
    return {"status_code":status_code, "cron_id":cron_id, "date":datetime.now()}


async def save_responses(schedule:dict, cron_id, status_code, email, producer):
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
        await cron_table.update_one({"_id": ObjectId(cron_id)}, {"$set": {"schedule.next_execution": upper_execution}, "$inc": {"error_count": 1}})
        if schedule['notify_on_error']:
            await producer.send("error-mail",{"code":status_code, "email":email})
    else:
        await cron_table.update_one({"_id":ObjectId(cron_id)}, {"$set": {"schedule.next_execution":upper_execution}})




async def CronJob(producer):

        tasks=[]
        # filtering through the database to find crons whose schedule time are less than or equal to the current UTC time
        async for cron in cron_table.find({"schedule.next_execution":{"$lte": datetime.now(tz=pytz.timezone("UTC"))}, "error_count":{"$lt":3}}):
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
                task = asyncio.create_task(producer.send('cron-2', {"url":url, "cron_id":cron_id, "method":method, "schedule":schedule, "header":header, "body":body, "email":email}))
                tasks.append(task)
        start=datetime.now()
        await asyncio.gather(*tasks)
        print(f"producing finished: {datetime.now() - start}")



async def Startcron():
    producer=AIOKafkaProducer(
    bootstrap_servers=[server], 
    security_protocol="SASL_SSL", sasl_mechanism="PLAIN", 
    sasl_plain_username=kafka_username, 
    sasl_plain_password=kafka_password, 
    ssl_context=ssl.create_default_context(),compression_type="gzip", value_serializer=lambda x: json.dumps(x, cls=CustomJsonEncoder).encode('utf-8'))
    try:
        await producer.start()
        print("worker started 🚀")
        while True:

            '''A loop that occurs every 1 minute , and calls the main coroutine 
            which then finds any cron which its scheduled time is at this particular minute
            '''
            st=datetime.now()
            await CronJob(producer)
            print(datetime.now() - st)
            next_minute = (datetime.now() + timedelta(minutes=1)).replace(second=0, microsecond=0)
            delay = (next_minute - datetime.now()).total_seconds()
            await asyncio.sleep(delay)
    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(Startcron())




