import asyncio, aiohttp
from datetime import datetime
from CRON2.database import cron_table

async def fetch(session, url, c):
    async with session.post(url, json=c, headers={"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2M2ZlOTkzYmYzOGUzZmEwNDQzZTM1Y2MiLCJpYXQiOjE2NzgyNDcwMzcsIm5iZiI6MTY3ODI0NzAzNywianRpIjoiOGIyYTU5OTgtNDgwZS00MzMxLTk1YzEtN2JlOWU0YmQ4ZTliIiwiZXhwIjoxNjc4MjQ3OTM3LCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlfQ.oIsdRJzXGReBLqu6sfxABdSsOIYJfIqSRc1ZmfpTpuc"}) as response:
             return  response.status


async def start_test(s_url,token,end): 
     c={
     "url": s_url,
     "method": "get",
     "headers": {
     "Authorization": f"Bearer {token}"
     },
     "timezone": "Africa/Lagos",
     "notify_on_error":True,
     "minutes": 5
          }                            
     async with aiohttp.ClientSession() as session:
             tasks=[]
             for u in [f'{end}/v1/add-cron/'] * 500:
                     tasks.append(asyncio.ensure_future(fetch(session, u, c)))
             responses= await asyncio.gather(*tasks)
             return responses



if __name__ == "__main__":
    start=datetime.now()
    asyncio.run(go())
    print(datetime.now() - start)

