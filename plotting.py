import dash_core_components as dcc
import plotly.graph_objs as go


class PostgresGrapher:

    def __init__(self):
        pass

    def plot_lines(self, df, column, title, ytitle=None):
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
                    yaxis={'title': ytitle if ytitle else title},
                    margin={'l': 90, 'b': 90, 't': 90, 'r': 90},
                    legend={'x': 1, 'y': 1},
                    hovermode='closest',
                    title=title
                )
            }
        )

    def plot_area(self, df, column, title, ytitle=None, ylim=None):

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
                    yaxis={'title': ytitle if ytitle else title,
                           'range': ylim if ylim else 'auto'},
                    margin={'l': 90, 'b': 90, 't': 90, 'r': 50},
                    hovermode='closest',
                    title=title
                )
            },
        )

    def plot_opposed(self, df, column1, column2, title):
        """ Column1 will be plotted in positive, Column 2 in negative"""

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


def plot_bar(df, column_list, title, ytitle=None):
    """Plots bar chart, somewhat specificially for the current snow depths.
     Assumes that each column in `column_list` contains a single """

    return dcc.Graph(
            figure={'data': [
                go.Bar(
                    x=column_list,
                    y=df[df['location'] == i][column_list].as_matrix()[0],
                    text=df[df['location'] == i][column_list].as_matrix()[0],
                    opacity=0.5,
                    name=i
                ) for i in df['location'].unique()],
                'layout': go.Layout(
                    xaxis={'title': 'Region'},
                    yaxis={'title': ytitle if ytitle else title},
                    margin={'l': 90, 'b': 90, 't': 90, 'r': 90},
                    legend={'x': 1, 'y': 1},
                    hovermode='closest',
                    title=title,
            )
        },
        id='my-graph',
    )
