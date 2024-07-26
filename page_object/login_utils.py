from modules.data_cache import search_merged_data, get_searched_column_data
from constants.database_constants import User_creds
from modules.hash_encrypter import check_password


def validate_creds(identifier, password):
    flag = False
    _id, is_identifier_valid = search_identifier(identifier=identifier)
    if is_identifier_valid:
        if is_password_valid(_id, password):
            flag = True
    return _id, flag


def search_identifier(identifier):
    user_search_tuple = search_merged_data(username=identifier)
    email_search_tuple = search_merged_data(email=identifier)
    phone_search_tuple = search_merged_data(phone=identifier)
    _id, data = (phone_search_tuple if email_search_tuple[1] is None else email_search_tuple) if user_search_tuple[1] is None else user_search_tuple
    return _id, data is not None


def is_password_valid(search_id, password):
    hashed_password = get_searched_column_data(search_id, User_creds.salt)
    return False if hashed_password is None else check_password(hashed_password, password)
