from ..database import cron_table, response_table
from .schema import CronSchemaDetails
from bson.objectid import ObjectId
from fastapi import HTTPException
from .schema import CronSchema
from ..utils import find_next_execution
import pytz
from datetime import datetime
from fastapi import HTTPException



class Cron:
    cron_error=HTTPException(detail="cron dosent exists", status_code=404)

    async def create_cron(schema:CronSchema, user:dict)-> dict:
        try:
           cron_data={}
           schedule_data={}
           cron_data['url']=schema.url
           cron_data['method']=schema.method
           cron_data['headers']=schema.headers
           cron_data['body']=schema.body
           schedule_data['notify_on_error']= schema.notify_on_error
           cron_data["date_added"]= datetime.now()
           schedule_data['years']=schema.years
           schedule_data['month']=schema.month
           schedule_data['weekday']=schema.weekday
           schedule_data['days']=schema.days
           schedule_data['hours']=schema.hours
           schedule_data['minutes']=schema.minutes
           schedule_data['timezone']=schema.timezone
           schedule_data['date_created']= datetime.now()
           schedule_data['next_execution']=find_next_execution(schema.timezone, schema.years, schema.month, schema.weekday, schema.days, schema.hours, schema.minutes)
           cron_data['schedule']=schedule_data
           cron= await cron_table.insert_one({**cron_data , 'user':{'_id':user['_id'], 'email':user['email']} , "error_count":0})
        
        except:
            raise HTTPException(detail=f"{e}", status_code=400)
        return {"_id":cron.inserted_id,**cron_data}

    async def get_crons(user_id:str,skip:int=0, limit:int=5, )-> list:
        cron_list=[]
        try:
            async for cron in cron_table.find({"user._id":ObjectId(user_id)}).limit(limit).skip(skip):
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
            schedule_data['notify_on_error']= schema.notify_on_error
            schedule_data['years']=schema.years
            schedule_data['month']=schema.month
            schedule_data['weekday']=schema.weekday
            schedule_data['days']=schema.days
            schedule_data['hours']=schema.hours
            schedule_data['minutes']=schema.minutes 
            schedule_data['timezone']=schema.timezone
            schedule_data['next_execution']=find_next_execution(schema.timezone, schema.years, schema.month, schema.weekday, schema.days, schema.hours, schema.minutes)
            cron_data['schedule']=schedule_data
            cron_data['error_count'] = 0
            cron= await cron_table.update_one({"_id": ObjectId(id), "user._id":ObjectId(user_id)},{"$set":cron_data})
            cron_data.pop('error_count') 
            if cron.matched_count==1:
                return {"_id":ObjectId(id),**cron_data}
            raise cls.cron_error
        except Exception as e:
            raise cls.cron_error
        

    @classmethod
    async def delete_cron(cls, id:str, user_id:str):
        cron= await cron_table.delete_one({"_id": ObjectId(id), "user._id":ObjectId(user_id)})
        if cron.deleted_count ==1:
            return True
        raise cls.cron_error
    

    @classmethod
    async def get_cron(cls,id:str, user_id:str):
        try:
            cron= await cron_table.find_one({"_id": ObjectId(id), "user._id":ObjectId(user_id)})
            if cron:
                return cron
            raise cls.cron_error
        except:
            raise cls.cron_error
    @classmethod
    async def get_response_history(cls, cron_id, skip, limit):
        try:
            response_list=[]
            async for resp in response_table.find({"cron_id":ObjectId(cron_id)}).skip(skip).limit(limit):
                response_list.append(resp)
                print(resp) 
            return response_list
        except:
            raise cls.cron_error
    @classmethod
    async def clear_response_history(cls, cron_id):
        try:
            return await response_table.delete_many({"cron_id":ObjectId(cron_id)})
        except:
            raise cls.cron_error
    async def get_response(id:str):
         try:
            resp= await response_table.find_one({"_id": ObjectId(id),})
            if resp:
                return resp
            raise HTTPException(detail="response doesn't exists", status_code=404)
         except:
             raise HTTPException(detail="response doesn't exists", status_code=404)
    
    async def delete_response(id:str):
        try:
            resp= await response_table.delete_one({"_id": ObjectId(id)})
            if resp.deleted_count ==1:
                return True
        except:
            pass
        raise HTTPException(detail="response doesn't exists", status_code=404)

    
    async def insert_many_response(data):
        await response_table.insert_many(data)

        
    




