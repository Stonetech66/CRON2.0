from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO, TU, TH, WE, FR, SA, SU
import pytz

def find_next_execution(last_execution:datetime, timezone:str, year:int, month:int, weekday, day:int, hours:int, minutes:int):
    if not month == 0:
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(month=month, months=1, hour=hours, minute=minutes)
    elif weekday:
        return last_execution+relativedelta(weekday=eval(weekday)(1))
    elif not day == 0:
        return last_execution.replace(tzinfo=pytz.timezone(timezone)) + relativedelta( days=day)
    else:
        return last_execution.replace(tzinfo=pytz.timezone(timezone)) + relativedelta( hours=hours, minutes=minutes)


    
        

    # if day:
    #      return datetime.now(tz=pytz.timezone(timezone)).replace(hour=hours, minute=minutes )+ relativedelta(day=day)
    
    # elif hours:
    #     return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(hours=hours)
    
    # elif minutes:
    #     return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(minutes=minutes)
