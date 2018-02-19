from urllib import parse

import pandas as pd
import psycopg2
import os
import json
import requests
import datetime

from psycopg2.extensions import AsIs
import darksky

def connect_to_db():

    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ.get("DATABASE_URL"))

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)

    return conn


def get_table(conn, table_name):

    df = pd.read_sql('SELECT * from %s;' % table_name, conn)

    return df

def get_current_weather(loc_dict):

    data_dict = {}
    for location in loc_dict.keys():

        r = requests.get('http://api.weatherunlocked.com/api/forecast/%1.2f,%1.2f?app_id=6765a93c&app_key=51b7b6cb5cf11b77b78d84d8f5c44845'%(loc_dict[location]))

        result = json.loads(r.text)

        data_dict[location] = {'Windspeed_Mph':result['Days'][0]['windspd_max_mph'],
                               'Rain_mm': result['Days'][0]['rain_total_mm'],
                               'Snow_mm': result['Days'][0]['snow_total_mm'],
                               'Temp_C_Max': result['Days'][0]['temp_max_c'],
                               'Temp_C_Min': result['Days'][0]['temp_min_c'],
                               'Timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                              }

    return data_dict

def get_forecast_weather(loc_dict):

    data_dict = {}

    for location in loc_dict.keys():

        r = requests.get('http://api.weatherunlocked.com/api/forecast/%1.2f,%1.2f?app_id=6765a93c&app_key=51b7b6cb5cf11b77b78d84d8f5c44845'%(loc_dict[location]))

        result = json.loads(r.text)
        tomorrow = result['Days'][1]['Timeframes']

        data_dict[location] ={}
        for i in range(8):
            timestamp = (datetime.datetime.strptime(result['Days'][1]['date'],'%d/%m/%Y')
                         +datetime.timedelta(hours=int(tomorrow[i]['time'])/100)).strftime('%Y-%m-%d %H:%M')
            data_dict[location][timestamp]= {'Windspeed_Mph':tomorrow[i]['windspd_mph'],
                                                       'Rain_mm': tomorrow[i]['rain_mm'],
                                                       'Snow_mm': tomorrow[i]['snow_mm'],
                                                       'Temp_C_Max': tomorrow[i]['temp_c'],
                                                       'Temp_C_Min': tomorrow[i]['temp_c'],

                              }


    return data_dict

def add_row(conn, data, table_name):

    columns = data.keys()
    values = [data[column] for column in columns]

    insert_statement = 'INSERT into ' + table_name + ' (%s) values %s'

    cursor=conn.cursor()
    try:
        cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
        conn.commit()
    except psycopg2.IntegrityError:
        print('Skipping value already in table')
        conn.rollback()


def add_forecasts(forecast_dict):

    for location in forecast_dict.keys():

        for timestamp in forecast_dict[location]:
            data = forecast_dict[location][timestamp]
            data['Timestamp'] = timestamp
            data['Location'] = location

            add_row(data, 'forecasts')

def add_current(current_dict):

    for location in forecast_dict.keys():

        data = current_dict[location]
        data['Location'] = location

        add_row(data, 'current')


def add_darksky(conn, df, table_name):
    """ Take a darksky dataframe and add it to the specified table."""

    data = df.to_dict(orient='records')

    for item in data:
        add_row(conn, item, table_name)

def drop_table(conn, table_name):
    """Use me with caution!"""
    cursor=conn.cursor()
    cursor.execute("DROP TABLE %s"%table_name)
    conn.commit()

def create_darksky_table(conn, table_name):
    """ All darksky tables have the same format.

    Note that location and precipSigned are added by us, not the API."""

    cursor=conn.cursor()
    cursor.execute("CREATE TABLE %s( \
                location TEXT, \
                time TIMESTAMP, \
                apparentTemperature REAL, \
                cloudCover TEXT, \
                dewPoint REAL, \
                humidity REAL, \
                icon TEXT, \
                ozone REAL, \
                precipAccumulation REAL, \
                precipIntensity REAL, \
                precipProbability REAL, \
                precipType TEXT, \
                pressure REAL, \
                summary TEXT, \
                temperature REAL, \
                uvIndex REAL, \
                visibility REAL, \
                windBearing REAL, \
                windGust REAL, \
                windSpeed REAL, \
                precipSigned REAL, \
                PRIMARY KEY(Location, time));"%table_name)

    conn.commit()

if __name__ == '__main__':

    loc_dict = {'Jay Peak':(44.9649,-72.4602),
            'Mt Sutton':(45.1047, -72.5618),
            'Mt Tremblant': (46.1185,-74.5962),
            'St Anne': (47.0754,-70.9049),
            'Le Massif': (47.2848,-70.5697),
           }

    conn = connect_to_db()

    current_df = darksky.get_past_week_darksky(loc_dict)
    add_darksky(conn, current_df, 'ds_current')

    forecast_df = darksky.get_nextweek_darksky(loc_dict)

    # We have to drop existing forecasts before adding new ones
    drop_table(conn, 'ds_forecasts')
    create_darksky_table(conn, 'ds_forecasts')
    add_darksky(conn, forecast_df, 'ds_forecasts')
