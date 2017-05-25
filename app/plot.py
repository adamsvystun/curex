import plotly.offline as opy
import plotly.graph_objs as go
from django.core.cache import caches

def get_plot(exchange, cache_key):
    """
    Draws and returns a plot based on currency rates given
    """
    plot_cache = caches['plot']
    x = []
    y = []
    div = plot_cache.get(cache_key)
    for val in exchange:
        y.append(val["rate"])
        x.append(val["date"])
    trace1 = go.Scatter(x=x, y=y, marker={'color': '#33C3F0'})
    data=go.Data([trace1])
    layout=go.Layout()
    figure=go.Figure(data=data,layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div', show_link=False,
                    config={"displayModeBar": False})
    plot_cache.set(cache_key, div, 30)
    return div
