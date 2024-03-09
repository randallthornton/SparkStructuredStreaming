import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import random

class Rabbit: 
    id: int
    lat: float
    long: float
    color: str

    def __init__(self, id, lat, long, color) -> None:
        self.id = id
        self.lat = lat
        self.long = long
        self.color = color

    def to_dict(self):
        return {
            "lat": self.lat,
            "long": self.long,
            "color": self.color,
            "id": self.id
        }
    
    def move(self):
        self.lat = self.lat + (random.random() - .5) * .03
        self.long = self.long + (random.random() - .5) * .03

def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'rgb({r},{g},{b})'

def initial_fig():
    df = pd.DataFrame([rabbit.to_dict() for rabbit in rabbits])
    fig = px.scatter_geo(df, lat='lat', lon='long', color='color', text='id')
    
    return fig

numRabbits = 20
rabbits = []

for i in range(20):
    lat = 28.4386529
    long = -81.2169541
    rabbits.append(Rabbit( i, lat, long, get_random_color() ))

# Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div(
    children=[
        dcc.Graph(id='live-graph', animate=True, style={"height": "80vh"}, figure = initial_fig()),
        dcc.Interval(
            id='graph-update',
            interval=3*1000,  # in milliseconds
            n_intervals=0
        ),
    ]
)

@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    print("Updating graph...")
    for rabbit in rabbits:
        rabbit.move()
    df = pd.DataFrame([rabbit.to_dict() for rabbit in rabbits])
    fig = px.scatter_geo(df, lat='lat', lon='long', color='color', text='id')
    fig.update_traces()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

