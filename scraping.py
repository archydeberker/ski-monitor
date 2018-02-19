import requests
from bs4 import BeautifulSoup
import pandas as pd

loc_dict = {'Jay Peak':'https://www.onthesnow.com/vermont/jay-peak/skireport.html',
            'Mt Sutton':'https://www.onthesnow.ca/quebec/mont-sutton/skireport.html',
            'Mt Tremblant': 'https://www.onthesnow.ca/quebec/tremblant/skireport.html',
            'St Anne': 'https://www.onthesnow.ca/quebec/mont-sainte-anne/skireport.html',
            'Le Massif': 'https://www.onthesnow.ca/quebec/le-massif/skireport.html',
           }

def get_snow_depths(loc_dict):
    """ Returns a df with snowd depth in cm"""

    snow_depth = {}
    for location in loc_dict:

        snow_depth[location] = {}

        r = requests.get(loc_dict[location])
        soup = BeautifulSoup(r.text, 'html.parser')

        for slope in ['upper', 'middle', 'lower']:
            list_item = soup.find('li', attrs={'class':'elevation %s' % slope})
            value = list_item.find('div', attrs={'class':"bluePill"}).contents[0]
            value = int(''.join(list(filter(str.isdigit, value))))

            if location == 'Jay Peak':
                value=int(value*2.54)

            snow_depth[location][slope] = value

    df_list = []

    for location in snow_depth:
        df_list.append(pd.DataFrame(snow_depth[location], index=[location]))

    df = pd.concat(df_list)
    df['location'] = df.index

    return df
