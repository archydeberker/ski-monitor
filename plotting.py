import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

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
        pass

    def plot_lines(self, df, column, title):
        df.sort_values(by='time', inplace=True)
        return dcc.Graph(
            id= column,
            figure={
                'data': [
                    go.Scatter(
                        x=df[df['location'] == i]['time'],
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

    def plot_area(self, df, column, title, ytitle=None):


        return dcc.Graph(
            id= column,
            figure={
                'data': [
                    go.Scatter(
                        x=df[df['location'] == i]['time'],
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
                    yaxis={'title': ytitle if ytitle else title},
                    margin={'l': 100, 'b': 100, 't': 100, 'r': 100},
                    legend={'x': 1, 'y': 1},
                    hovermode='closest',
                    title=title
                )
            }
        )

    def plot_opposed(self, table_name, column1, column2, title):
        ' Column1 will be plotted in positive, Column 2 in negative'


        return dcc.Graph(
            id= '-'.join((table_name, column1, column2)),
            figure={
                'data': [
                    go.Scatter(
                        x=df[df['location'] == i]['time'],
                        y=df[df['location'] == i][column1],
                        text=df[df['location'] == i][column1],
                        mode='none',
                        opacity=0.1,
                        fill='tozeroy',
                        name=i
                    ) for i in df['location'].unique()] +
                    [go.Scatter(
                        x=df[df['location'] == i]['time'],
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
