from django.shortcuts import render
from django.http import HttpResponse
from datetime import date, timedelta, datetime
from django.core.cache import caches

from app.rates import get_exchange
from app.plot import get_plot

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def rates(request, show_plot=True, show_table=True):
    cur_from = request.GET.get("currency_from") or "usd"
    cur_to = request.GET.get("currency_to") or "eur"
    if cur_from == cur_to:
        return render(request, 'rates.html', {
            "cur_from": cur_from,
            "cur_to": cur_to,
            "get_request": request.get_full_path().rsplit('?', 1)[-1],
            "error": {
                "what": "Selected currencies are the same"
            }
        })
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if date_from:
        date_from = datetime.strptime(date_from,'%Y-%m-%d').date()
    else:
        date_from = date.today()-timedelta(days=7)
    if date_to:
        date_to = datetime.strptime(date_to,'%Y-%m-%d').date()
    else:
        date_to = date.today()
    exchange = None
    plot = None
    if show_plot:
        cache_key = cur_from+cur_to+date_from.isoformat()+date_to.isoformat()
        plot_cache = caches['plot']
        plot = plot_cache.get(cache_key)
        if plot:
            print("Plot cache hit")
        else:
            exchange = get_exchange(cur_from, cur_to, date_from, date_to)
            plot = get_plot(exchange, cache_key)
    if show_table and not exchange:
        exchange = get_exchange(cur_from, cur_to, date_from, date_to)
    return render(request, 'rates.html', {
        "exchange": exchange,
        "plot": plot,
        "cur_from": cur_from,
        "cur_to": cur_to,
        "date_from": date_from.isoformat(),
        "date_to": date_to.isoformat(),
        "get_request": request.get_full_path().rsplit('?', 1)[-1],
        "show_table": show_table,
    })
