import os
import time
import datetime
from modules.database_util import get_data_in_tuples, get_pk_id, update_data, insert_data
from constants.database_constants import Table_name, Search_variable, Search_table_queries, User_creds, Dp_data, Update_table_queries, Insert_table_queries, User_records, Delete_table_data_queries
from constants.database_constants import Roles
from modules.config_reader import read_config
from modules.image_utils import get_picture_url_from_binary, get_default_no_img_binary
from modules.hash_encrypter import hash_password
from modules.id_generator import create_user_id


# Cached data
config = read_config()
cached_data = {}
cache_last_updated = 0
cache_expiry_secs = int(os.getenv('CACHE_EXPIRATION_IN_SECONDS', config['cache_expiry']))


def cache_db_data():
    global cached_data
    global cache_last_updated
    # Check if cache is expired or empty
    if time.time() - cache_last_updated > cache_expiry_secs or cached_data is None:
        # Fetch data from the database
        cached_data = get_all_db_data()
        cache_last_updated = time.time()
    return cached_data


def force_refresh_cache():
    global cached_data
    cached_data = get_all_db_data()


def get_all_db_data():
    data_tuple_user_cred = get_data_in_tuples(Table_name.user_creds)
    data = {}
    for row in data_tuple_user_cred:
        row_data = {}
        userid = row[0]
        data_tuple_user_records = get_data_in_tuples(query=Search_table_queries.search_records_with_id % userid)[0]
        data_tuple_existing_creds = get_data_in_tuples(query=Search_table_queries.search_history_with_id % userid)
        row_data['UserName'] = row[1]
        row_data['Role'] = get_data_in_tuples(query=Search_table_queries.get_role_with_id % row[2])[0][0]
        row_data['Salt'] = row[3]
        row_data['CreatedOn'] = row[4]
        row_data['ExistingSalt'] = None if len(data_tuple_existing_creds) <= 0 else data_tuple_existing_creds[0][1]
        row_data['TimeModified'] = None if len(data_tuple_existing_creds) <= 0 else data_tuple_existing_creds[0][2]
        row_data['Name'] = data_tuple_user_records[1]
        row_data['Gender'] = data_tuple_user_records[2]
        row_data['Email'] = data_tuple_user_records[3]
        row_data['Phone'] = data_tuple_user_records[4]
        row_data['DOB'] = data_tuple_user_records[5]
        row_data['Address_L1'] = data_tuple_user_records[6]
        row_data['Address_L2'] = data_tuple_user_records[7]
        row_data['City'] = data_tuple_user_records[8]
        row_data['State'] = data_tuple_user_records[9]
        row_data['Country'] = data_tuple_user_records[10]
        data_tuple_dp_table = get_data_in_tuples(query=Search_table_queries.search_dp_with_id % userid)
        row_data['Img'] = None if len(data_tuple_dp_table) <= 0 else data_tuple_dp_table[0][1]
        row_data['Img_URL'] = None if len(data_tuple_dp_table) <= 0 else get_picture_url_from_binary(data_tuple_dp_table[0][1])
        data[userid] = row_data
    return data


def get_all_identifiers_data():
    data_tuple_identifiers = get_data_in_tuples(Table_name.identifiers)
    data = {}
    for row in data_tuple_identifiers:
        row_data = {}
        cust_id = row[0]
        data_tuple_identifier_records = get_data_in_tuples(query=Search_table_queries.search_record_history_with_cust_id % cust_id)[0]
        row_data['CustID'] = cust_id
        row_data['Name'] = row[1]
        row_data['CustImg'] = get_picture_url_from_binary(row[2])
        row_data['Contact'] = row[3]
        row_data['DOB'] = row[4]
        row_data['Email'] = row[5]
        row_data['Address'] = row[6]
        row_data['City'] = row[7]
        row_data['State'] = row[8]
        row_data['Country'] = row[9]
        row_data['EnrollDate'] = data_tuple_identifier_records[1]
        row_data['EnrollerID'] = data_tuple_identifier_records[2]
        row_data['EnrolledBy'] = get_searched_column_data(data_tuple_identifier_records[2], User_records.name)
        data[cust_id] = row_data

    return data


def search_merged_data(username=None, email=None, phone=None, userid=None):
    result = None
    if userid is not None and username is None and email is None and phone is None:
        result = cache_db_data().get(userid)
    else:
        userid = get_pk_id(Search_variable.username, username) if username else (get_pk_id(Search_variable.email, email) if email else (get_pk_id(Search_variable.phone, phone) if phone else userid))
        if userid is not None:
            for _id, row_data in cache_db_data().items():
                result = row_data if _id == userid else result
    return userid, result


def get_searched_column_data_from_db(table, return_column, column_search, column_value):
    query = Search_table_queries.search_column_for_value_in_creds if table == Table_name.user_creds else (Search_table_queries.search_column_for_value_in_records if table == Table_name.user_records else Search_table_queries.search_column_for_value_in_dp)
    tuple_records = get_data_in_tuples(query=query % (return_column, column_search, column_value))
    return None if len(tuple_records) <= 0 else tuple_records[0][0]


