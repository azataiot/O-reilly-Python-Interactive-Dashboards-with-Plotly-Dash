from dash import Dash, html, dcc
import pandas as pd
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='World Happiness Dashboard'),
    html.P([
        'This dashboard shows the happiness score of countries around the world.',
        html.Br(),
        html.A(
            'Data source',
            href='https://worldhappiness.report/',
            target='_blank'
        ),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
