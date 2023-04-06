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

# create the radio buttons
radio = dcc.RadioItems(options={
    'happiness_score': 'Happiness Score',
    'happiness_rank': 'Happiness Rank',
}, value='happiness_score')

# create the figure
graph = dcc.Graph()

# create the div
average = html.Div(
    children=''
)

app.layout = html.Div([
    title,
    description,
    dropdown,
    radio,
    graph,
    average,
])


# create the callback
@app.callback(
    Output(graph, 'figure'),
    Output(average, 'children'),
    Input(dropdown, 'value'),
    Input(radio, 'value'),
)
def update_graph(country, metric):
    # filter the data
    country = country or 'United States'
    df_filtered = df[df['country'] == country]
    # create the figure
    fig = {
        'data': [
            {
                'x': df_filtered['year'],
                'y': df_filtered[metric],
                'type': 'line',
            },
        ],
        'layout': {
            'title': f'{metric} for {country}',
        },
    }
    # create the average
    avg = f'The average {metric} for {country} is {df_filtered[metric].mean():.2f}'
    return fig, avg


if __name__ == '__main__':
    app.run_server(debug=True)
