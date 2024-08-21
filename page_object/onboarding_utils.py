from modules.data_cache import add_customer_data_to_db
from modules.image_utils import convert_img_to_binary


def onboard_users(user, details, img):
    full_name = f"{details.get('first_name')} {'' if details.get('middle_name') == '' else (details.get('middle_name') + ' ')}{details.get('last_name')}"
    return add_customer_data_to_db(name=full_name, dob=details.get('dob'), email=details.get('email'), contact=details.get('phone'), country='', state='', city='', address='', picture_binary=convert_img_to_binary(img), user_id=user)
