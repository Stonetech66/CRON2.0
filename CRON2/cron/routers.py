from typing import List
from fastapi import APIRouter, Depends
from .schema import CronSchema, CronSchemaDetails, Response, CronResponseSchema 
from .crud import Cron
from ..dependencies import get_current_user




router=APIRouter(prefix='/v1', tags=["jobs"] )

@router.post('/jobs', status_code=201, response_model=CronResponseSchema,response_model_exclude={"notify_on_error"})
async def add_job(schema:CronSchema, user=Depends(get_current_user)):
    job =await Cron.create_job(schema, user)
    return job

@router.get('/jobs', response_model=List[CronSchemaDetails], response_model_exclude={"notify_on_error"})
async def get_jobs(limit:int=10, skip:int=0, user=Depends(get_current_user)):
    jobs= await Cron.get_jobs(skip=skip, limit=limit, user_id=str(user["_id"]))
    return jobs

@router.put('/jobs/{job_id}', response_model=CronResponseSchema, response_model_exclude={"notify_on_error"})
async def update_job(schema:CronSchema, job_id:str, user=Depends(get_current_user)):
    job= await Cron.update_job(job_id, schema, str(user["_id"]))
    return job

@router.delete("/jobs/{job_id}", status_code=204)
async def delete_job(job_id:str, user=Depends(get_current_user)):
    delete= await Cron.delete_job(job_id, str(user["_id"]))
    return delete


@router.get("/jobs/{job_id}", response_model=CronSchemaDetails, response_model_exclude={"notify_on_error"})
async def get_job(job_id:str, user=Depends(get_current_user)):
    job= await Cron.get_job(job_id, str(user["_id"]))
    return job

@router.get("/response/history/{job_id}", response_model=List[Response], response_model_exclude={"job_id", "url"})
async def cron_response_history(job_id:str, skip:int=0, limit:int=10,user=Depends(get_current_user)):
    job=await Cron.get_job(job_id, str(user["_id"]))
    response=await  Cron.get_response_history(job_id, skip, limit)
    return response


@router.delete("/response/history/{job_id}", status_code=204)
async def delete_response_history(job_id:str, user=Depends(get_current_user)):

    job=await Cron.get_job(job_id, str(user["_id"]))
    response= await Cron.clear_response_history(job_id)
    return "success"


@router.get("/response/{response_id}", response_model=Response)
async def get_response(response_id:str, user=Depends(get_current_user) ):
     resp= await Cron.get_response(response_id)
     return resp

@router.delete("/response/{response_id}", status_code=204)
async def delete_response(response_id:str, user=Depends(get_current_user)):
    response= await Cron.delete_response(response_id)
    return "success"



"""
@router.get("/timeout")
async def timeout(time:int):
   await asyncio.sleep(time)
   return "success" 

@router.get("/count")
async def timeout():
   count= await response_table.count_documents({})
   return count 

@router.post("/test/{access}/")
async def test(access:str, url:str, min:int, hour:int, no:int):
   await start_test("http//:example.com",access,"https://cron20-production.up.railway.app", url, no, min, hour) 
   return "success" 
"""