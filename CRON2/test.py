import asyncio, aiohttp
from datetime import datetime
from CRON2.database import cron_table

async def fetch(session, url, c, token):
    async with session.post(url, json=c, headers={"Authorization":f"Bearer {token}"}) as response:
             return  response.status


async def start_test(s_url,token,end, url, no, min, hour): 
     c={
  "url": f"{url}",
  "method": "get",
  "headers": {
    "Authorization": "Bearer xxxxxxx"
  },
  "timezone": "Africa/Lagos",
  "days" :1,
  "hours":hour, 
  "minutes": min,
  "notify_on_error": False
}                       
     async with aiohttp.ClientSession() as session:
             tasks=[]
             for u in [f'{end}/v1/add-cron/'] * no:
                     tasks.append(asyncio.ensure_future(fetch(session, u, c, token)))
             responses= await asyncio.gather(*tasks)
             return responses



if __name__ == "__main__":
    start=datetime.now()
    asyncio.run(go())
    print(datetime.now() - start)

