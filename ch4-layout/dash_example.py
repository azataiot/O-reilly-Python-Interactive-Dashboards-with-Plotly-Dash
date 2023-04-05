from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# import the data and read with pandas
df = pd.read_csv('world_happiness.csv')

# create a figure
figure = px.line(
    df[df['country'] == 'United States'],
    x='year', y='happiness_score',
    title="United States Happiness Score",
)

app = Dash(__name__)

app.layout = html.Div(children=[
    # title and data source
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
    dcc.RadioItems(
        options=df['region'].unique(),
        value='North America',
    ),
    dcc.Checklist(
        options=df['region'].unique(),
        value=['North America'],
    ),
    dcc.Dropdown(
        options=df['country'].unique(),
        value='United States',
    ),
    dcc.Graph(
        figure=figure,
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
