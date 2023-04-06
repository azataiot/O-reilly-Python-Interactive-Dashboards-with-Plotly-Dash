from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

df = pd.read_csv('fifa_soccer_players.csv')

title = html.H1('FIFA Soccer Players Dashboard')

data_source = html.P(
    [
        'Data source: ',
        html.A('Sofifa', href='https://sofifa.com/', target='_blank')
    ]
)

name_label = html.Label('Player Name')
name_dropdown = dcc.Dropdown(
    options=df['long_name'].sort_values().unique(),
    value=df['long_name'][0],
)

app.layout = html.Div(
    children=[
        title,
        data_source,
        name_label,
        name_dropdown,
    ],
    style={
        # give some padding to the left and right
        'padding': 100,
        # make the border solid
        'border': 'solid',

    }
)

if __name__ == '__main__':
    app.run_server(debug=True)
