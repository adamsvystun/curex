from urllib.request import urlopen, URLError
import json

def get_rate(currency, start_date, end_date):
    url = 'http://api.nbp.pl/api/exchangerates/rates/A/'+currency
    if start_date and end_date:
        url += '/'+start_date+'/'+end_date+'/'
    url += '?format=json'
    try:
        weburl = urlopen(url)
    except URLError as e:
        print(e.reason)
        return False
    else:
        data = weburl.read()
        encoding = weburl.info().get_content_charset('utf-8')
        result = json.loads(data.decode(encoding))
        return result

def get_table():
    url = 'http://api.nbp.pl/api/exchangerates/tables/a/'
    try:
        weburl = urlopen(url)
    except URLError as e:
        print(e.reason)
        return False
    else:
        data = weburl.read()
        encoding = weburl.info().get_content_charset('utf-8')
        result = json.loads(data.decode(encoding))
        return result
