from celery import Celery
app=Celery(__name__)
from .database import cron_table, response_table
from datetime import datetime
import asyncio
import pytz
import aiohttp
from .utils import find_next_execution
from bson.objectid import ObjectId





timeout=aiohttp.ClientTimeout(total=30)

async def send_requests(url, method, header, body, cron_id, timeout, next_execution):
    try:
        async with aiohttp.ClientSession() as session:
            if method == "get":
                    async with session.get(url, timeout=timeout, headers=header) as response:
                        status_code= response.status
            elif method== "post":
                async with session.post(url, timeout=timeout, headers=header, body=body) as response:
                    status_code= response.status
            elif method == "put":
                async with session.put(url, timeout=timeout, headers=header) as response:
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
    response_table.insert_one({"staus_code":status_code, "cron_id":cron_id, "date":next_execution})
    x=await cron_table.find_one({"_id": ObjectId(cron_id)})
    year= x["schedule"]["years"]
    month=x["schedule"]["months"]
    week=x["schedule"]["weeks"]
    day=x["schedule"]["days"]
    hour=x["schedule"]["hours"]
    minute=x["schedule"]["minutes"]
    timezone=x["schedule"]["timezone"]
    upper_execution= find_next_execution(next_execution, timezone, year, month, week, day, hour, minute)
    c=await cron_table.update_one({"id":cron_id}, {"$set": {"schedule.next_execution":upper_execution}})
    return c


async def main():
    tasks=[]
    async for cron in cron_table.find({"schedule.next_execution":{"$lte": datetime.now(tz=pytz.timezone("UTC"))}}):
        url=cron["url"]
        cron_id=cron["_id"]
        method=cron["method"]
        next_execution=cron["schedule"]["next_execution"]
        header=cron["headers"]
        body=cron["body"]
        timezone=cron["schedule"]["timezone"]
        if datetime.now(tz=pytz.timezone(timezone)) >= next_execution.replace(tzinfo=pytz.timezone(timezone)):
            task = asyncio.ensure_future(send_requests(url, method, header, body, cron_id,0,next_execution))
            tasks.append(task)
    cron= await asyncio.gather(*tasks)
    return cron



            




async def Startcron():
    while True:

        await asyncio.gather(main())
        await asyncio.sleep(60)

        

            




# celery conf
# @app.task
# def CronJob2():
#     asyncio.run(main())

# app.conf.beat_schedule= {
#     'send_sceduled_letters':{
#         'task': 'CRON2.worker.CronJob',
#         'schedule':60,

#     }

# }