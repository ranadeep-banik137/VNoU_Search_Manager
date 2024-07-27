import string
import uuid
import random
from modules.data_cache import update_cache, update_db


def update_user_details(user_id, picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state):
    # Cache does not need to be updated as we are forcing cache to pull latest DB data
    # update_cache(user_id, picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state)
    update_db(user_id, picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state)
