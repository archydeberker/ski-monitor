from urllib import parse

import pandas as pd
import psycopg2
import os
import datetime

from psycopg2.extensions import AsIs

import darksky
from constants import loc_dict


class DatabaseConnection:

    def __init__(self):
        self.conn = self.connect_to_db()

    def connect_to_db(self):

        """
        You need to have the variable DATABASE_URL in your environment.
        This is automatically set in your Heroku app.

        """

        parse.uses_netloc.append("postgres")
        url = parse.urlparse(os.environ.get("DATABASE_URL"))

        return psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port)

    def get_table(self, table_name):

        """ Returns all the entries in the specified table.

        """

        df = pd.read_sql('SELECT * from %s;' % table_name, self.conn)

        return df

    def add_row(self, data, table_name):

        """Add a row to table_name.

        `Data` must be a dictionary, where the keys match the columns in
        `table_name`.

        """

        columns = data.keys()
        values = [data[column] for column in columns]

        insert_statement = 'INSERT into ' + table_name + ' (%s) values %s'

        cursor = self.conn.cursor()
        try:
            cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
            self.conn.commit()
        except psycopg2.IntegrityError:
            print('Skipping value already in table')
            self.conn.rollback()

    def add_forecasts(self, forecast_dict):

        for location in forecast_dict.keys():

            for timestamp in forecast_dict[location]:
                data = forecast_dict[location][timestamp]
                data['Timestamp'] = timestamp
                data['Location'] = location

                self.add_row(data, 'forecasts')

    def add_darksky(self, df, table_name):
        """ Take a darksky dataframe and add it to the specified table."""

        data = df.to_dict(orient='records')

        for item in data:
            self.add_row(item, table_name)

    def drop_table(self, table_name):
        """Use me with caution!"""

        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE %s" % table_name)
        self.conn.commit()

    def delete_old_rows(self, table_name, interval='1 month'):

        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM %s WHERE CURRENT_TIMESTAMP - time > %s::interval" % (table_name,
                                                                                         interval))
        self.conn.commit()

    def create_darksky_table(self, table_name):
        """ All darksky tables have the same format.

        Note that location and precipSigned are added by us, not the API."""

        cursor = self.conn.cursor()
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
                    PRIMARY KEY(Location, time));" % table_name)

        self.conn.commit()

    def hours_since_last_record(self, table_name):
        df = pd.read_sql('SELECT * from %s' % table_name, self.conn)
        td = datetime.datetime.now() - df['time'].max()

        return td.seconds/3600 + td.days* 24


if __name__ == '__main__':

    db = DatabaseConnection()

    # Remove records older than a month
    db.delete_old_rows('ds_current', interval='1 month')

    if db.hours_since_last_record('ds_current') > 6:

        ds = darksky.DarkSky()
        current_df = ds.get_past_week_darksky(loc_dict)
        db.add_darksky(current_df, 'ds_current')

        forecast_df = ds.get_nextweek_darksky(loc_dict)

        # We have to drop existing forecasts before adding new ones
        db.drop_table('ds_forecasts')
        db.create_darksky_table('ds_forecasts')
        db.add_darksky(forecast_df, 'ds_forecasts')
