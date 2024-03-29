from ..database import user_table
from bson.objectid import ObjectId
from datetime import datetime
from pytz import timezone
from fastapi import HTTPException

from passlib.context import CryptContext

pwd_hash=CryptContext(schemes=['bcrypt'], deprecated='auto')
def hash_password(password):
    return pwd_hash.hash(password)
def verify_password(plain_password, hashed_password):
    return pwd_hash.verify(plain_password, hashed_password)
class UserCrud:

    async def get_user_by_id(id):
        user= await user_table.find_one({"_id":ObjectId(id)})
        return {"_id":user["_id"], "email":user['email'], "fullname":user["fullname"]}

    async def create_user(schema):
        user= await user_table.insert_one({'email':schema.email, 'password':hash_password(schema.password), 'fullname':schema.fullname, 'date_joined':datetime.now(tz=timezone("UTC"))})
        return user.inserted_id
    
    async def get_user_by_email(email):
        return await user_table.find_one({"email":email})

    async def authenticate(email, password):
        user=await user_table.find_one({'email':email})
        if user:
            if verify_password(password, user['password']):
                return user
            raise HTTPException(detail="invalid email or password", status_code=401)
        raise HTTPException(detail="invalid email or password", status_code=401)

    
