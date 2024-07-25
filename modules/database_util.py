import mysql.connector
from mysql.connector import errorcode

class MySQLUtility:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connected to the database successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist.")
            else:
                print(err)

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Connection closed.")

    def create_table(self, create_table_sql):
        try:
            self.cursor.execute(create_table_sql)
            self.connection.commit()
            print("Table created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()

    def insert_data(self, insert_sql, data):
        try:
            self.cursor.execute(insert_sql, data)
            self.connection.commit()
            print("Data inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()

    def update_data(self, update_sql, data):
        try:
            self.cursor.execute(update_sql, data)
            self.connection.commit()
            print("Data updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()

    def drop_table(self, table_name):
        try:
            drop_table_sql = f"DROP TABLE IF EXISTS {table_name}"
            self.cursor.execute(drop_table_sql)
            self.connection.commit()
            print(f"Table {table_name} dropped successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()

if __name__ == "__main__":
    # Update with your AWS RDS credentials
    HOST = 'your-rds-endpoint'
    USER = 'your-username'
    PASSWORD = 'your-password'
    DATABASE = 'your-database'

    db_utility = MySQLUtility(HOST, USER, PASSWORD, DATABASE)
    db_utility.connect()

    # Example: Create table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age INT
    )
    """
    db_utility.create_table(create_table_sql)

    # Example: Insert data
    insert_sql = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
    user_data = ("John Doe", "john.doe@example.com", 30)
    db_utility.insert_data(insert_sql, user_data)

    # Example: Update data
    update_sql = "UPDATE users SET age = %s WHERE email = %s"
    update_data = (31, "john.doe@example.com")
    db_utility.update_data(update_sql, update_data)

    # Example: Drop table
    db_utility.drop_table("users")

    db_utility.close()
