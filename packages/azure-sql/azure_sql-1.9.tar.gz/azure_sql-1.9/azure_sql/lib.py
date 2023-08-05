import datetime
import urllib

import pyodbc
import pandas as pd

from sqlalchemy import create_engine


def generate_connection_string(username, password, database, server, port=1477, driver="{ODBC Driver 17 for SQL Server}"):
    con_str = "DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password}"
    con_str = con_str.format(username=username, password=password, database=database,
                             server=server, port=port, driver=driver)
    return con_str


def sql_df(query='', username="", password="", database='', server="",
                   driver='{ODBC Driver 17 for SQL Server}'):
    # Setup connection parameters

    connection_string = generate_connection_string(username, password, database, server)
    params = urllib.parse.quote_plus(connection_string)
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)

    # Read from database
    temp_df = pd.read_sql(query, engine)

    return temp_df


read_sql_to_df = sql_df


def df_sql(df, table='', username="", password="", database='', server='',
                    if_exists='append', chunksize=10000, driver='{ODBC Driver 17 for SQL Server}',
                    update_date=True):
    # Add datestamp to df
    if update_date:
        df.insert(0, 'update_date', datetime.date.today())
        # Setup connection parameters

    connection_string = generate_connection_string(username, password, database, server)

    params = urllib.parse.quote_plus(connection_string)

    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)

    # Write (update) df to database.table
    df.to_sql(table, con=engine, if_exists=if_exists, index=False, chunksize=chunksize)


write_df_to_sql = df_sql


def query(query='', username="", password="", database='', server='',
                             driver='{ODBC Driver 17 for SQL Server}'):
    # Setup connection parameters
    connection_string = generate_connection_string(username, password, database, server)
    params = urllib.parse.quote_plus(connection_string)
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)

    # Execute query
    connection = engine.connect()
    connection.execute(query)
    connection.close()


query_sql_without_return = query


def connect(username, password, database, server, port=1477, driver="{ODBC Driver 17 for SQL Server}"):
    con_str = generate_connection_string(username, password, database, server, port, driver)
    cnxn = pyodbc.connect(con_str)
    c = cnxn.cursor()
    return cnxn, c


def insert(cursor, table, object, replace=None, commit=None,verbose=False):
    c = cursor
    if replace:
        c.execute("delete from {} where {} = ?".format(table, replace), object[replace])
    sql = "insert into {} ({})VALUES({})".format(table,
                                                 ",".join(list(object.keys())),
                                                 ",".join(["?"] * len(object)))
    if verbose:
    	print(sql,object)
    c.execute(sql, *list(object.values()))
    if commit:
        commit.commit()
    return c


if __name__ == "__main__":
    creds = ["vlad@#####sqlserver", "#####", "#####_team", "#####sqlserver.database.windows.net"]
    table = "#####_item_attrs_temp"

    if True and "read":
        sql = "select TOP(10) * from {}".format(table)

        print(sql_df(sql, *creds))

    if True and "write":
        df = pd.DataFrame([{"Artykul": "101-404-451", }])
        print(df_sql(df, table, *creds))

    if True and "query":
        query("delete from {}".format(table), *creds)

    if True and "insert":
        cnxn, c = connect(*creds)
        insert(c, table, {"Artykul": "101-404-451", "Brand": "Huawei"})
        insert(c, table, {"Artykul": "101-404-451", "Brand": "Apple"}, commit=cnxn, replace="Artykul")
