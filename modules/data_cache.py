import os
import time
from modules.database_util import get_data_in_tuples, get_pk_id, update_data, insert_data
from constants.database_constants import Table_name, Search_variable, Search_table_queries, User_creds, Dp_data, Update_table_queries, Insert_table_queries
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
        row_data['UserName'] = row[1]
        row_data['Salt'] = row[2]
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
        data_tuple_dp_table = get_data_in_tuples(query=Search_table_queries.search_dp_with_id % userid)[0]
        row_data['Img'] = data_tuple_dp_table[1]
        row_data['Img_URL'] = get_picture_url_from_binary(data_tuple_dp_table[1])
        data[userid] = row_data
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


def update_db(userid, picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state):
    update_data(Update_table_queries.update_all_in_user_records_with_id, (name, gender, email, phone, dob, address_l1, address_l2, city, state, country, userid))
    if picture_binary is not None:
        update_data(Update_table_queries.update_all_in_dp_table_with_id, (picture_binary, userid))
    force_refresh_cache()


def add_user_to_db(picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state, username, new_password):
    user_id = create_user_id()
    insert_data(Insert_table_queries.insert_all_in_user_creds, (user_id, username, hash_password(new_password)))
    insert_data(Insert_table_queries.insert_all_in_user_records, (user_id, name, gender, email, phone, dob, address_l1, address_l2, city, state, country))
    insert_data(Insert_table_queries.insert_all_in_dp_table, (user_id, get_default_no_img_binary() if picture_binary is None else picture_binary))
    force_refresh_cache()
