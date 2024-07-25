import mysql.connector
from mysql.connector import errorcode
from modules.config_reader import read_config


def connect():
    config = read_config()
    database_conf = config['local_database'] if config['exec_mode'] != 'AWS' else config['database']
    dbconfig = {
        'user': database_conf['user'],
        'password': database_conf['password'],
        'host': database_conf['host'],
        'database': database_conf['db']
    }
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)

    return conn, cursor


def create_table(query):
    conn, cursor = connect()
    try:
        cursor.execute(query)
        print("Table 'user_creds' created successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def insert_data(insert_sql, data):
    conn, cursor = connect()
    try:
        cursor.execute(insert_sql, data)
        conn.commit()
        print("Table 'user_creds' created successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
    finally:
        if conn.is_connected():
            conn.close()
            cursor.close()


def update_data(update_sql, data):
    conn, cursor = connect()
    try:
        cursor.execute(update_sql, data)
        conn.commit()
        print("Table 'user_creds' created successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def get_data_in_tuples(table_name, query=None):
    conn, cursor = connect()
    records = tuple
    try:
        # query = """ SELECT * from users where name = %s """
        if query is None:
            cursor.execute(f""" SELECT * from {table_name} """)
        else:
            cursor.execute(query)
        records = cursor.fetchall()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
    finally:
        # Close the connection object
        conn.close()
        cursor.close()
        return records
