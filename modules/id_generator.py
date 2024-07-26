import string
import uuid
import random


def create_uuid():
    uuid_hash = str(uuid.uuid4())
    print(f'UUID created {uuid_hash}')
    return uuid_hash


def create_user_id():
    chars = string.ascii_uppercase + string.digits
    username = ''.join(random.choice(chars) for _ in range(8))
    print(f'User created {username}')
    return username
