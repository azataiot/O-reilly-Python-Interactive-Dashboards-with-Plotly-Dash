from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv('../data/electricity.csv')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Data
year_min = df['Year'].min()
year_max = df['Year'].max()
avg_price = df.groupby('US_State')['Residential Price'].mean().reset_index()

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
map_fig = px.choropleth(
    avg_price,
    locations='US_State',
    locationmode='USA-states',
    color='Residential Price',
    scope='usa',
    color_continuous_scale=px.colors.sequential.YlOrRd,
)

# Table
table = dash_table.DataTable(
    data=df.to_dict('records'),
)

# Layout
app.layout = html.Div([
    title,
    range_slider,
    range_slider_result,
    dcc.Graph(figure=map_fig),
    table,
], style={'padding': 100})


# callbacks
@app.callback(
    Output(range_slider_result, 'children'),
    Input(range_slider, 'value'),
)
def update_range_slider_result(value):
    return f"Selected range: {value}"


if __name__ == '__main__':
    app.run_server(debug=True)
