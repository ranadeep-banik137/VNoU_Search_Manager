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
    _id, first_search = search_merged_data(username=identifier)
    _id, second_search = search_merged_data(email=identifier)
    _id, data = (search_merged_data(phone=identifier) if second_search is None else (_id, second_search)) if first_search is None else (_id, first_search)
    return _id, data is not None


def is_password_valid(search_id, password):
    hashed_password = get_searched_column_data(search_id, User_creds.salt)
    print(f'Hashed: {hashed_password}')
    print(f'Password: {password}')
    return False if hashed_password is None else check_password(hashed_password, password)
