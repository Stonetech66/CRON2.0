from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO, TU, TH, WE, FR, SA, SU
import pytz

def find_upper_execution(last_execution:datetime, timezone:str, year:int, month:int, weekday, day:int, hours:int, minutes:int):
    if not month == 0:
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(month=month, months=1, hour=hours, minute=minutes)
    elif weekday:
        return last_execution+relativedelta(weekday=eval(weekday)(1))
    elif not day == 0:
        return last_execution.replace(tzinfo=pytz.timezone(timezone)) + relativedelta( days=day)
    else:
        return last_execution.replace(tzinfo=pytz.timezone(timezone)) + relativedelta( hours=hours, minutes=minutes)


def error_code(status_code):
    if status_code > 400:
        return True
    return False
    
        

def next_execution(timezone:str, year:int , month:int, weekday, day:int, hours:int, minutes:int):

    if not month == 0:
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(month=month, months=1, hour=hours, minute=minutes)


    elif not weekday ==None:
        v=datetime.now(tz=pytz.timezone(timezone))+ relativedelta(weekday=eval(weekday)(1), hour=hours, minute=minutes, second=0, microsecond=0 )
        return v
    elif not day == 0:
        d=datetime.now(tz=pytz.timezone(timezone))
        if d + relativedelta(hour=hours, minute=minutes, second=0, microsecond=0) < d:
            return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(days=day, hour=hours, minute=minutes, second=0, microsecond=0)
        return d + relativedelta(hour=hours, minute=minutes, second=0, microsecond=0)
    
    elif not hours == 0:
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(hours=hours, minutes=minutes, second=0, microsecond=0)
    
    elif minutes:
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(minutes=minutes, second=0, microsecond=0)
