# vim: set fileencoding=utf-8 :

# connord - connect to nordvpn servers
# Copyright (C) 2019  Mael Stor <maelstor@posteo.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sqlite3
from sqlite3 import Error
from cachetools import cached, TTLCache
from connord import ConnordError
from connord import resources


class SqliteError(ConnordError):
    """Thrown within this module"""

    def __init__(self, error=None, message=""):
        self.error = error

        if not message:
            self.message = "Database Error:\n  {}".format(error)
        else:
            self.message = "Database Error: {}\n  {}".format(message, error)


def create_connection(db_file=None):
    """Create a database connection"""
    if not db_file:
        db_file = resources.get_database_file()

    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as error:
        raise SqliteError(
            error, "Could not create a connection to database '{}'".format(db_file)
        )

    return None


def create_table(connection, create_table_sql):
    """Create the table. Prints errors to stdout.

    :param connection: a database connection
    :param create_table_sql: the sql to create the table.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
        connection.commit()
    except Error as error:
        raise SqliteError(error, "Could not create table")


def create_location(connection, location):
    """Create a location in the location table. Prints errors to stdout.

    :param connection: a database connection
    :param location: tuple with (latitude, longitude, display_name, city, country,
                     country_code)
    """
    sql = """ INSERT OR IGNORE INTO locations(
                latitude,
                longitude,
                display_name,
                city,
                country,
                country_code,
                map
              )
              VALUES(?,?,?,?,?,?,?) """

    try:
        cursor = connection.cursor()
        cursor.execute(sql, location)
        connection.commit()
        return cursor.lastrowid
    except Error as error:
        raise SqliteError(error, "Could not create location '{}'".format(location))


def location_exists(connection, latitude, longitude):
    """Return true if a location (latitude, longitude) exists. Prints errors to
    stdout."""
    result = get_columns(
        connection,
        columns="latitude, longitude",
        latitude=latitude,
        longitude=longitude,
        fetch="one",
    )
    return bool(result)


def get_city(connection, latitude, longitude):
    """Return the city specified with latitude and longitude. Prints errors to
    stdout."""
    return get_columns(
        connection, columns="city", latitude=latitude, longitude=longitude, fetch="one"
    )


# deprecated: use get_columns directly
def get_locations(connection):
    """Returns all locations found in the database as list. Prints errors to
    stdout."""
    return get_columns(connection)


# pylint: disable=too-many-arguments
@cached(cache=TTLCache(ttl=60, maxsize=20))
def get_columns(
    connection,
    columns="*",
    table="locations",
    latitude=None,
    longitude=None,
    fetch="all",
):
    """
    Query columns from a given table by unique locations defined by latitude and
    longitude if not None else selects all rows

    param connection: A valid connection to the database
    param columns: A comma separated list of columns. Takes the special value '*'
    param table: query the given table
    param latitude: the latitude of the location
    param longitude: the longitude of the location
    param fetch: the query type 'all' or 'one'. 'many' is currently resolved to 'all'
    returns: the result of the query. May be None if location does not exist
    """

    if latitude is None and longitude is None:
        sql = """SELECT {} FROM {}""".format(columns, table)
    else:
        sql = """SELECT {} FROM {}
                WHERE latitude = {} AND longitude = {}""".format(
            columns, table, latitude, longitude
        )

    try:
        if fetch == "one":
            cursor = connection.cursor()
            result = cursor.execute(sql).fetchone()
            if result:
                return result[0]

            return result

        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        result = cursor.execute(sql).fetchall()
        return result

    except Error as error:
        raise SqliteError(
            error,
            "Failed query of {} for {} with lat={}, lon={}".format(
                columns, table, latitude, longitude
            ),
        )


# deprecated: use get_columns directly
def get_display_name(connection, latitude, longitude):
    """Return the display_name of the city specified by latitude, longitude. Prints
    errors to stdout."""
    return get_columns(
        connection,
        columns="display_name",
        latitude=latitude,
        longitude=longitude,
        fetch="one",
    )


# deprecated: use get_columns directly
def get_map(connection, latitude, longitude):
    return get_columns(
        connection, columns="map", latitude=latitude, longitude=longitude, fetch="one"
    )


def create_location_table(connection):
    """Creates the location table if it doesn't exist.

    :raises: SqliteError if connection is None
    """
    sql_create_location_table = """ CREATE TABLE IF NOT EXISTS locations(
                                        latitude text NOT NULL,
                                        longitude text NOT NULL,
                                        display_name text NOT NULL,
                                        city text NOT NULL,
                                        country NOT NULL,
                                        country_code NOT NULL,
                                        UNIQUE(latitude, longitude)
                                    ); """

    create_table(connection, sql_create_location_table)
