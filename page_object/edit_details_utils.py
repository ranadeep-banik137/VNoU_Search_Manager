import string
import uuid
import random
from modules.data_cache import update_cache, update_db


def update_user_details(user_id, picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state):
    update_cache(user_id, picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state)
    update_db(user_id, picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state)


def create_user_id():
    user_id = str(uuid.uuid4())
    print(f'User ID created {user_id}')
    return user_id


def create_user_name():
    chars = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(chars) for _ in range(8))
    print(f'User created {username}')
    return username
