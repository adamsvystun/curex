from datetime import datetime
from app.api import get_rate, get_table
from django.core.cache import cache

# {'code': 'USD', 'currency': 'dolar amerykański', 'table': 'A', 'rates':
# [{'mid': 3.4454, 'no': '1/A/NBP/2012', 'effectiveDate': '2012-01-02'},
def get_exchange(cur_from, cur_to, date_from, date_to):
    """
    Calculates exchange rates for two currencies
    in a certain date frame
    """
    exchange = []
    # check if one of the currencies is 'pln'
    if cur_from == "pln":
        rates_to = get_rate(cur_to, date_from, date_to)
        for index, val in enumerate(rates_to):
            ex = {
                "rate": 1/val["rate"],
                "date": val["date"]
            }
            exchange.append(ex)
    elif cur_to == "pln":
        rates_from = get_rate(cur_from, date_from, date_to)
        for index, val in enumerate(rates_from):
            ex = {
                "rate": val["rate"],
                "date": val["date"]
            }
            exchange.append(ex)
    else:
        rates_from = get_rate(cur_from, date_from, date_to)
        rates_to = get_rate(cur_to, date_from, date_to)
        for index, val in enumerate(rates_from):
            ex = {
                "rate": val["rate"]/rates_to[index]["rate"],
                "date": val["date"]
            }
            exchange.append(ex)
    return exchange

def get_currencies():
    """
    Returns a list of all available currencies
    """
    currency_list = cache.get("currency_list")
    # check if in cache
    if currency_list:
        return currency_list
    else:
        table = get_table()
        currency_list = table[0]["rates"]
        currency_list.append({"code": "pln"})
        cache.set("currency_list", currency_list, None)
        return currency_list
