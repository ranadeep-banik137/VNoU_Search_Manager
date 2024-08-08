import base64
import json
import os
import shutil
import logging
import time
import requests
from modules.timestamp_util import convert_to_epoch_time, is_epoch_time


def read_file(filename=f'{os.getenv("PROJECT_PATH") or ""}data/database.csv'):
    f = open(filename, "r")
    return f.read().splitlines()


def add_entry_to_file(entry, src=f'{os.getenv("PROJECT_PATH") or ""}data/database.csv',
                      bkp_dest=f'{os.getenv("PROJECT_PATH") or ".."}/data/database_bkp.csv', is_backup_needed=True):
    if is_backup_needed:
        shutil.copyfile(src, bkp_dest)
    f = open(src, "a+")
    f.write(entry)


def get_available_image(index):
    try:
        f = open(f'{os.getenv("PROJECT_PATH") or ""}img/{index}.png', "r")
        return f'{os.getenv("PROJECT_PATH") or ""}img/{index}.png'
    except Exception as err:
        return f'{os.getenv("PROJECT_PATH") or ""}img/{index}.jpg'


def convertToBinaryData(filename):
    # Convert digital data to binary format
    logging.info(f'Converting the img in location: {filename} to binary')
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data


def convert_binary_to_img(data, filename):
    with open(filename, "wb") as fh:
        fh.write(data)
    return filename


def convert_img_to_base64(image_path):
    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Read the binary data
        img_binary = image_file.read()
        # Encode the binary data to base64
        base64_img = base64.b64encode(img_binary).decode('utf-8')
    return base64_img


def convert_image_url_to_base64(image_url):
    # Send a HTTP request to the URL to fetch the image
    response = requests.get(image_url)
    # Ensure the request was successful
    if response.status_code == 200:
        # Read the binary content of the response
        img_binary = response.content
        # Encode the binary data to base64
        base64_img = base64.b64encode(img_binary).decode('utf-8')
        return base64_img
    else:
        raise Exception(f"Failed to retrieve image from URL: {image_url}")


def remove_file(filename):
    os.remove(filename)


def get_file_names(folder_path=f'{os.getenv("PROJECT_PATH") or ""}img'):
    return [file_name for file_name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file_name))]


def get_file_names_with_dir(folder_path=f'{os.getenv("PROJECT_PATH") or ""}img'):
    return [f"{folder_path}/{file_name}" for file_name in os.listdir(folder_path) if
            os.path.isfile(os.path.join(folder_path, file_name))]


def get_file_names_excluding_file(folder_path=f'{os.getenv("PROJECT_PATH") or ""}img', exclude_file_name=''):
    return [file_name for file_name in os.listdir(folder_path) if
            os.path.isfile(os.path.join(folder_path, file_name)) and file_name != exclude_file_name]


def is_img_file(file_path):
    flag = False
    if os.path.basename(file_path) in ['.jpg', '.jpeg', '.png', '.img']:
        flag = True
    return flag


def wait_until_file_is_ready(file, retry=5):
    while retry != 0:
        if os.path.exists(file):
            is_file_ready = False
            while not is_file_ready:
                initial_size = os.path.getsize(file)
                time.sleep(10)
                current_size = os.path.getsize(file)
                if initial_size == current_size:
                    is_file_ready = True
                    retry = 0
        else:
            retry = retry - 1


def get_missing_items_from_tuple_list(main_list, latest_list):
    main_set = set(main_list)
    missing_items = []
    for item in latest_list:
        if item not in main_set:
            missing_items.append(item)
    return missing_items


def fetch_first_element_in_tuple(tuple_data):
    return tuple_data[0][0] if tuple_data else None


def make_dir_if_not_exist(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory) and directory != '':
        os.makedirs(directory)
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            logging.debug(f'File at {file_path} created')


def get_tuple_from_list_matching_column(tuple_list, column_val, column_index):
    filtered_list = [item for item in tuple_list if item[column_index] == column_val]
    return filtered_list[0] if filtered_list else None


def get_tuple_index_from_list_matching_column(tuple_list, column_val, column_index):
    index = None
    index_incrementer = 0
    for row in tuple_list:
        if row[column_index] == column_val:
            index = index_incrementer
            break
        index_incrementer += 1
    return index


def get_json_objects_from_file(json_file_path):
    json_objects = []
    line_count = 0
    with open(json_file_path, 'r') as json_file:
        for line in json_file:
            line_count += 1
            try:
                line = line.replace("'", '"')
                json_obj = json.loads(line)
                json_objects.append(json_obj)
            except json.JSONDecodeError as e:
                logging.error(f'Error in parsing JSON in line {line_count} {e}')
    # Now `json_objects` contains all the JSON objects from the file
    return json_objects


def get_json_objects_from_directory(file_dir):
    json_objects = []
    file_list = get_file_names_with_dir(file_dir)
    for file in file_list:
        json_objects.extend(get_json_objects_from_file(file))
    return json_objects


def is_timestamp_within_range(timestamp, start_time, end_time=None):
    epoch_input_time = convert_to_epoch_time(timestamp)
    epoch_start_time = start_time if is_epoch_time(start_time) else convert_to_epoch_time(start_time)
    if end_time is not None:
        epoch_end_time = end_time if is_epoch_time(end_time) else convert_to_epoch_time(end_time)
        return epoch_start_time <= epoch_input_time <= epoch_end_time
    else:
        return epoch_start_time <= epoch_input_time


def is_input_within_range(current_val, start, end=None):
    return start <= current_val if end is None else start <= current_val <= end


def fetch_all_log_files(logs_dir):
    log_files = []
    for root, dirs, files in os.walk(logs_dir):
        for file in files:
            if file.endswith(".log"):  # Assuming log files have a .log extension
                log_files.append(os.path.join(root, file))
    return log_files


def process_log_files(log_files):
    json_data = []
    for log_file in log_files:
        with open(log_file, 'r') as file:
            try:
                for line in file:
                    log_data = json.loads(line)
                    json_data.append(log_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {log_file}: {e}")
    return json_data


def get_active_attributes(name=None, start_detection_time=None, end_detection_time=None, start_frame_number=None,
                          end_frame_number=None, user_id=None, email=None, has_saved_image=False,
                          unidentified_reason=None):
    attr_values = {}
    if name:  # This checks for both None and empty string
        attr_values['name'] = (name, None)
    if start_detection_time or end_detection_time:
        attr_values['detected_at'] = (start_detection_time, end_detection_time)
    if start_frame_number or end_frame_number:  # Keep this to check for None explicitly
        attr_values['frame_number'] = (start_frame_number, end_frame_number)
    if user_id is not None:
        attr_values['user_id'] = (user_id, None)
    if email:
        attr_values['email'] = (email, None)
    if has_saved_image is not None:  # Keep this to check for None explicitly
        attr_values['is_img_saved_in_local'] = (has_saved_image, None)
    if unidentified_reason:
        attr_values['unidentified_reason'] = (unidentified_reason, None)
    return attr_values
