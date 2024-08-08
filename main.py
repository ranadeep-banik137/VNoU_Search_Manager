import logging
from datetime import datetime
from modules.data_reader import get_json_objects_from_directory, get_active_attributes
from modules.json_filtering import filter_jsons_by_range, filter_jsons_by_attr, filter_jsons_by_attrs, \
    filter_jsons_by_ranges
from modules.search_util import search_value_by_attributes, search_value_by_attr
from page_object.login_utils import search_identifier, is_password_valid, validate_creds
from modules.data_cache import get_all_db_data, search_merged_data, cache_db_data, get_searched_column_data, get_searched_column_data_from_db
from constants.database_constants import Search_variable, Search_table_queries, Table_name, User_creds
from modules.database_util import create_table, insert_data, get_data_in_tuples, get_pk_id, update_data
from modules.image_utils import get_picture_url_from_binary, convert_img_file_to_binary
from modules.hash_encrypter import hash_password, check_password
from page_object.search_utils import search_data

if __name__ == '__main__':
    # start_time = datetime.fromisoformat('2024-07-12T13:40:49')
    # end_time = datetime.fromisoformat('2024-07-12T13:40:50')
    # file_dest = 'files/json_reports'
    # all_jsons = get_json_objects_from_directory(file_dest)
    # print('Getting all the filtered files')
    # logging.info('Getting all the filtered files')
    # matched = filter_jsons_by_range(all_jsons, 'timestamp', start_time, end_time)
    # print(matched)
    # frame_numbers = []
    # for match in matched:
    #    frame_numbers.append(match['frame_number'])
    # print(frame_numbers)
    # matched_name_json = filter_jsons_by_attr(all_jsons, 'name', 'Ranadeep Banik')
    # print(f'Names matched {matched_name_json}')
    # matched_frame_json = filter_jsons_by_attr(all_jsons, 'frame_number', 40608)
    # print(f'Frames matched {matched_frame_json}')
    # detected_frame_json = filter_jsons_by_attr(all_jsons, 'is_person_detected', True)
    # print(f'Detected frames matched {detected_frame_json}')
    # detected_total_visit_count_json = filter_jsons_by_range(all_jsons, 'total_visit_count', 7, 9)
    # print(f'Detected Total visit count matched {detected_total_visit_count_json}')
    # detected_mult = search_value_by_attributes(detected_total_visit_count_json, ['is_repeated_user', 'name'])
    # print(f'Detected multiple fiters {detected_mult}')
    # detected_single_search = search_value_by_attr(detected_total_visit_count_json, 'is_repeated_user')
    # print(f'Detected Single fiter {detected_single_search}')

    # attr_values = {'user_id': 6, 'email': 'ranadeep.banik137@yahoo.com'}
    # attr_values1 = {'is_repeated_user': True, 'unidentified_reason': 'Face Not Identified'}
    # mul_filtered = filter_jsons_by_attrs(all_jsons, attr_values)
    # print(f'Detected with multiple filters {mul_filtered}')
    # mul_filtered1 = filter_jsons_by_attrs(all_jsons, attr_values1)
    # print(f'Detected with multiple filters 1 {mul_filtered1}')
    # attr_values2 = attr_values = {'name': 'Ranadeep Banik', 'detected_at': None, 'frame_number': None, 'user_id': 6, 'email': None, 'is_img_saved_in_local': None, 'unidentified_reason': None}
    # attr_values2 = get_active_attributes(name='Ranadeep Banik', detection_time=None, frame_number=None, user_id=6, email=None, has_saved_image=None, unidentified_reason=None)
    # mul_filtered2 = filter_jsons_by_attrs(all_jsons, attr_values2)
    # print(f'Detected with multiple filters 1 {mul_filtered2}')
    # att_vals = {
    #    'timestamp': ('2024-07-14T15:31:44', '2024-07-14T15:36:44'),
    #    'frame_number': (800, 900),
    #    'name': ('Ranadeep Banik', None)
    # }
    # att_vals = {'timestamp': ('2024-07-05T12:07', '2024-07-05T12:08')}
    # mul_filtered_values3 = filter_jsons_by_ranges(all_jsons, att_vals)
    # print(f'Multiple ranges values {mul_filtered_values3}')

    # Example: Create table
    #create_table_sql = """
    #CREATE TABLE user_creds (
    #    UserID VARCHAR(255) PRIMARY KEY,
    #    UserName VARCHAR(255) UNIQUE NOT NULL,
    #    Salt VARCHAR(255) NOT NULL
    #)
    #"""
    #create_table(create_table_sql)

    # Example: Insert data
    #insert_sql = "INSERT INTO user_creds (UserID, UserName, Salt) VALUES (%s, %s, %s)"
    #user_data = ("XFDSR987RTS", "ranadeep.banik@vnousolutions.com", hash_password('rana#123'))

    #insert_data(insert_sql=insert_sql, data=user_data)
    #tupler = get_data_in_tuples(table_name='user_creds')
    #print(tupler)

    #insert_details_table = "CREATE TABLE IF NOT EXISTS user_records (UserID VARCHAR(255), FOREIGN KEY (UserID) REFERENCES user_creds(UserID), Name VARCHAR(255) NOT NULL, Gender VARCHAR(255), Email VARCHAR(255) UNIQUE NOT NULL, Phone VARCHAR(255) NOT NULL, DOB VARCHAR(255), Address_L1 VARCHAR(255), Address_L2 VARCHAR(255), City VARCHAR(255), State VARCHAR(255), Country VARCHAR(255))"
    #dp_table = "CREATE TABLE IF NOT EXISTS dp_table (UserID VARCHAR(255) UNIQUE, FOREIGN KEY (UserID) REFERENCES user_creds(UserID), Img LONGBLOB NOT NULL)"

    #create_table(insert_details_table)
    #create_table(dp_table)

    #insert_user_records_sql = "INSERT INTO user_records (UserID, Name, Gender, Email, Phone, DOB, Address_L1, Address_L2, City, State, Country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #print(f'User_id is {tupler[0][0]}')
    #insert_user_records_values = (tupler[0][0], 'Ranadeep Banik', 'Male', 'ranadeep.banik@vnousolutions.com', '7378332802', '1993-03-13', 'R.m.S Chowmani', 'Badurtala Lane', 'Agartala', 'Tripura', 'India')

    #insert_data(insert_sql=insert_user_records_sql, data=insert_user_records_values)
    #tupler_user_records = get_data_in_tuples(table_name='user_records')
    #print(tupler_user_records)

    #insert_user_image_data_sql = "INSERT INTO dp_table (UserID, Img) VALUES (%s, %s)"
    #insert_user_image_data_val = (tupler[0][0], convert_img_file_to_binary('templates/uploads/rana.jpg'))

    #insert_data(insert_sql=insert_user_image_data_sql, data=insert_user_image_data_val)
    #tupler_user_img_records = get_data_in_tuples(table_name='dp_table')
    #print(tupler_user_img_records)
    #_id = get_pk_id(Search_variable.username, "ranadeep.banik@vnousolutions.com")
    #print(f'User in creds {_id}')
    #print(f'User in Records with email {get_pk_id(Search_variable.email, "ranadeep.banik@vnousolutions.com")}')
    #print(f'User in records with phone {get_pk_id(Search_variable.phone, "7378332802")}')
    #print(f'User in records with Invalid {get_pk_id(Search_variable.username, "ranadeep.banik")}')

    #print(f'User_records data {get_data_in_tuples(query=Search_table_queries.search_records_with_id % _id)[0]}')
    #all_data = get_all_db_data()
    #rint(f'All data {all_data}')
    #cache_db_data()
    #_id, search_data = search_merged_data(email='test@example.c')
    #print(f'Searched data 1 {_id} {search_data}')

    #_id2, search_data2 = search_merged_data(email='ranadeep.banik@vnousolutions.com')
    #print(f'Searched data 2 {_id2} {search_data2}')

    #_id3, search_data3 = search_merged_data(phone='7378332802', userid='jhf')
    #print(f'Searched data 3 {_id3} {search_data3}')

    #print(f'Identifier found: {search_identifier("ranadeep.banik@vnousolutions.com")}')

    #print(f'Search column data {get_searched_column_data_from_db(Table_name.user_creds, "Salt", "UserID", "XhsjhgayeS")}')

    #print(f'Search column data from cache {get_searched_column_data("XhsjhgayeS", "salt")}')

    #print(f'Password is valid: {is_password_valid("XhsjhgayeS", "ddd46910-6642-4fa3-ae32-400a0b76c34e")}')

    # Example: Update data


    #update_sql = "UPDATE user_records SET Address_L1 = %s WHERE UserId = %s"
    #values = ('R.M.S test Nagar', "XFDSR987RTS")

    #update_data(update_sql, values)



    # Fresh app

    #_id, is_identifier_valid = search_identifier(identifier='anwesha.bhattacharjee@vnousolutions.com')
    #_id2, is_identifier_valid2 = search_identifier(identifier='8759218242')




    # Example usage
    #plain_password = "rana#123"
    #hashed_password = hash_password(plain_password)
    #print(f"Hashed password: {hashed_password}")


    # Checking the password
    #password_match = check_password(hashed_password, plain_password)
    #unmatched_password = check_password(hashed_password, 'rana#123 ')
    #print(f"Password match: {password_match}")
    #print(f"Password match: {unmatched_password}")

    #_id, is_creds_valid = validate_creds(identifier='8759218242', password='anwesha#123')
    #print(f'{_id} {is_creds_valid}')

    #test = get_pk_id(Search_variable.username, None)
    #print(f'test {test}')

    search_data(name='Ranadeep Banik')

