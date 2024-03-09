from time import sleep
import plotly.express as px
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

fig = initial_fig()

fig.show()

while True:
    for rabbit in rabbits:
        rabbit.move()

    fig.update_traces(lat=[rabbit.lat for rabbit in rabbits], lon=[rabbit.long for rabbit in rabbits])

    sleep(2)