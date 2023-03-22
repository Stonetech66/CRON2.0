from motor import motor_asyncio
from dotenv import load_dotenv
import os
load_dotenv()
client=motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
#client={'cron2':{'users':[], 'cron':[], 'response':[]}}
db=client['cron2']
user_table=db['users']
cron_table=db['cron']
response_table=db['response']
