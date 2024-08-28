import mysql.connector
from mysql.connector import errorcode
from modules.config_reader import read_config
from constants.database_constants import Search_variable, Search_table_queries


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
        print("Table created successfully.")
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
    error = ''
    conn, cursor = connect()
    try:
        cursor.execute(insert_sql, data)
        conn.commit()
        print("Table data inserted successfully.")
    except mysql.connector.Error as err:
        error = err
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
        return error


def update_data(update_sql, data):
    error = ''
    conn, cursor = connect()
    try:
        print(update_sql, data)
        cursor.execute(update_sql, data)
        conn.commit()
        print("Table updated successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            error = 'Something is wrong with your user name or password.'
            print(error)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            error = "Database does not exist."
            print(error)
        else:
            error = err
            print(err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
        return error


def get_data_in_tuples(table_name=None, query=None):
    conn, cursor = connect()
    records = None
    try:
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


def get_pk_id(field, value):
    match field:
        case Search_variable.username:
            query = Search_table_queries.search_creds_with_uname % value
        case Search_variable.email:
            query = Search_table_queries.search_records_with_email % value
        case Search_variable.phone:
            query = Search_table_queries.search_records_with_phone % value
    result = get_data_in_tuples(query=query)
    return result[0][0] if len(result) > 0 else None
