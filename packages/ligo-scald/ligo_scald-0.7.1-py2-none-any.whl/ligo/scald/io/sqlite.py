#!/usr/bin/env python

__author__ = "Patrick Godwin (patrick.godwin@ligo.org)"
__description__ = "a module for sqlite I/O utilities"

#-------------------------------------------------
### imports

import os
import sqlite3

#-------------------------------------------------
### functions


def store_timeseries(connection, routes, time, data, table):
    ### format query
    columns = ','.join(routes)
    vals = ','.join(['?' for ii in range(len(routes)+1)])
    sql_insert = " INSERT INTO {table}(timestamp,{columns}) VALUES({vals})".format(
        table=table,
        columns=columns,
        vals=vals,
    )

    ### insert rows
    c = connection.cursor()
    for row in zip(time, *[data[route] for route in routes]):
        c.execute(sql_insert, row)

    ### commit changes / close connection
    ### FIXME: really need to handle errors properly
    try:
        connection.commit()
    except sqlite3.OperationalError:
        pass


def retrieve_timeseries(connection, routes, start, end, table):
    ### format query
    columns = ','.join(routes)
    sql_query = " SELECT timestamp,{columns} FROM {table} WHERE timestamp BETWEEN {start} AND {end} ORDER BY timestamp;".format(
        columns=columns,
        table=table,
        start=start,
        end=end,
    )

    c = connection.cursor()
    rows = c.execute(sql_query).fetchall()
    time, data = zip(*rows)

    return time, data


def create_table(connection, routes, table):
    c = connection.cursor()

    columns = ''.join([',{} real'.format(route) for route in routes])
    table = " CREATE TABLE IF NOT EXISTS {table} (timestamp real PRIMARY KEY{columns});".format(
        table=table,
        columns=columns,
    )

    c.execute(table)

    ### commit changes / close connection
    connection.commit()


def create_client(database_name, database_path, extension='sqlite'):
    sqlite_path = os.path.join(database_path, '.'.join([database_name, extension]))
    return sqlite3.connect(sqlite_path)
