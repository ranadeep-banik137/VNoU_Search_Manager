class Create_table_queries:
    user_creds = """
    CREATE TABLE user_creds (
        UserID VARCHAR(255) PRIMARY KEY,
        UserName VARCHAR(255) UNIQUE NOT NULL,
        Salt LONGBLOB NOT NULL
    )
    """
    user_records = "CREATE TABLE IF NOT EXISTS user_records (UserID VARCHAR(255), FOREIGN KEY (UserID) REFERENCES user_creds(UserID), Name VARCHAR(255) NOT NULL, Gender VARCHAR(255), Email VARCHAR(255) UNIQUE NOT NULL, Phone VARCHAR(255) NOT NULL, DOB VARCHAR(255), Address_L1 VARCHAR(255), Address_L2 VARCHAR(255), City VARCHAR(255), State VARCHAR(255), Country VARCHAR(255))"
    dp_table = "CREATE TABLE IF NOT EXISTS dp_table (UserID VARCHAR(255) UNIQUE, FOREIGN KEY (UserID) REFERENCES user_creds(UserID), Img LONGBLOB NOT NULL)"


class Insert_table_queries:
    insert_all_in_user_creds = """INSERT INTO user_creds (UserID, UserName, Salt) VALUES (%s, %s, %s)"""
    insert_all_in_user_records = """INSERT INTO user_records (UserID, Name, Gender, Email, Phone, DOB, Address_L1, Address_L2, City, State, Country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    insert_all_in_dp_table = """INSERT INTO dp_table (UserID, Img) VALUES (%s, %s)"""


class Update_table_queries:  # UserID and Username cannot be updated
    update_all_in_user_creds_with_id = """UPDATE user_creds SET Salt = %s WHERE UserID = %s"""
    update_all_in_user_records_with_id = """UPDATE user_records SET Name = %s, Gender = %s, Email = %s, Phone = %s, DOB = %s, Address_L1 = %s, Address_L2 = %s, City = %s, State = %s, Country = %s WHERE UserID = %s"""
    update_all_in_dp_table_with_id = """UPDATE dp_table SET Img = %s WHERE UserID = %s"""


class Search_table_queries:
    search_creds_with_uname = """SELECT UserID from user_creds where UserName = '%s'"""
    search_records_with_email = """SELECT UserID from user_records where Email = '%s'"""
    search_records_with_phone = """SELECT UserID from user_records where Phone = '%s'"""
    search_creds_with_id = """SELECT * from user_creds where UserID = '%s'"""
    search_records_with_id = """SELECT * from user_records where UserID = '%s'"""
    search_dp_with_id = """SELECT * from dp_table where UserID = '%s'"""
    search_column_for_value_in_creds = """SELECT %s from user_creds where %s = '%s'"""
    search_column_for_value_in_records = """SELECT %s from user_records where %s = '%s'"""
    search_column_for_value_in_dp = """SELECT %s from dp_table where %s = '%s'"""


class Table_name:
    user_creds = 'user_creds'
    user_records = 'user_records'
    dp_table = 'dp_table'


class Search_variable:
    username = 'UserName'
    email = 'Email'
    phone = 'Phone'
    userid = 'UserID'


class User_creds:
    userid = "UserID"
    username = "UserName"
    salt = "Salt"


class User_records:
    userid = "UserID"
    name = "Name"
    gender = "Gender"
    email = "Email"
    phone = "Phone"
    dob = "DOB"
    address_l1 = "Address_L1"
    address_l2 = "Address_L2"
    city = "City"
    state = "State"
    country = "Country"


class Dp_data:
    userid = "UserID"
    userimg = "Img"
