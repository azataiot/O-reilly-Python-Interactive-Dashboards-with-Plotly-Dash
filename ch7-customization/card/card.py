from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv('../data/fifa_soccer_players.csv')

# statistics
avg_age = df['age'].mean()
avg_height = df['height_cm'].mean()
avg_weight = df['weight_kg'].mean()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    brand='FIFA Soccer Players Dashboard',
    children=[
        html.Img(
            src="https://upload.wikimedia.org/wikipedia/en/thumb/6/67/2018_FIFA_World_Cup.svg/1200px-2018_FIFA_World_Cup.svg.png",
            height=20,
        ),
        html.A(
            "Data Source",
            href="https://sofifa.com/",
            target="_blank",
            style={
                'color': 'white',
            }
        ),
    ],
    color='primary',
    dark=True,
    fluid=True,
)


#  DRY - Don't Repeat Yourself Card Component
def get_card(title, value, color):
    return dbc.Card(
        [
            html.H4(title),
            html.H5(value),
        ],
        body=True,
        style={
            "textAlign": "center",
            "color": "white",
        },
        color=color,
    )


cards = dbc.Row([
    dbc.Col(
        dbc.Card(
            [
                html.H4("Average Age"),
                html.H5(f'{avg_age:.2f} years'),
            ],
            body=True,
            style={
                "textAlign": "center",
                "color": "white",
            },
            color='lightblue',
        )
    ),
    dbc.Col(get_card('Average Height', f'{avg_height:.2f} cm', 'lightgreen')),
    dbc.Col(get_card('Average Weight', f'{avg_weight:.2f} kg', 'lightpink')),
], style={'margin': 10})

app.layout = html.Div(
    [
        navbar,
        html.Br(),
        cards,
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
