from ..database import cron_table
from .schema import CronSchemaDetails
from bson.objectid import ObjectId
from fastapi import HTTPException
from .schema import CronSchema
from .utils import next_execution
import pytz
from datetime import datetime
from fastapi import HTTPException



class Cron:

    async def create_cron(schema:CronSchema)-> dict:
        cron_data={}
        schedule_data={}
        cron_data['url']=schema.url
        cron_data['method']=schema.method
        cron_data['headers']=schema.headers
        cron_data['body']=schema.body
        schedule_data['years']=schema.years
        schedule_data['months']=schema.months
        schedule_data['weeks']=schema.weeks
        schedule_data['days']=schema.days
        schedule_data['hours']=schema.days
        schedule_data['minutes']=schema.days
        schedule_data['timezone']=schema.timezone
        schedule_data['next_execution']=next_execution(schema.timezone, schema.years, schema.months, schema.weeks, schema.days, schema.hours, schema.minutes)
        cron_data['schedule']=schedule_data
        cron= await cron_table.insert_one({**cron_data })
        return {"_id":cron.inserted_id,**cron_data}

    async def get_crons(skip:int=0, limit:int=5)-> list:
        cron_list=[]
        async for cron in cron_table.find().limit(limit).skip(skip):
            cron_list.append(cron)
        v= await cron_table.find({"schedule.next_execution":{"$lte": datetime.now(tz=pytz.timezone("UTC"))}}).to_list(100)
        print(v)

        return cron_list
    async def update_cron(id:str, schema:CronSchema):
        cron_data={}
        schedule_data={}
        cron_data['url']=schema.url
        cron_data['method']=schema.method
        cron_data['headers']=schema.headers
        cron_data['body']=schema.body
        schedule_data['years']=schema.years
        schedule_data['months']=schema.months
        schedule_data['weeks']=schema.weeks
        schedule_data['days']=schema.days
        schedule_data['hours']=schema.hours
        schedule_data['minutes']=schema.minutes 
        schedule_data['timezone']=schema.timezone
        schedule_data['next_execution']=next_execution(schema.timezone, schema.years, schema.months, schema.weeks, schema.days, schema.hours, schema.minutes)
        cron_data['schedule']=schedule_data
        cron= await cron_table.update_one({"_id": ObjectId(id)},{"$set":cron_data})
        return {"_id":ObjectId(id),**cron_data}

    async def delete_cron(id:str):
        cron= await cron_table.delete_one({"_id": ObjectId(id)})
        return True

    async def get_cron(id:str):
        cron= await cron_table.find_one({"_id": ObjectId(id)})
        if cron:
            return cron
        raise HTTPException(detailt="error this cron dosent exists", status_code=404)
    



        
    




