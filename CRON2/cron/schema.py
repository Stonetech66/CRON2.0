from pydantic import BaseModel, validator, Field, HttpUrl
from enum import Enum
from bson.objectid import ObjectId
from typing import Any
from .validators import timezone_valid

from datetime import datetime

class Methods(str,Enum):
    GET="get"
    POST="post"
    HEAD="head"
    OPTIONS="options"
    PUT="put"
    DELETE="delete"
    PATCH="patch"


class Weekdays(str, Enum):
    monday='MO'
    tuesday= 'TU'
    wednesday='WE'
    thursday='TH'
    friday='FR'
    saturday='SA'
    sunday='SU'


class MongoId(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance (v, ObjectId):
            raise ValueError(" Invalid object id")
        return str(v)

    def to_representation(self):
        return str(self)

class ID(BaseModel):
    id:MongoId=Field(alias="_id")

class CronBase(BaseModel):
    url:HttpUrl
    method:Methods=Field(default='get')
    headers:dict =Field(default=None)
    body:Any=Field(default=None,)
    notify_on_error: bool= Field(default=True)

class  CronSchema(BaseModel):
    url:HttpUrl
    method:Methods=Field(default='get')
    headers:dict =Field(default=None)
    body:Any=Field(default=None,)
    notify_on_error: bool= Field(default=True)
    minutes:int=Field(default=0,le=59)
    hours:int=Field(default=0, le=23)
    days:int=Field(default=0)
    weekday:Weekdays=Field(default=None)
    month:int=Field(default=0,  le=31)
    years:int=Field(default=0)
    timezone:str


    

    class Config:

        schema_extra={
            "example":
            {
                "url": "https://example.com",
                "method": "get",
                "headers": {"Authorization": "Bearer xxxxxxx"},
                "timezone":"Africa/Lagos",
                "weekday":"MO",
                "hours":9,
                "minutes":0,
                "notify_on_error": False
            }
        }

    @validator("month")
    def validate_month(cls, v, values, **kwargs):
        if not v==0 and not values["hours"]:
            raise ValueError(f"you chose {v} of every month, you are to also provide a time e.g hours=18, minutes=0 i.e every {v} of the month  by 6:00 pm ")
        return v
    
    @validator("weekday")
    def validate_weekday(cls, v, values, **kwargs):
        if v and not values["hours"] :
            raise ValueError(f"you are to also provide a time e.g hours=18, minutes=30 i.e every {v}  by 6:30 pm ")
        return v
    
    @validator("days")
    def validate_days(cls, v, values, **kwargs):
        if not v==0 and not values["hours"] :
            raise ValueError(f"you are to also provide a time e.g hours=18, minutes=0 i.e every {v} days  by 6:00 pm ")
        return v
    

    
    @validator('timezone')
    def validate_timezone(cls, v):
        if not timezone_valid(v):
            raise ValueError("invalid timezone provided")
        return v


class Response(ID):
    status_code:int
    date:datetime
class CronSchemaDetails(CronBase, ID):
    schedule:dict
    class Config:
        arbitrary_types_allowed=True
        allow_population_by_field_name=True











