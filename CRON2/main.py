from fastapi import FastAPI, BackgroundTasks
from .cron.routers import router as cron_router
from .auth.router import router as auth_router

app=FastAPI(title="CRON 2.0")
import asyncio
app.include_router(cron_router)
app.include_router(auth_router)
from .worker import Startcron
@app.on_event("startup")
async def start_running():
    task=BackgroundTasks()
    asyncio.create_task(Startcron())
