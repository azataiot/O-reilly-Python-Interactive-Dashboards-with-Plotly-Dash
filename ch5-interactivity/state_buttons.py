from dash import Dash, dcc, html, Input, Output, State
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

# create the region radio buttons
region_radio = dcc.RadioItems(
    options=df['region'].unique(),
    value='North America',
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

# create the update button
update_button = html.Button(
    n_clicks=0,
    children='Update',
)

# create the figure
graph = dcc.Graph()

# create the div
average = html.Div(
    children=''
)

app.layout = html.Div([
    title,
    description,
    region_radio,
    dropdown,
    radio,
    html.Br(),
    update_button,
    graph,
    average,
])


# create the callback for region selection
@app.callback(
    Output(dropdown, 'options'),
    Input(region_radio, 'value'),
)
def update_dropdown(region):
    return df[df['region'] == region]['country'].unique()


# create the callback
@app.callback(
    # the output is the figure and the average
    Output(graph, 'figure'),
    Output(average, 'children'),
    # the inputs
    Input(update_button, 'n_clicks'),
    # State changes based on the button click event.
    State(dropdown, 'value'),
    State(radio, 'value'),
)
def update_graph(btn_click, country, metric):
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
