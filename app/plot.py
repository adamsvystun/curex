import plotly.offline as opy
import plotly.graph_objs as go

def get_plot(exchange):
    x = []
    y = []
    for val in exchange:
        y.append(val["rate"])
        x.append(val["date"])

    # trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': "10"},
    #                     mode="lines",  name='1st Trace')
    trace1 = go.Scatter(x=x, y=y, marker={'color': '#33C3F0'})
    data=go.Data([trace1])
    layout=go.Layout()
    figure=go.Figure(data=data,layout=layout)
    div = opy.plot(figure, auto_open=False, output_type='div', show_link=False, config={"displayModeBar":False})
    return div
