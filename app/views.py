from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date, timedelta, datetime
from django.core.cache import caches
import logging

from app.rates import get_exchange, get_currencies
from app.plot import get_plot

logger = logging.getLogger("app")

def rates(request, show_plot=True, show_table=True):
    """Renders an exchange currency view"""
    # parametrs from get
    cur_from = request.GET.get("currency_from") or "usd"
    cur_to = request.GET.get("currency_to") or "pln"
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    exchange = None; plot = None; error = None
    # parsing dates to datetime.date objects
    if date_from:
        try:
            date_from = datetime.strptime(date_from,'%Y-%m-%d').date()
        except ValueError:
            date_from = date.today()-timedelta(days=7)
            error = "Not correct date format. Use isoformat YYYY-mm-dd."
    else:
        date_from = date.today()-timedelta(days=7)
    if date_to:
        try:
            date_to = datetime.strptime(date_to,'%Y-%m-%d').date()
        except ValueError:
            date_to = date.today()
            error = "Not correct date format. Use isoformat YYYY-mm-dd."
    else:
        date_to = date.today()
    # getting currency list
    try:
        currency_list = get_currencies()
    except ValueError as e:
        error = str(e)
    # checks for forbidden inputs
    if date_from > date_to:
        error = "Date from is greater than date to"
    elif date_to > date.today():
        error = "You cannot get exchange rates for the future"
    elif cur_from == cur_to:
        error = "Selected currencies are the same"
    else:
        cache_key = cur_from+cur_to+date_from.isoformat()+date_to.isoformat()
        if show_table:
            try:
                exchange = get_exchange(cur_from, cur_to, date_from, date_to)
            except ValueError as e:
                error = str(e)
        if show_plot:
            plot_cache = caches['plot']
            plot = plot_cache.get(cache_key)
            # check if plot is cache
            if not plot:
                # check if exchange rates have already been calculated
                if exchange:
                    plot = get_plot(exchange, cache_key)
                else:
                    try:
                        exchange = get_exchange(cur_from, cur_to,
                                                date_from, date_to)
                        if len(exchange):
                            plot = get_plot(exchange, cache_key)
                    except ValueError as e:
                        error = str(e)
    return render(request, 'rates.html', {
        "exchange": exchange,
        "plot": plot,
        "cur_from": cur_from,
        "cur_to": cur_to,
        "date_from": date_from.isoformat(),
        "date_to": date_to.isoformat(),
        "get_request": request.get_full_path().rsplit('?', 1)[-1],
        "show_table": show_table,
        "currency_list": currency_list,
        "error": error
    })

def cache_clear(request):
    """Clears cache and redirects back to referer"""
    caches["plot"].clear()
    caches["default"].clear()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
