from urllib.request import urlopen, URLError, HTTPError
import json
from django.core.cache import cache
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("app")

def get_rate(currency, start_date, end_date):
    url = 'http://api.nbp.pl/api/exchangerates/rates/A/'+currency
    cache_cur = cache.get(currency)
    rates = []
    if cache_cur:
        hit = True
        idate = start_date
        while idate <= end_date:
            if idate.isoformat() in cache_cur:
                rate = cache_cur[idate.isoformat()]
                if rate["rate"]:
                    rates.append(rate)
            else:
                hit = False
                break
            idate = idate + timedelta(days=1)
        if hit:
            logger.info("["+currency+"] Rates cache hit")
            return rates
        else:
            logger.info("["+currency+"] Hit for", str((idate-start_date).days))
            start_date = idate
    else:
        cache_cur = {}
    if start_date and end_date:
        url += '/'+start_date.isoformat()+'/'+end_date.isoformat()+'/'
    url += '?format=json'
    try:
        weburl = urlopen(url)
    except HTTPError as e:
        logger.warning('Error code: '+str(e.code)+", reason:"+e.reason)
        return rates
    except URLError as e:
        logger.error(e.reason)
        raise ValueError('Can not open api url')
    else:
        data = weburl.read()
        encoding = weburl.info().get_content_charset('utf-8')
        result = json.loads(data.decode(encoding))

        idate = start_date
        for index, val in enumerate(result["rates"]):
            cdate = datetime.strptime(val["effectiveDate"],'%Y-%m-%d').date()
            while cdate > idate:
                cache_cur[idate.isoformat()] = { "rate":False }
                idate = idate + timedelta(days=1)
            rate = {
                "rate": val["mid"],
                "date": cdate
            }
            cache_cur[idate.isoformat()] = rate
            idate = idate + timedelta(days=1)
            rates.append(rate)
        cache.set(currency, cache_cur, None)
        return rates

def get_table():
    url = 'http://api.nbp.pl/api/exchangerates/tables/a/'
    try:
        weburl = urlopen(url)
    except URLError as e:
        logger.error(e.reason)
        raise ValueError('Can not open api url')
    else:
        data = weburl.read()
        encoding = weburl.info().get_content_charset('utf-8')
        result = json.loads(data.decode(encoding))
        return result
