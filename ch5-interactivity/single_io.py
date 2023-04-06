from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

input_text = dcc.Input(value='Type here', type='text')
output_text = html.Div()

app.layout = html.Div([
    input_text,
    output_text
])


@app.callback(
    Output(output_text, 'children'),
    Input(input_text, 'value')
)
def update_output(value):
    return value


if __name__ == '__main__':
    app.run_server(debug=True)
