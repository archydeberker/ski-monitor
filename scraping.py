import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_snow_depths(url_dict):

    """ Returns a df with snow depth in cm.

    Relies upon data from onthesnow.com/ca.

    """

    snow_depth = {}
    for location in url_dict:

        snow_depth[location] = {}

        r = requests.get(url_dict[location])
        soup = BeautifulSoup(r.text, 'html.parser')

        for slope in ['upper', 'middle', 'lower']:
            try:
                list_item = soup.find('li', attrs={'class':'elevation %s' % slope})
                value = list_item.find('div', attrs={'class':"bluePill"}).contents[0]
                value = int(''.join(list(filter(str.isdigit, value))))
            except AttributeError:
                value = None

            if location == 'Jay Peak':
                value=int(value*2.54)

            snow_depth[location][slope] = value

    df_list = []

    for location in snow_depth:
        df_list.append(pd.DataFrame(snow_depth[location], index=[location]))

    df = pd.concat(df_list)
    df['location'] = df.index

    return df
