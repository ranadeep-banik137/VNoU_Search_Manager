from modules.data_cache import search_merged_data, add_user_to_db
from page_object.login_utils import search_identifier


def is_identifier_already_used(identifier):
    _id, identifier_exists = search_identifier(identifier=identifier)
    return identifier_exists


def is_email_used(identifier):
    _id, details = search_merged_data(email=identifier)
    return details is not None


def is_username_used(identifier):
    _id, details = search_merged_data(username=identifier)
    return details is not None


def add_user_data(picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state, username, new_password):
    add_user_to_db(picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state, username, new_password)
