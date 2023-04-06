from dash import Dash, html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import yfinance as yf

"""Application"""
app = Dash(__name__)

"""App Data"""


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

# Error Message
error_msg = html.Div(children='', style={
    'paddingTop': 10,
    'color': 'red',
    'fontSize': 20,
})

# Candle Stick Chart

chart_graph = dcc.Graph()

# Data Table
table_header = html.Div(
    style={'fontSize': 20,
           'fontWeight': 'bold',
           'textAlign': 'center',
           'padding': 20,
           })
table = dash_table.DataTable()

# Interval Component
interval_chart = dcc.Interval(
    interval=1 * 1000 * 60 * 15,  # in milliseconds [1s * 60s * 15m = 15m]
    n_intervals=0,  # counter that shows how many times the interval has passed, we start at 0
)

interval_table = dcc.Interval(
    interval=1 * 1000 * 60,  # in milliseconds [1s * 60s = 1m]
    n_intervals=0,
)

"""Layout"""
app.layout = html.Div([
    title,
    ticker_input,
    btn_submit,
    error_msg,
    html.Br(),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(label='Candle Stick', children=[
            chart_graph
        ]),
        dcc.Tab(label='Recent Data', children=[
            table_header,
            html.Br(),
            table
        ]),
    ]),
    interval_chart,
    interval_table,
], style={'padding': 20})

"""App Callbacks"""


@app.callback(
    # update the candle stick chart
    Output(chart_graph, 'figure'),
    Output(error_msg, 'children'),
    # either button click or the interval triggers the update
    Input(btn_submit, 'n_clicks'),
    Input(interval_chart, 'n_intervals'),
    # get the ticker from the input (this needs to be triggered to being updated)
    State(ticker_input, 'value'),
)
def update_chart(btn, itv, ticker):
    """Update the chart"""
    if ticker is None:
        # default to AAPL
        ticker = 'AAPL'
    ticker_price = yf.Ticker(ticker).history(period='1d', interval='15m').reset_index()
    if len(ticker_price) > 0:
        fig = go.Figure(
            data=go.Candlestick(
                x=ticker_price['Datetime'],
                open=ticker_price['Open'],
                high=ticker_price['High'],
                low=ticker_price['Low'],
                close=ticker_price['Close'],
            )
        )

        return fig, ""
    else:
        return go.Figure(), "Ticker not found"


# update the table
@app.callback(
    Output(table_header, 'children'),
    Output(table, 'data'),
    Input(btn_submit, 'n_clicks'),
    Input(interval_table, 'n_intervals'),
    State(ticker_input, 'value'),
)
def update_table(btn_click, table_interval, ticker):
    """Update the table"""
    if ticker is None:
        # default to AAPL
        ticker = 'AAPL'
    ticker_price = yf.Ticker(ticker).history(period='1d', interval='1m').reset_index()
    if len(ticker_price) > 0:
        latest_price = ticker_price['Close'].iloc[-1]
        price_change = ticker_price['Close'].iloc[-1] - ticker_price['Close'].iloc[-2]
        candle_color = 'green' if price_change > 0 else 'red'
        latest_time = ticker_price['Datetime'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S %p')
        info = f'Latest Price of {ticker} : {latest_price} at {latest_time}'
        header_children = html.P(children=[
            "Last Price of ",
            html.Span(ticker, style={'color': 'blue'}),
            " : ",
            html.Span(latest_price, style={'color': f'{candle_color}'}),
            f' at {latest_time}'
        ])
        return header_children, ticker_price.tail(10).to_dict('records')
    else:
        return '', []


"""Run App"""
if __name__ == '__main__':
    app.run_server(debug=True)
