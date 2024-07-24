from modules.image_utils import profile_picture


user_data = {}


def default_data():
    data = {1: {
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
    user_data[user_id] = {
        'user_name': 'ranadeep.banik@vnousolutions.com',
        'profile_picture_url': profile_picture() if picture_binary is None else picture_binary,
        'user_details': user_details
    }
