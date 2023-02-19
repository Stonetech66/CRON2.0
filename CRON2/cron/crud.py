from ..database import cron_table, response_table
from .schema import CronSchemaDetails
from bson.objectid import ObjectId
from fastapi import HTTPException
from .schema import CronSchema
from ..utils import next_execution
import pytz
from datetime import datetime
from fastapi import HTTPException



class Cron:
    cron_error=HTTPException(detail="cron dosent exists", status=404)

    async def create_cron(schema:CronSchema, user_id:str)-> dict:
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
        cron= await cron_table.insert_one({**cron_data , 'user_id':ObjectId(user_id)})
        return {"_id":cron.inserted_id,**cron_data}

    async def get_crons(user_id:str,skip:int=0, limit:int=5, )-> list:
        cron_list=[]
        try:
            async for cron in cron_table.find({"user_id":ObjectId(user_id)}).limit(limit).skip(skip):
                cron_list.append(cron)
        except:
            pass
        return cron_list
    @classmethod
    async def update_cron(cls, id:str, schema:CronSchema, user_id:str):
        try:

            cron_data={}
            schedule_data={}
            cron_data['url']=schema.url
            cron_data['method']=schema.method
            cron_data['headers']=schema.headers
            cron_data['body']=schema.body
            schedule_data['years']=schema.years
            schedule_data['months']=schema.months
            schedule_data['weekday']=schema.weekday
            schedule_data['days']=schema.days
            schedule_data['hours']=schema.hours
            schedule_data['minutes']=schema.minutes 
            schedule_data['timezone']=schema.timezone
            schedule_data['next_execution']=next_execution(schema.timezone, schema.years, schema.months, schema.weekday, schema.days, schema.hours, schema.minutes)
            cron_data['schedule']=schedule_data
            cron= await cron_table.update_one({"_id": ObjectId(id), "user_id":ObjectId(user_id)},{"$set":cron_data})
            if cron.updated_count==1:
                return {"_id":ObjectId(id),**cron_data}
            raise cls.cron_error
        except:
            raise cls.cron_error

    async def delete_cron(cls, id:str, user_id:str):
        cron= await cron_table.delete_one({"_id": ObjectId(id), "user_id":ObjectId(user_id)})
        if cron.deleted_count ==1:
            return True
        raise cls.cron_error

    async def get_cron(cls,id:str, user_id:str):
        try:
            cron= await cron_table.find_one({"_id": ObjectId(id), "user_id":ObjectId(user_id)})
            if cron:
                return cron
            raise cls.cron_error
        except:
            raise cls.cron_error

    async def get_response_history(cron_id, skip, limit):

            response_list=[]
            async for resp in response_table.find({"cron_id":cron_id}).skip(skip).limit(limit):
                response_list.append(resp)
            return response_list
 
    async def clear_response_history(cron_id):
        return await response_table.delete_many({"cron_id":cron_id})
    



        
    




