from dash import Dash, dcc, html, Input, Output
import pandas as pd

# import the data from the csv file
df = pd.read_csv('world_happiness.csv')

app = Dash(__name__)

title = html.H1('World Happiness Dashboard')
description = html.P(
    [
        'This dashboard shows the happiness score for different countries',
        html.Br(),
        html.A('Data source', href='https://worldhappiness.report/'),
    ]
)

# create the dropdown
dropdown = dcc.Dropdown(
    options=df['country'].unique(),
)

# create the figure
graph = dcc.Graph()

app.layout = html.Div([
    title,
    description,
    dropdown,
    graph,
])


# create the callback
@app.callback(
    Output(graph, 'figure'),
    Input(dropdown, 'value'),
)
def update_graph(country):
    # filter the data
    country = country or 'United States'
    df_filtered = df[df['country'] == country]
    # create the figure
    fig = {
        'data': [
            {
                'x': df_filtered['year'],
                'y': df_filtered['happiness_score'],
                'type': 'line',
            },
        ],
        'layout': {
            'title': f'Happiness score for {country}',
        },
    }
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
