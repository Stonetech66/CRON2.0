from ..database import job_table, response_table
from bson.objectid import ObjectId
from fastapi import HTTPException
from .schema import CronSchema
from ..utils import find_next_execution
import pytz
from datetime import datetime
from fastapi import HTTPException



class Cron:
    job_error=HTTPException(detail="job dosent exists", status_code=404)

    async def create_job(schema:CronSchema, user:dict)-> dict:
        try:
           job_data={}
           schedule_data={}
           next_execution= find_next_execution(schema.timezone, schema.years, schema.month, schema.weekday, schema.days, schema.hours, schema.minutes)
           if next_execution == None:
                raise HTTPException(detail="Invalid schedule date or time", status_code=400)
           job_data['url']=schema.url
           job_data['method']=schema.method
           job_data['headers']=schema.headers
           job_data['body']=schema.body
           schedule_data['notify_on_error']= schema.notify_on_error
           job_data["timestamp"]= datetime.now()
           schedule_data['years']=schema.years
           schedule_data['month']=schema.month
           schedule_data['weekday']=schema.weekday
           schedule_data['days']=schema.days
           schedule_data['hours']=schema.hours
           schedule_data['minutes']=schema.minutes
           schedule_data['timezone']=schema.timezone
           schedule_data['next_execution']=next_execution
           job_data['schedule']=schedule_data
           job= await job_table.insert_one({**job_data , 'user':{'_id':user['_id'], 'email':user['email']} , "error_count":0})
        
        except Exception as e:
            raise HTTPException(detail=f"{e}", status_code=400)
        return {"_id":job.inserted_id, "message":"Job created successfully", "next_execution":schedule_data["next_execution"]}

    async def get_jobs(user_id:str,skip:int=0, limit:int=5, )-> list:
        job_list=[]
        try:
            async for job in job_table.find({"user._id":ObjectId(user_id)}).limit(limit).skip(skip).sort("timestamp" , -1 ):
                job_list.append(job)
        except:
            pass
        return job_list
    @classmethod
    async def update_job(cls, id:str, schema:CronSchema, user_id:str):
        try:

            job_data={}
            schedule_data={}
            next_execution=find_next_execution(schema.timezone, schema.years, schema.month, schema.weekday, schema.days, schema.hours, schema.minutes)
            if next_execution  == None:
                raise HTTPException(detail="Invalid schedule date or time", status_code=400 )
            job_data['url']=schema.url
            job_data['method']=schema.method
            job_data['headers']=schema.headers
            job_data['body']=schema.body
            schedule_data['notify_on_error']= schema.notify_on_error
            schedule_data['years']=schema.years
            schedule_data['month']=schema.month
            schedule_data['weekday']=schema.weekday
            schedule_data['days']=schema.days
            schedule_data['hours']=schema.hours
            schedule_data['minutes']=schema.minutes 
            schedule_data['timezone']=schema.timezone
            schedule_data['next_execution']=next_execution
            job_data['schedule']=schedule_data
            job_data['error_count'] = 0
            job= await job_table.update_one({"_id": ObjectId(id), "user._id":ObjectId(user_id)},{"$set":job_data})
            job_data.pop('error_count') 
            if job.matched_count==1:
                return {"_id":ObjectId(id),"message": "Job updated sucessfully", "next_execution": next_execution}
            raise cls.job_error
        except Exception as e:
            raise cls.job_error
        

    @classmethod
    async def delete_job(cls, id:str, user_id:str):
        job= await job_table.delete_one({"_id": ObjectId(id), "user._id":ObjectId(user_id)})
        if job.deleted_count ==1:
            return True
        raise cls.job_error
    

    @classmethod
    async def get_job(cls,id:str, user_id:str):
        try:
            job= await job_table.find_one({"_id": ObjectId(id), "user._id":ObjectId(user_id)})
            if job:
                return job
            raise cls.job_error
        except:
            raise cls.job_error
    @classmethod
    async def get_response_history(cls, job_id, skip, limit):
        try:
            response_list=[]
            async for resp in response_table.find({"job_id":job_id}).skip(skip).limit(limit).sort("timestamp" , -1):
                response_list.append(resp)
            return response_list
        except:
            raise cls.job_error
    @classmethod
    async def clear_response_history(cls, job_id):
        try:
            return await response_table.delete_many({"job_id":ObjectId(job_id)})
        except:
            raise cls.job_error
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

        
    




