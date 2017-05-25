# Curex

Currency exchange application in django.

## Running a project

Please, use Chrome.

### First way

Just go to this [link](http://curex.svit.net).

### Second way

Run it with Docker

```
docker run -d -p 8000:8000 adamsvystun/curex:latest
```
And then visit `localhost:8000`

### Third way

Direct instalation
Requirments:
* Python >=3.5

```
git clone https://github.com/adamsvystun/curex.git
pip3 install plotly
pip3 install django
cd curex
python3 manage.py migrate
python3 manage.py createcachetable
python3 manage.py runserver
```

(Checked on Linux Deepin 4.9.0-amd64)

## Caching system

There are two caches in this project:
1.First one is local memory cache for caching plots. Plots expire in 100 seconds.
2.Second one is database cache for caching api requests. It has expiration time set to forever (`None`).
