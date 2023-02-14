from datetime import datetime, timedelta
import pytz
from .utils import next_execution
from typing import List
from fastapi import APIRouter, HTTPException
from .schema import CronSchema, CronSchemaDetails
from ..database import cron_table, db
from .crud import Cron

cron=Cron
router=APIRouter(prefix='/cron/v1')

SCHEDULE_MAXIMUM_FAILURES=1

@router.post('/add-cron/', status_code=201)
async def add_cron(schema:CronSchema):
    result =await Cron.create_cron(schema)
    return result

@router.get('/crons', response_model=List[CronSchemaDetails])
async def get_crons(limit:int=10, skip:int=0):
    cron= await Cron.get_crons(skip=skip, limit=limit)
    return cron

@router.put('/update-cron/{cron_id}', response_model=CronSchemaDetails)
async def update_cron(schema:CronSchema, cron_id:str):
    result= await Cron.update_cron(cron_id, schema)
    return result

@router.delete("/delete-cron/{cron_id}", status_code=204)
async def delete_cron(cron_id:str):
    x= await Cron.delete_cron(cron_id)
    return x


@router.get("/cron/{cron_id}", response_model=CronSchemaDetails)
async def get_cron(cron_id:str):
    cron= await Cron.get_cron(cron_id)
    return cron