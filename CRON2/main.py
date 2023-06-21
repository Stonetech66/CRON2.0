from fastapi import FastAPI, BackgroundTasks
from .cron.routers import router as cron_router
from .auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="CRON 2.0", description="CRON2.0 is a system built to automate scheduling of CronJobs")
import asyncio
app.include_router(cron_router)
app.include_router(auth_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*']      
    )
