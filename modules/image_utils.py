import base64
import logging


def convert_img_from_img_path_to_binary(img_path):
    # Convert digital data to binary format
    logging.info(f'Converting the img in location: {img_path} to binary')
    with open(img_path, 'rb') as file:
        binary_data = file.read()
    return binary_data


def convert_img_to_binary(file):
    binary_data = file.read()
    return binary_data


def profile_picture(user_id=None):
    # Fetch the binary image data from the database
    # image_data = get_image_from_db(user_id)  # Implement this function based on your database setup
    image_data = convert_img_from_img_path_to_binary('C:/Users/ranad/Downloads/faces/Deepjoy.png')
    # Encode the binary data to base64
    base64_image = base64.b64encode(image_data).decode('utf-8')

    # Return the base64 string
    return f"data:image/jpeg;base64,{base64_image}"
