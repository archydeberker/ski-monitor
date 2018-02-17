import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

from db_utils import connect_to_db, get_table

app = dash.Dash()
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

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


def postgres_graph(table_name):

    conn = connect_to_db()
    df = get_table(conn, table_name)

    return dcc.Graph(
        id= table_name,
        figure={
            'data': [
                go.Scatter(
                    x=df[df['resort'] == i]['time'],
                    y=df[df['resort'] == i]['measurement'],
                    text=df[df['resort'] == i]['measurement'],
                    mode='line',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df['resort'].unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Temperature'},
                margin={'l': 100, 'b': 100, 't': 100, 'r': 100},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                title='Temperature graph'
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

#graph_divs = html.Div([base_graph(1), base_graph(2), base_graph(3), base_graph(4)], style={'columnCount': 2})
graph_divs = html.Div([postgres_graph('temperatures')])

app.layout = html.Div([header_div, graph_divs])

if __name__ == '__main__':
    app.run_server()