from urllib import parse

import pandas as pd
import psycopg2
import os

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

