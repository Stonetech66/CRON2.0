import pytz


def timezone_valid(timezone:str)->bool:
    try:
        pytz.timezone(timezone)
        return True
    except:
        return False