from modules.data_cache import search_merged_data, get_searched_column_data, update_password
from constants.database_constants import User_creds, User_records, User_creds_history
from modules.hash_encrypter import check_password, hash_password


def validate_email_and_get_id(identifier):
    _id, result = search_merged_data(email=identifier)
    return _id, result is not None


def validate_dob_and_name(user_id, name, dob):
    if user_id is None:
        return False
    db_dob = get_searched_column_data(user_id, User_records.dob)
    db_name = get_searched_column_data(user_id, User_records.name)
    return name == db_name and dob == db_dob


def validate_username(user_id, username):
    if user_id is None:
        return False
    db_username = get_searched_column_data(user_id, User_creds.username)
    return username == db_username


def is_password_existing(search_id, password):
    existing_password = get_searched_column_data(search_id, User_creds_history.existing_salt)
    return False if existing_password is None else check_password(existing_password, password)


def update_new_password_for_user(userid, password):
    existing_password = get_searched_column_data(userid, User_creds.salt)
    new_hashed_password = hash_password(password=password)
    update_password(userid=userid, new_hashed_password=new_hashed_password, existing_hashed_password=existing_password)
