from dash import Dash, html, dcc, Input, Output
import pandas as pd

df = pd.read_csv('../data/electricity.csv')

app = Dash(__name__)

# data
year_min = df['Year'].min()
year_max = df['Year'].max()

# layouts
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

app.layout = html.Div([
    title,
    range_slider,
    range_slider_result,
])


# callbacks
@app.callback(
    Output(range_slider_result, 'children'),
    Input(range_slider, 'value'),
)
def update_range_slider_result(value):
    return f"Selected range: {value}"


if __name__ == '__main__':
    app.run_server(debug=True)
