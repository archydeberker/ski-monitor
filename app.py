import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from db_utils import connect_to_db, get_table

app = dash.Dash()
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    dcc.Tabs(
        tabs=[
            {'label': 'Historic Data', 'value': 0},
            {'label': 'Forecast Data', 'value': 1},
        ],
        value=0,
        id='tabs'
    ),
    html.Div(id='tab-output')
], style={
    'width': '80%',
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto'
})

def base_graph(i):

    return dcc.Graph(
        id='life-exp-vs-gdp-%d'%i,
        figure={
            'data': [
                go.Scatter(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='line',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in ['Asia', 'Europe']
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l':100, 'b': 100, 't': 100, 'r': 100},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                title='Blablabla'
            )
        }
    )


class PostgresGrapher():

    def __init__(self):
        self.conn = connect_to_db()

    def plot_lines(self, table_name, column, title):

        df = get_table(self.conn, table_name).sort_values(by='timestamp')

        return dcc.Graph(
            id= '-'.join((table_name, column)),
            figure={
                'data': [
                    go.Scatter(
                        x=df[df['location'] == i]['timestamp'],
                        y=df[df['location'] == i][column],
                        text=df[df['location'] == i][column],
                        mode='line',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df['location'].unique()
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Date'},
                    yaxis={'title': title},
                    margin={'l': 100, 'b': 100, 't': 100, 'r': 100},
                    legend={'x': 1, 'y': 1},
                    hovermode='closest',
                    title=title
                )
            }
        )

    def plot_area(self, table_name, column, title):

        df = get_table(self.conn, table_name).sort_values(by='timestamp')

        return dcc.Graph(
            id= '-'.join((table_name, column)),
            figure={
                'data': [
                    go.Scatter(
                        x=df[df['location'] == i]['timestamp'],
                        y=df[df['location'] == i][column],
                        text=df[df['location'] == i][column],
                        mode='none',
                        opacity=0.1,
                        fill='tozeroy',
                        name=i
                    ) for i in df['location'].unique()
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Date'},
                    yaxis={'title': title},
                    margin={'l': 100, 'b': 100, 't': 100, 'r': 100},
                    legend={'x': 1, 'y': 1},
                    hovermode='closest',
                    title=title
                )
            }
        )

    def plot_opposed(self, table_name, column1, column2, title):
        ' Column1 will be plotted in positive, Column 2 in negative'

        df = get_table(self.conn, table_name)

        return dcc.Graph(
            id= '-'.join((table_name, column1, column2)),
            figure={
                'data': [
                    go.Scatter(
                        x=df[df['location'] == i]['timestamp'],
                        y=df[df['location'] == i][column1],
                        text=df[df['location'] == i][column1],
                        mode='none',
                        opacity=0.1,
                        fill='tozeroy',
                        name=i
                    ) for i in df['location'].unique()] +
                    [go.Scatter(
                        x=df[df['location'] == i]['timestamp'],
                        y=-df[df['location'] == i][column2],
                        text=df[df['location'] == i][column2],
                        mode='none',
                        opacity=0.1,
                        fill='tonexty',
                        name=i
                    ) for i in df['location'].unique()],
                'layout': go.Layout(
                    xaxis={'title': 'Date'},
                    yaxis={'title': title},
                    margin={'l': 100, 'b': 100, 't': 100, 'r': 100},
                    legend={'x': 1, 'y': 1},
                    hovermode='closest',
                    title=title
                )
            }
        )

header_div = html.H1(
        children='Welcome to Ski Monitor',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    )

explainer_div = html.P(children='Snowfall plotted as positive values, rainfall as negative.',
                       style={
                           'textAlign': 'center',
                       })



pg = PostgresGrapher()
#graph_divs = html.Div([base_graph(1), base_graph(2), base_graph(3), base_graph(4)], style={'columnCount': 2})
@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    if value==0:
        graph_divs = html.Div([pg.plot_lines('current', 'temp_c_max', 'Max Temperature (C)'),
                           pg.plot_lines('current', 'windspeed_mph', 'Windspeed (Mph)')],
                           style={'columnCount': 2})

        return html.Div([graph_divs, html.Div(pg.plot_opposed('current', 'snow_mm', 'rain_mm', 'Snowfall plotted as positive values, rainfall as negative.'))])
    else:
        graph_divs = html.Div([pg.plot_lines('forecasts', 'temp_c_max', 'Max Temperature (C)'),
                           pg.plot_lines('forecasts', 'windspeed_mph', 'Windspeed (Mph)')],
                           style={'columnCount': 2})

        return html.Div([graph_divs, html.Div(pg.plot_opposed('forecasts', 'snow_mm', 'rain_mm', '+ Snow (mm), - Rain(mm)'))])


if __name__ == '__main__':
    app.run_server()