def get_searched_column_data(search_id, column):
    value = None
    for _id, row_data in cache_db_data().items():
        if _id == search_id:
            value = row_data.get(column)
    return value


def update_cache(userid, picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state):
    updated_details = {}
    for _id, details in cached_data.items():
        if _id == userid:
            updated_details['UserName'] = get_searched_column_data(userid, User_creds.username)
            updated_details['Salt'] = get_searched_column_data(userid, User_creds.salt)
            updated_details['Name'] = name
            updated_details['Gender'] = gender
            updated_details['Email'] = email
            updated_details['Phone'] = phone
            updated_details['DOB'] = dob
            updated_details['Address_L1'] = address_l1
            updated_details['Address_L2'] = address_l2
            updated_details['City'] = city
            updated_details['State'] = state
            updated_details['Country'] = country
            updated_details['Img'] = picture_binary if picture_binary is not None else get_searched_column_data(userid, Dp_data.userimg)
            updated_details['Img_URL'] = get_picture_url_from_binary(updated_details.get('Img'))
            break
    cached_data.get(userid).update(updated_details)


def update_identifiers_db(user_id, cust_id, picture_binary, name, email, contact, address, dob, city, country, state):
    time_current = time.time()
    timestamp = datetime.datetime.fromtimestamp(time_current).strftime('%Y-%m-%d %H:%M:%S')
    error = update_data(Update_table_queries.update_all_in_identifiers_with_id, (name, contact, dob, email, address, city, state, country, cust_id))
    print(f'error1: {error}')
    if picture_binary is not None and error == '':
        error = update_data(Update_table_queries.update_img_in_identifiers_with_id, (picture_binary, cust_id))
        print(f'error2: {error}')
    id_err = update_data(Update_table_queries.update_all_in_identifier_records_with_id, (timestamp, user_id, cust_id)) if error == '' else error
    print(f'error3: {id_err}')
    return id_err == '', id_err,


def remove_identifier_from_db(cust_id, user_id):
    success = True
    time_current = time.time()
    timestamp = datetime.datetime.fromtimestamp(time_current).strftime('%Y-%m-%d %H:%M:%S')
    insert_data(Insert_table_queries.insert_all_into_deleted_identifiers, (cust_id, timestamp, user_id))
    error = update_data(Delete_table_data_queries.delete_identifier_records_with_id, (cust_id,))
    if error == '':
        error2 = update_data(Delete_table_data_queries.delete_identifier_with_id, (cust_id,))
        success = error2 == ''
        error = error2
    return success, error


def update_db(userid, picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state):
    update_data(Update_table_queries.update_all_in_user_records_with_id, (name, gender, email, phone, dob, address_l1, address_l2, city, state, country, userid))
    if picture_binary is not None:
        update_data(Update_table_queries.update_all_in_dp_table_with_id, (picture_binary, userid))
    force_refresh_cache()


def update_password(userid, existing_hashed_password, new_hashed_password):
    time_created = time.time()
    timestamp = datetime.datetime.fromtimestamp(time_created).strftime('%Y-%m-%d %H:%M:%S')
    update_data(Update_table_queries.update_all_in_user_creds_with_id, (new_hashed_password, userid))
    insert_data(Insert_table_queries.insert_all_in_user_creds_history, (userid, existing_hashed_password, timestamp))
    force_refresh_cache()


def add_user_to_db(picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state, username, new_password):
    user_id = create_user_id()
    time_created = time.time()
    timestamp = datetime.datetime.fromtimestamp(time_created).strftime('%Y-%m-%d %H:%M:%S')
    insert_data(Insert_table_queries.insert_all_in_user_creds, (user_id, username, Roles.admin, hash_password(new_password), timestamp))
    insert_data(Insert_table_queries.insert_all_in_user_records, (user_id, name, gender, email, phone, dob, address_l1, address_l2, city, state, country))
    insert_data(Insert_table_queries.insert_all_in_dp_table, (user_id, get_default_no_img_binary() if picture_binary is None else picture_binary))
    force_refresh_cache()


def add_customer_data_to_db(user_id, picture_binary, name, contact, dob, email, address, city, country, state):
    cust_id = f'CUST_{create_user_id()}'
    enroll_time = time.time()
    timestamp = datetime.datetime.fromtimestamp(enroll_time).strftime('%Y-%m-%d %H:%M:%S')
    error_identifier = insert_data(Insert_table_queries.insert_all_into_identifiers, (cust_id, name, picture_binary, contact, dob, email, address, city, state, country))
    error_id_records = error_identifier if error_identifier != '' else insert_data(Insert_table_queries.insert_all_into_identifier_records, (cust_id, timestamp, user_id))
    error = error_identifier or error_id_records
    message = f'Successfully onboarded customer data. Customer ID: {cust_id}' if error == '' else f'Something wrong happened while onboarding customer data: {error}'
    status = 'danger' if error != '' else 'success'
    return message, status
