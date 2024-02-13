# Import libraries
from dash import Dash, html, dcc, Input, Output
from dash import dash_table
import pandas as pd
import plotly.express as px
from collections import OrderedDict

data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)

df = pd.DataFrame(data)

df['id'] = df.index

# Load the dataset
avocado = pd.read_csv('avocado-updated-2020.csv')

# Create the Dash app
# app = Dash()

app = Dash(__name__)
server = app.server
# df['id'] = df.index

# Set up the app layout
geo_dropdown = dcc.Dropdown(options=avocado['geography'].unique(),
                            value='New York')

app.layout = html.Div(children=[
    html.H1(children='Avocado Prices Dashboard'),
    geo_dropdown,
    dcc.Graph(id='price-graph'),
    dash_table.DataTable(
    data=df.to_dict('records'),
    sort_action='native',
    columns=[
        {'name': 'Date', 'id': 'Date', 'type': 'datetime', 'editable': False},
        {'name': 'Delivery', 'id': 'Delivery', 'type': 'datetime'},
        {'name': 'Region', 'id': 'Region', 'type': 'text'},
        {'name': 'Temperature', 'id': 'Temperature', 'type': 'numeric'},
        {'name': 'Humidity', 'id': 'Humidity', 'type': 'numeric'},
        {'name': 'Pressure', 'id': 'Pressure', 'type': 'any'},
    ],
    editable=True,
    style_data_conditional=[
        {
            'if': {
                'column_id': 'Region',
            },
            'backgroundColor': 'dodgerblue',
            'color': 'white'
        },
{
            'if': {
                'state': 'active'  # 'active' | 'selected'
            },
           'backgroundColor': 'rgba(0, 116, 217, 0.3)',
           'border': '1px solid rgb(0, 116, 217)'
        }

    ]
)
])


# Set up the callback function
@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id=geo_dropdown, component_property='value')
)
def update_graph(selected_geography):
    filtered_avocado = avocado[avocado['geography'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                       x='date', y='average_price',
                       color='type',
                       title=f'Avocado Prices in {selected_geography}')
    return line_fig


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)
    #
    # if __name__ == '__main__':
    #     app.run(debug=True)

#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