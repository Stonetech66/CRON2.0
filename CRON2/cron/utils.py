import pytz
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta




def next_execution(timezone:str, year:int | None, month:int| None, week:int | None, day:int, hours:int | None, minutes:int):

    if not day == 0:
         return datetime.now(tz=pytz.timezone(timezone)).replace(hour=hours, minute=minutes )+ relativedelta(day=day)
    
    elif not hours == 0:
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(hours=hours, minutes=minutes)
    
    elif minutes:
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(minutes=minutes)





   


