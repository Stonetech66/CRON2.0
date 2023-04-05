from datetime import datetime, timedelta
import pytz
from ..utils import next_execution
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from .schema import CronSchema, CronSchemaDetails, Response
from ..database import cron_table, db, response_table
from .crud import Cron
from ..dependencies import get_current_user
from bson.objectid import ObjectId
from ..test import start_test 
import asyncio
cron=Cron


router=APIRouter(prefix='/v1')

@router.post('/add-cron', status_code=201, response_model=CronSchemaDetails,response_model_exclude_unset=True,  response_model_by_alias=False)
async def add_cron(schema:CronSchema, user=Depends(get_current_user)):
    result =await Cron.create_cron(schema, user)
    return result

@router.get('/crons', response_model=List[CronSchemaDetails], response_model_exclude_unset=True)
async def get_crons(limit:int=10, skip:int=0, user=Depends(get_current_user)):
    cron= await Cron.get_crons(skip=skip, limit=limit, user_id=str(user["_id"]))
    return cron

@router.put('/update-cron/{cron_id}', response_model=CronSchemaDetails)
async def update_cron(schema:CronSchema, cron_id:str, user=Depends(get_current_user)):
    result= await Cron.update_cron(cron_id, schema, str(user["_id"]))
    return result

@router.delete("/delete-cron/{cron_id}", status_code=204)
async def delete_cron(cron_id:str, user=Depends(get_current_user)):
    x= await Cron.delete_cron(cron_id, str(user["_id"]))
    return x


@router.get("/cron/{cron_id}", response_model=CronSchemaDetails)
async def get_cron(cron_id:str, user=Depends(get_current_user)):
    cron= await Cron.get_cron(cron_id, str(user["_id"]))
    return cron

@router.get("/cron-response/history/{cron_id}", response_model=list[Response])
async def cron_response_history(cron_id:str, skip:int=0, limit:int=10,user=Depends(get_current_user)):
    cron=await Cron.get_cron(cron_id, str(user["_id"]))
    response=await  Cron.get_response_history(cron_id, skip, limit)
    return response


@router.delete("/clear-cron-response-history/{cron_id}", status_code=204)
async def delete_response_history(cron_id:str, user=Depends(get_current_user)):

    cron=await Cron.get_cron(cron_id, str(user["_id"]))
    response= await Cron.clear_response_history(cron_id)
    return "success"

@router.post("/test/{access}/")
async def test(access:str, url:str, min:int, hour:int, no:int):
   await start_test("http//:example.com",access,"https://cron20-production.up.railway.app", url, no, min, hour) 
   return "success" 
@router.get("/cron-response/{response_id}", response_model=Response)
async def get_response(response_id:str, user=Depends(get_current_user) ):
     resp= await Cron.get_response(response_id)
     return resp

@router.delete("/delete-response/{response_id}", status_code=204)
async def delete_response(response_id:str, user=Depends(get_current_user)):
    response= await Cron.delete_response(response_id)
    return "success"

@router.get("/timeout")
async def timeout(time:int):
   await asyncio.sleep(time)
   return "success" 

@router.get("/count")
async def timeout():
   count= await response_table.count_documents({})
   return count 

