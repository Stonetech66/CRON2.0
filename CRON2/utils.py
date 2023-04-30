from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO, TU, TH, WE, FR, SA, SU
import pytz
from fastapi import HTTPException
def find_next_execution(timezone:str, year:int , month:int, weekday, day:int, hours:int, minutes:int):

    if not month == 0:
        
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(month=month, months=1, hour=hours, minute=minutes, second=0, microsecond=0)


    elif weekday:
        weekdays = {'MON': MO, 'TUE': TU, 'WED': WE, 'THU': TH, 'FRI': FR, 'SAT': SA, 'SUN': SU}
        dt_now = datetime.now(pytz.timezone(timezone))
        next_dt = dt_now + relativedelta(weekday=weekdays[weekday], hour=hours, minute=minutes, second=0, microsecond=0)
        if str(dt_now.strftime('%a')[:2]).upper() == weekday and next_dt <= dt_now:
            date=dt_now + relativedelta(weekday=weekdays[weekday](+1), days=+1, hour=hours, minute=minutes, second=0, microsecond=0)
        elif str(dt_now.strftime('%a')[:2]).upper() == weekday and next_dt > dt_now:
            date=dt_now + relativedelta(weekday=weekdays[weekday](+1), hour=hours, minute=minutes, second=0, microsecond=0)
        else:
            date=dt_now + relativedelta(weekday=weekdays[weekday](+1), hour=hours, minute=minutes, second=0, microsecond=0) 
            
       
        return date
    elif  day:
        d=datetime.now(tz=pytz.timezone(timezone))
        if d + relativedelta(hour=hours, minute=minutes, second=0, microsecond=0) < d:
            return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(days=day, hour=hours, minute=minutes, second=0, microsecond=0)
        return d + relativedelta(hour=hours, minute=minutes, second=0, microsecond=0)
    
    elif hours:
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(hours=hours, minute=minutes, second=0, microsecond=0)
    
    elif minutes:
        if minutes < 1:
            raise HTTPException(detail="invalid schedule time provided you are to enter a minute greater than 0", status_code=400)
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(minutes=minutes, second=0, microsecond=0)

def error_code(status_code):
    if status_code > 400:
        return True
    return False
    
        

def next_execution(timezone:str, year:int , month:int, weekday, day:int, hours:int, minutes:int):

    if not month == 0:
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(month=month, months=1, hour=hours, minute=minutes)


    elif weekday:
        weekdays = {'MON': MO, 'TUE': TU, 'WED': WE, 'THU': TH, 'FRI': FR, 'SAT': SA, 'SUN': SU}
        dt_now = datetime.now(pytz.timezone(timezone))
        next_dt = dt_now + relativedelta(weekday=weekdays[weekday](+1), days=+1, hour=hours, minute=minutes, second=0, microsecond=0)
         
        return next_dt
    elif day:
        d=datetime.now(tz=pytz.timezone(timezone))
        if d + relativedelta(hour=hours, minute=minutes, second=0, microsecond=0) < d:
            return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(days=day, hour=hours, minute=minutes, second=0, microsecond=0)
        return d + relativedelta(hour=hours, minute=minutes, second=0, microsecond=0)
    
    elif hours:
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(hours=hours, minutes=minutes, second=0, microsecond=0)
    
    elif minutes:
        if minutes < 1:
                        raise HTTPException(detail="invalid schedule time provided you are to enter a minute greater than 0", status_code=400)
        return datetime.now(tz=pytz.timezone(timezone))+ relativedelta(minutes=minutes, second=0, microsecond=0)
