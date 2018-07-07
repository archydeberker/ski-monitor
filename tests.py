import darksky
import db_utils
import plotting
import scraping
from constants import url_dict, loc_dict
import app

import pandas as pd

mock_df = pd.DataFrame([[0, 1, 2, 'london', pd.to_datetime('01/01/1970')],
                        [0, 1, 2, 'paris', pd.to_datetime('02/01/1970')]],
                        columns=['A', 'B', 'C', 'location', 'time'])


def test_app_returns_200():

    content = app.display_content(0)

    assert content.status_code == 200

    content = app.display_content(1)

    assert content.status_code == 200


def test_scraping_returns_df():
    df = scraping.get_snow_depths(url_dict)

    assert isinstance(df, pd.DataFrame)


def test_darksky_class_returns_df():

    ds = darksky.DarkSky()
    df = ds.df_template()

    assert isinstance(df, pd.DataFrame)


def test_get_past_week_darksky_returns_df():

    ds = darksky.DarkSky()
    df = ds.get_past_week_darksky(loc_dict)

    assert isinstance(df, pd.DataFrame)


def test_get_next_week_darksky_returns_df():

    ds = darksky.DarkSky()
    df = ds.get_nextweek_darksky(loc_dict, daily=False)

    assert isinstance(df, pd.DataFrame)


def test_db_connection():

    db = db_utils.DatabaseConnection()


def test_plot_lines():

    pg = plotting.PostgresGrapher()

    plot = pg.plot_lines(mock_df, 'A', 'plot of A')


def test_plot_area():

    pg = plotting.PostgresGrapher()

    plot = pg.plot_area(mock_df, 'A', 'plot of A')


def test_plot_bar():

    plot = plotting.plot_bar(mock_df, ['A', 'B'], 'bar of A and B')

def test_hours_since_last_record():


