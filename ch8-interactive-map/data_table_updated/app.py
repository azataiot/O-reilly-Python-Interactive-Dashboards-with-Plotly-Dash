from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv('../data/electricity.csv')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Data
year_min = df['Year'].min()
year_max = df['Year'].max()

# Components
title = html.H1('Electricity Consumption Dashboard')
# we define a range slider for the year, that ranges between the min and max, and only allows the integer values
range_slider = dcc.RangeSlider(
    min=year_min,
    max=year_max,
    step=1,  # we do not want people to select 1995.6
    value=[year_min, year_max],
    marks={
        i: str(i) for i in range(year_min, year_max + 1, 5)
    }
)
range_slider_result = html.Div()

# Map
map_graph = dcc.Graph()

# Temporary div
temp_div = html.Div()

# Table
table = dash_table.DataTable()

# Layout
app.layout = html.Div([
    title,
    range_slider,
    range_slider_result,
    map_graph,
    table,
], style={'padding': 100})


# callbacks
@app.callback(
    Output(range_slider_result, 'children'),
    Input(range_slider, 'value'),
)
def update_range_slider_result(value):
    return f"Selected range: {value}"


@app.callback(
    Output(map_graph, 'figure'),
    Input(range_slider, 'value'),
)
def update_map(value):
    filtered_df = df[(df['Year'] >= value[0]) & (df['Year'] <= value[1])]
    avg_price = filtered_df.groupby('US_State')['Residential Price'].mean().reset_index()
    map_fig = px.choropleth(
        data_frame=avg_price,
        locations='US_State',
        locationmode='USA-states',
        color='Residential Price',
        scope='usa',
        color_continuous_scale=px.colors.sequential.YlOrRd,
    )
    return map_fig


# map interactivity with table

@app.callback(
    Output(table, 'data'),
    Input(range_slider, 'value'),
    Input(map_graph, 'clickData'),
)
def update_table(value, clicked_data):
    filtered_df = df[(df['Year'] >= value[0]) & (df['Year'] <= value[1])]
    if clicked_data is None:
        return filtered_df.to_dict('records')
    else:
        state = clicked_data['points'][0]['location']
        table_df = filtered_df[filtered_df['US_State'] == state]
        return table_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
