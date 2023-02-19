from datetime import datetime, timedelta
import pytz
from .utils import next_execution
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from .schema import CronSchema, CronSchemaDetails, Response
from ..database import cron_table, db
from .crud import Cron
from ..dependencies import get_current_user
cron=Cron

router=APIRouter(prefix='/v1',)

CRON_MAXIMUM_FAILURES=1

@router.post('/add-cron/', status_code=201, response_model=CronSchemaDetails, response_model_by_alias=False)
async def add_cron(schema:CronSchema, user=Depends(get_current_user)):
    result =await Cron.create_cron(schema, str(user["_id"]))
    return result

@router.get('/crons', response_model=List[CronSchemaDetails])
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

@router.get("/cron-response/{cron_id}", response_model=Response)
async def cron_response_history(cron_id:str, skip:int=0, limit:int=10,user=Depends(get_current_user)):
    cron=await Cron.get_cron(cron_id, str(user["_id"]))
    response=await  Cron.get_reponse_history(cron_id, skip, limit)
    return response


@router.delete("/clear-response-history/{cron_id}")
async def cron_response_history(cron_id:str, skip:int=0, limit:int=10,user=Depends(get_current_user)):
    cron=await Cron.get_cron(cron_id, str(user["_id"]))
    response= await Cron.clear_response_history(cron_id)
    return JSONResponse("success", status_code=204)