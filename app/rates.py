from datetime import datetime
from app.api import get_rate

# {'code': 'USD', 'currency': 'dolar amerykański', 'table': 'A', 'rates':
# [{'mid': 3.4454, 'no': '1/A/NBP/2012', 'effectiveDate': '2012-01-02'},
def get_exchange(cur_from, cur_to, date_from, date_to):
    exchange = []
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
