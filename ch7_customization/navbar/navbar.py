from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

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

app.layout = html.Div(
    [
        navbar,
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
