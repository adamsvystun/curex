from django.shortcuts import render
from django.http import HttpResponse
from app.services import get_rate

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def rates(request, cur_from="usd", cur_to="eur", date_from="1", date_to="2"):
    print(get_rate("usd","2012-01-01","2012-01-31"))
    return render(request, 'rates.html', {
        "cur_from": cur_from,
        "cur_to": cur_to,
        "date_from": date_from,
        "date_to": date_to
    })
