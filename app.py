import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import datetime

from dash.dependencies import Input, Output

from db_utils import connect_to_db, get_table
import darksky
import plotting


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
    'width': '95%',
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto'
})



header_div = html.H1(
        children='Welcome to Ski Monitor',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    )

darksky_div = html.Div(dcc.Markdown('[Powered by Dark Sky.](https://darksky.net/poweredby/)'),
                        style={'textAlign':'center'})

#columns=['location', 'time', 'summary', 'icon', 'precipIntensity', 'precipProbability', 'precipType', 'temperature', 'apparentTemperature', 'dewPoint', 'humidity', 'pressure', 'windSpeed', 'windGust', 'windBearing', 'cloudCover', 'uvIndex', 'visibility', 'ozone'])

conn = connect_to_db()

today = datetime.datetime.now().strftime('%Y-%m-%d')
earliest = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

df_historic = pd.read_sql("SELECT * from ds_current WHERE time > '%s'"%earliest, conn)
#darksky.get_past_week_darksky(darksky.loc_dict)
df_forecast = pd.read_sql("SELECT * from ds_forecasts WHERE time >= '%s'"%today, conn)
#darksky.get_nextweek_darksky(darksky.loc_dict)

pg = plotting.PostgresGrapher()
#graph_divs = html.Div([base_graph(1), base_graph(2), base_graph(3), base_graph(4)], style={'columnCount': 2})
@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    if value == 0:

        graph_divs = html.Div([pg.plot_lines(df_historic, 'temperature', 'Temperature (C)'),
                           pg.plot_lines(df_historic, 'windspeed', 'Windspeed (Mph)')],
                           style={'columnCount': 2})

        return html.Div([graph_divs, html.Div(pg.plot_area(df_historic, 'precipsigned', 'Snowfall plotted as positive values, rainfall as negative.',
                                                                                        'Precipitation (mm/hr)')),
                        darksky_div])
    else:

        graph_divs = html.Div([pg.plot_lines(df_forecast, 'temperature', 'Temperature (C)'),
                           pg.plot_lines(df_forecast, 'windspeed', 'Windspeed (Mph)')],
                           style={'columnCount': 2})

        return html.Div([graph_divs, html.Div(pg.plot_area(df_forecast, 'precipsigned' , 'Snowfall plotted as positive values, rainfall as negative.', 'Precipitation (mm/hr)')),
                        darksky_div])


if __name__ == '__main__':
    app.run_server()
