from pydantic import BaseModel, validator, Field
from enum import Enum
from bson.objectid import ObjectId
from typing import Union, Any
from .validators import timezone_valid, url_valid

class Methods(str,Enum):
    GET="get"
    POST="post"
    HEAD="head"
    OPTIONS="options"
    PUT="put"
    DELETE="delete"
    PATCH="patch"



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

class CronBase(BaseModel):
    url:str
    method:Methods
    headers:dict =Field(default=None)
    body:Any=Field(default=None,)


class  CronSchema(CronBase):
    years:int=Field(default=0)
    months:int=Field(default=0, description="number of months", le=12)
    weeks:int=Field(default=0, description="number of weeks", le=4)
    days:int=Field(default=0)
    hours:int=Field(default=0, le=24)
    minutes:int=Field(default=1,le=60)
    timezone:str

    class Config:

        schema_extra={
            "example":
            {
                "url": "https://example.com",
                "method": "get",
                "headers": {"Authorization": "Bearer xxxxxxx"},
                "timezone":"Africa/Lagos",
                "days":1,
                "hours":3,
            }
        }
    @validator('timezone')
    def validate_timezone(cls, v):
        if not timezone_valid(v):
            raise ValueError("invalid timezone provided")
        return v
    @validator('url')
    def validate_url(cls, v):
        if not url_valid(v):
            raise ValueError("invalid url provided")
        return v
class CronSchemaDetails(CronBase):
    id: MongoId= Field(alias="_id")
    schedule:dict
    class Config:
        arbitrary_types_allowed=True
        allow_population_by_field_name=True











