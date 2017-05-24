from datetime import datetime
from app.api import get_rate
# {'code': 'USD', 'currency': 'dolar amerykański', 'table': 'A', 'rates':
# [{'mid': 3.4454, 'no': '1/A/NBP/2012', 'effectiveDate': '2012-01-02'},
def get_exchange(cur_from, cur_to, date_from, date_to):
    exchange = []
    if cur_from == "pln" or cur_to == "pln":
        print("pln")
    else:
        rates_from = get_rate(cur_from, date_from, date_to)["rates"]
        rates_to = get_rate(cur_to, date_from, date_to)["rates"]
        for index, val in enumerate(rates_from):
            ex = {
                "rate": val["mid"]/rates_to[index]["mid"],
                "date": datetime.strptime(val["effectiveDate"],'%Y-%m-%d').date()
            }
            exchange.append(ex)
    return exchange
