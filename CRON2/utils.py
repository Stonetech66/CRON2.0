from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz

def find_next_execution(last_execution:datetime, timezone:str, year:int | None, month:int| None, week:int | None, day:int, hours:int | None, minutes:int):
    return last_execution.replace(tzinfo=pytz.timezone(timezone)) + relativedelta( years=year, months=month, weeks=week, day=day, hours=hours, minutes=minutes)
        

    # if day:
    #      return datetime.now(tz=pytz.timezone(timezone)).replace(hour=hours, minute=minutes )+ relativedelta(day=day)
    
    # elif hours:
    #     return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(hours=hours)
    
    # elif minutes:
    #     return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(minutes=minutes)
