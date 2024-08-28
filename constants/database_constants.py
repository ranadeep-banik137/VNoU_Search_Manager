class Create_table_queries:
    roles = """
    CREATE TABLE roles (
        RoleID INTEGER PRIMARY KEY,
        RoleType VARCHAR(255) UNIQUE NOT NULL
    )
    """
    user_creds = """
    CREATE TABLE user_creds (
        UserID VARCHAR(255) PRIMARY KEY,
        UserName VARCHAR(255) UNIQUE NOT NULL,
        Role INTEGER NOT NULL,
        Salt LONGBLOB NOT NULL,
        CreatedOn TIMESTAMP NOT NULL
    )
    """
    user_creds_history = """
    CREATE TABLE user_creds_history (
        UserID VARCHAR(255) PRIMARY KEY,
        ExistingSalt LONGBLOB NOT NULL,
        TimeModified TIMESTAMP NOT NULL
    )
    """
    user_records = "CREATE TABLE IF NOT EXISTS user_records (UserID VARCHAR(255), FOREIGN KEY (UserID) REFERENCES user_creds(UserID), Name VARCHAR(255) NOT NULL, Gender VARCHAR(255), Email VARCHAR(255) UNIQUE NOT NULL, Phone VARCHAR(255) NOT NULL, DOB VARCHAR(255), Address_L1 VARCHAR(255), Address_L2 VARCHAR(255), City VARCHAR(255), State VARCHAR(255), Country VARCHAR(255))"
    dp_table = "CREATE TABLE IF NOT EXISTS dp_table (UserID VARCHAR(255) UNIQUE, FOREIGN KEY (UserID) REFERENCES user_creds(UserID), Img LONGBLOB NOT NULL)"
    identifiers = "CREATE TABLE IF NOT EXISTS \
			identifiers (CustID VARCHAR(255) PRIMARY KEY, Name VARCHAR(255) NOT NULL,\
			CustImg LONGBLOB NOT NULL, Contact VARCHAR(255), DOB VARCHAR(255), Email VARCHAR(255), Address VARCHAR(255), City VARCHAR(255), State VARCHAR(255), Country VARCHAR(255))"
    identifier_records = "CREATE TABLE IF NOT EXISTS identifier_records (CustID VARCHAR(255), FOREIGN KEY (CustID) REFERENCES identifiers(CustID), EnrollDate TIMESTAMP NOT NULL, EnrollerId VARCHAR(255))"
    deleted_identifiers = "CREATE TABLE IF NOT EXISTS deleted_identifiers (CustID VARCHAR(255) NOT NULL, RemovalDate TIMESTAMP NOT NULL, RemoverID VARCHAR(255) NOT NULL)"


class Insert_table_queries:
    insert_all_in_user_creds = """INSERT INTO user_creds (UserID, UserName, Role, Salt, CreatedOn) VALUES (%s, %s, %s, %s, %s)"""
    insert_all_in_user_records = """INSERT INTO user_records (UserID, Name, Gender, Email, Phone, DOB, Address_L1, Address_L2, City, State, Country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    insert_all_in_dp_table = """INSERT INTO dp_table (UserID, Img) VALUES (%s, %s)"""
    insert_all_in_user_creds_history = """INSERT INTO user_creds_history (UserID, ExistingSalt, TimeModified) VALUES (%s, %s, %s)"""
    insert_al_into_roles = """INSERT INTO roles (RoleID, RoleType) VALUES (%s, %s)"""
    insert_all_into_identifier_records = """INSERT INTO identifier_records (CustID, EnrollDate, EnrollerId) VALUES (%s, %s, %s)"""
    insert_all_into_identifiers = """INSERT INTO identifiers (CustID, Name, CustImg, Contact, DOB, Email, Address, City, State, Country)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    insert_all_into_deleted_identifiers = """INSERT INTO deleted_identifiers (CustID, RemovalDate, RemoverID) VALUES (%s, %s, %s)"""


class Update_table_queries:  # UserID and Username cannot be updated
    update_all_in_user_creds_with_id = """UPDATE user_creds SET Salt = %s WHERE UserID = %s"""
    update_all_in_user_records_with_id = """UPDATE user_records SET Name = %s, Gender = %s, Email = %s, Phone = %s, DOB = %s, Address_L1 = %s, Address_L2 = %s, City = %s, State = %s, Country = %s WHERE UserID = %s"""
    update_all_in_dp_table_with_id = """UPDATE dp_table SET Img = %s WHERE UserID = %s"""
    update_all_in_identifiers_with_id = """UPDATE identifiers SET Name = %s, Contact = %s, DOB = %s, Email = %s, Address = %s, City = %s, State = %s, Country = %s WHERE CustID = %s"""
    update_img_in_identifiers_with_id = """UPDATE identifiers SET CustImg = %s WHERE CustID = %s"""
    update_all_in_identifier_records_with_id = """UPDATE identifier_records SET UpdatedOn = %s, UpdatedBy = %s WHERE CustID = %s"""


class Delete_table_data_queries:
    delete_identifier_with_id = """DELETE FROM identifiers WHERE CustID = %s"""
    delete_identifier_records_with_id = """DELETE FROM identifier_records WHERE CustID = %s"""


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
    search_history_with_id = """SELECT * from user_creds_history where UserID = '%s'"""
    get_role_with_id = """SELECT RoleType from roles where RoleID = '%s'"""
    search_records_with_cust_id = """SELECT * FROM identifiers where CustID = '%s'"""
    search_record_history_with_cust_id = """SELECT * FROM identifier_records where CustID = '%s'"""

class Table_name:
    user_creds = 'user_creds'
    user_records = 'user_records'
    dp_table = 'dp_table'
    identifiers = 'identifiers'
    identifier_records = 'identifier_records'


class Search_variable:
    name = 'Name'
    username = 'UserName'
    email = 'Email'
    phone = 'Phone'
    userid = 'UserID'
    custid = 'CustID'


class User_creds:
    userid = "UserID"
    username = "UserName"
    salt = "Salt"
    role = "Role"
    created_on = "CreatedOn"


class User_creds_history:
    userid = "UserID"
    existing_salt = "ExistingSalt"
    time_modified = "TimeModified"


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


class Roles:
    default = 1;
    admin = 1;
    employee = 2;
    customer = 3;
    support = 4
