import pandas as pd
import datetime
import requests
import os
import numpy as np

loc_dict = {'Jay Peak':(44.9649,-72.4602),
            'Mt Sutton':(45.1047, -72.5618),
            'Mt Tremblant': (46.1185,-74.5962),
            'St Anne': (47.0754,-70.9049),
            'Le Massif': (47.2848,-70.5697),
           }

KEY = os.environ['DARKSKY_KEY']

def df_template():

    return pd.DataFrame(
        columns=['location', 'time', 'summary', 'icon', 'precipIntensity', 'precipProbability', 'precipType',
                 'temperature', 'apparentTemperature', 'dewPoint', 'humidity', 'pressure', 'windSpeed', 'windGust',
                 'windBearing', 'cloudCover', 'uvIndex', 'visibility', 'ozone'])

def post_process(df):

    df['time'] = df['time'].apply(lambda x: datetime.datetime.fromtimestamp(x))

    df.sort_values(by='time', inplace=True)

    p_type = np.array([int(i) for i in (df['precipType']=='rain').tolist()])

    df['precipSigned'] = df['precipIntensity'] * (1- 2*p_type)
    return df


def get_past_week_darksky(loc_dict):
    """ Fetch hourly details for every day in the last week.
    """

    now = datetime.datetime.date(datetime.datetime.now())
    df = df_template()
    dates = [now - datetime.timedelta(days=i) for i in range(7)]

    timestamps = [datetime.datetime.combine(d, datetime.time()).timestamp() for d in dates]

    for loc in loc_dict.keys():
        lon = loc_dict[loc][0]
        lat = loc_dict[loc][1]
        for t in timestamps:
            r = requests.get(
                'https://api.darksky.net/forecast/%s/%1.4f,%1.4f,%d' % (KEY, lon, lat, t),
                params={'units': 'si'})

            for h in r.json()['hourly']['data']:
                h['location'] = loc
                df = df.append(h, ignore_index=True)



    return post_process(df)


def get_nextweek_darksky(loc_dict):
    """ From the DarkSky docs:
    A Forecast Request returns the current weather conditions,
    a minute-by-minute forecast for the next hour (where available),
    an hour-by-hour forecast for the next 48 hours, and a day-by-day forecast for the next week.
    """

    df = df_template()

    for loc in loc_dict.keys():
        lon = loc_dict[loc][0]
        lat = loc_dict[loc][1]

        r = requests.get('https://api.darksky.net/forecast/%s/%1.4f,%1.4f' % (KEY, lon, lat),
                         params={'units': 'si'})

        dict_list = []

        c = r.json()['currently']

        c['location'] = loc

        df = df.append(c, ignore_index=True)

        for h in r.json()['hourly']['data']:
            h['location'] = loc
            df = df.append(h, ignore_index=True)

        for d in r.json()['daily']['data']:
            h['location'] = loc
            df = df.append(h, ignore_index=True)


    return post_process(df)
