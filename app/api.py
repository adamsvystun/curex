from urllib.request import urlopen, URLError, HTTPError
import json
from django.core.cache import cache
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("app")

def get_rate(currency, start_date, end_date):
    """
    Makes an API request and
    Returns exchange rates for currency relative to PLN in a certain date frame

    Keyword arguments:
    currency -- curreny code (ex: 'usd' )
    start_date -- date from which rates are taken (type: date)
    end_date -- date from which rates are taken (type: date)
    """
    url = 'http://api.nbp.pl/api/exchangerates/rates/A/'+currency
    cache_cur = cache.get(currency)
    rates = []
    # check if there is cache for given currency
    if cache_cur:
        hit = True
        idate = start_date
        # go from start date to end date
        while idate <= end_date:
            # check if current date is in cache
            if idate.isoformat() in cache_cur:
                rate = cache_cur[idate.isoformat()]
                if rate["rate"]:
                    rates.append(rate)
            # if current date is not in cache
            # and wy did not reach the end yet
            # then get out of the loop
            else:
                hit = False
                break
            idate = idate + timedelta(days=1)
        # if rates in whole date frame were in cache
        if hit:
            logger.info("["+currency+"] Rates cache hit")
            return rates
        else:
            logger.info("["+currency+"] Hit for", str((idate-start_date).days))
            # set start date to the first date which was not in cache
            start_date = idate
    else:
        cache_cur = {}
    if start_date and end_date:
        url += '/'+start_date.isoformat()+'/'+end_date.isoformat()+'/'
    url += '?format=json'
    try:
        logger.info("["+currency+"] Making a request")
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
            # because api does not return rates for each day
            # we need to fill those spaces with blanks
            # so later we now that we asked for those dates
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
    """
    Makes an API request and
    Returns latest exchange rates for all available currencies
    """
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
