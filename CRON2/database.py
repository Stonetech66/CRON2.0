from motor import motor_asyncio
from dotenv import load_dotenv
import os
load_dotenv()
client=motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db=client['cron2']
user_table=db['users']
job_table=db['job']
response_table=db['response']
