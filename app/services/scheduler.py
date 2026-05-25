from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Callable, Any

scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")

def start_scheduler():
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()

def add_cron_job(func: Callable, hour: int = None, minute: int = None, second: int = None, **kwargs):
    trigger = CronTrigger(hour=hour, minute=minute, second=second)
    scheduler.add_job(func, trigger, **kwargs)

def add_interval_job(func: Callable, minutes: int = 5, **kwargs):
    scheduler.add_job(func, 'interval', minutes=minutes, **kwargs)
