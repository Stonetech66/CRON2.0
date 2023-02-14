import pytz

def url_valid(url)-> bool:

    return url.startswith("https://") or url.startswith("http://")

def timezone_valid(timezone:str)->bool:
    try:
        pytz.timezone(timezone)
        return True
    except:
        return False