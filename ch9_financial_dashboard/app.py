from dash import Dash, html, dcc, dash_table
import plotly.graph_objects as go
import yfinance as yf

"""Application"""
app = Dash(__name__)

"""App Data"""
price = yf.Ticker('AAPL').history(period='1d', interval='15m').reset_index()
"""App Components"""
# Title
title = html.H1('Financial Dashboard', style={})

# Ticker Input
ticker_input = dcc.Input(
    placeholder='Search for a ticker symbol...',
    type='text',
    style={'width': '50%'},
)

# Submit Button
btn_submit = html.Button('Submit', style={})

# Candle Stick Chart
candle_stick_fig = go.Figure(
    data=go.Candlestick(
        x=price['Datetime'],
        open=price['Open'],
        high=price['High'],
        low=price['Low'],
        close=price['Close'],
    )
)
candle_stick = dcc.Graph(figure=candle_stick_fig)

# Data Table
table = dash_table.DataTable(
    data=price.tail(10).to_dict('records'),
)

"""Layout"""
app.layout = html.Div([
    title,
    ticker_input,
    btn_submit,
    html.Br(),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(label='Candle Stick', children=[candle_stick]),
        dcc.Tab(label='Table', children=[table]),
    ]),
], style={'padding': 20})

"""Run App"""
if __name__ == '__main__':
    app.run_server(debug=True)
