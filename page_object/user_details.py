import string
import uuid
import random

from modules.image_utils import profile_picture, get_picture_url_from_binary


user_data = {}
login_details = {}


def default_cred():
    login_data = {}
    default = 'default'
    login_cred_data = {
        'user_name': 'ranadeep.banik',
        'Phone': '7378332802',
        'Email': 'ranadeep.banik@vnousolutions.com',
        'password': 'rana#123'
    }
    login_data[default] = {
        'creds': login_cred_data
    }
    return login_data


def default_data():
    data = {'default': {
        'user_name': 'ranadeep.banik@vnousolutions.com',
        'profile_picture_url': 'https://media.licdn.com/dms/image/C4D03AQF_aRH-ovJl6w/profile-displayphoto-shrink_800_800/0/1656588367653?e=1727308800&v=beta&t=EojZIwZbDuPS6Ns3yEo_yQB8ZBj_NkG0heGbqBODidc',  # Default picture
        'user_details': {
            'Name': 'Ranadeep Banik',
            'Gender': 'Male',
            'Email': 'ranadeep.banik@vnousolutions.com',
            'Phone': '123-456-7890',
            'DOB': '1993-03-13',
            'Address L1': '123 Main Street gsiugsiug',
            'Address L2': 'Additional infoihvasixusxkjgasiugas',
            'City': 'Agartala',
            'State': 'Tripura',
            'Country': 'India'
        }
    }}
    return data


def get_user_data(_id):
    data = default_data() if len(user_data.items()) == 0 else user_data
    return data.get(_id)


def update_data(user_id, picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state):
    user_details = {
        'Name': name,
        'Gender': gender,
        'Email': email,
        'Phone': phone,
        'DOB': dob,
        'Address L1': address_l1,
        'Address L2': address_l2,
        'City': city,
        'State': state,
        'Country': country
    }
    get_user_data_from = get_user_data(user_id)
    user_data[user_id] = {
        'user_name': get_user_data_from.get('user_name'),
        'profile_picture_url': profile_picture() if picture_binary is None else picture_binary,
        'user_details': user_details
    }


def get_user_creds(identifier):
    datas = default_cred()
    if len(login_details.items()) == 0:
        return 'default', datas.get('default')
    else:
        data = None
        for _id, dt in login_details.items():
            val = dt.get('creds')
            if val.get('user_name') == identifier or val.get('Email') == identifier or val.get('Phone') == identifier:
                data = dt
    return _id, data if data is not None else 'default', datas.get('default')


def add_data(picture_binary, name, gender, email, phone, address_l1, address_l2, dob, city, country, state, new_password):
    user_details = {
        'Name': name,
        'Gender': gender,
        'Email': email,
        'Phone': phone,
        'DOB': dob,
        'Address L1': address_l1,
        'Address L2': address_l2,
        'City': city,
        'State': state,
        'Country': country,
    }
    user_id = create_user_id()
    user_name = create_user_name()
    user_data[user_id] = {
        'user_name': user_name,
        'profile_picture_url': profile_picture() if picture_binary is None else get_picture_url_from_binary(picture_binary),
        'user_details': user_details
    }
    cred_details = {
        'user_name': user_name,
        'Email': email,
        'Phone': phone,
        'password': new_password
    }
    login_details[user_id] = {
        'creds': cred_details
    }


def create_user_id():
    user_id = str(uuid.uuid4())
    print(f'User ID created {user_id}')
    return user_id


def create_user_name():
    chars = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(chars) for _ in range(8))
    print(f'User created {username}')
    return username
