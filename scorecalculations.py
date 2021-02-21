# 21/2/21
# Gets everyone's x654 scores from competition results tables and calculates averages and handicaps
# Regularly updates (perhaps when main program is opened providing there's no performance issues)
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"IOMSC_Results.db"

    sql_create_stats_table = """ CREATE TABLE IF NOT EXISTS Stats (
                                        FirstName text,
                                        LastName text,
                                        Handicap integer,
                                        Average integer
                                    ); """


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_stats_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()

# Now that the stats table has been created, we need to get the x654 scores from all competitions and calculate
# from the moving average.

# What is the handicap equation?

# Query through competitions table

with sqlite3.connect("IOMSC_Results.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for tablerow in cursor.fetchall():
        table = tablerow[0]
        cursor.execute("SELECT * FROM {t}".format(t=table))
        for row in cursor:
            for field in row.keys():
                if field == 'FirstName':
                    print(table, field, row[field], row["x654Series"])
                if row[field] == 'Greg':
                    print("Greg found")

