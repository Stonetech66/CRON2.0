from fastapi import FastAPI, BackgroundTasks
from .cron.routers import router as cron_router
from .auth.router import router as auth_router

app=FastAPI(title="CRON 2.0", prefix="/api", description="CRON2.0 is a system built to automate scheduling of CronJobs")
import asyncio
app.include_router(cron_router)
app.include_router(auth_router)



