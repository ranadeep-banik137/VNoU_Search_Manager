import logging
from datetime import datetime
from modules.data_reader import get_json_objects_from_directory, get_active_attributes
from modules.json_filtering import filter_jsons_by_range, filter_jsons_by_attr, filter_jsons_by_attrs, filter_jsons_by_ranges
from modules.search_util import search_value_by_attributes, search_value_by_attr


if __name__ == '__main__':
    start_time = datetime.fromisoformat('2024-07-12T13:40:49')
    end_time = datetime.fromisoformat('2024-07-12T13:40:50')
    file_dest = 'files/json_reports'
    all_jsons = get_json_objects_from_directory(file_dest)
    print('Getting all the filtered files')
    logging.info('Getting all the filtered files')
    matched = filter_jsons_by_range(all_jsons, 'timestamp', start_time, end_time)
    print(matched)
    frame_numbers = []
    for match in matched:
        frame_numbers.append(match['frame_number'])
    print(frame_numbers)
    matched_name_json = filter_jsons_by_attr(all_jsons, 'name', 'Ranadeep Banik')
    print(f'Names matched {matched_name_json}')
    matched_frame_json = filter_jsons_by_attr(all_jsons, 'frame_number', 40608)
    print(f'Frames matched {matched_frame_json}')
    detected_frame_json = filter_jsons_by_attr(all_jsons, 'is_person_detected', True)
    print(f'Detected frames matched {detected_frame_json}')
    detected_total_visit_count_json = filter_jsons_by_range(all_jsons, 'total_visit_count', 7, 9)
    print(f'Detected Total visit count matched {detected_total_visit_count_json}')
    detected_mult = search_value_by_attributes(detected_total_visit_count_json, ['is_repeated_user', 'name'])
    print(f'Detected multiple fiters {detected_mult}')
    detected_single_search = search_value_by_attr(detected_total_visit_count_json, 'is_repeated_user')
    print(f'Detected Single fiter {detected_single_search}')

    attr_values = {'user_id': 6, 'email': 'ranadeep.banik137@yahoo.com'}
    attr_values1 = {'is_repeated_user': True, 'unidentified_reason': 'Face Not Identified'}
    mul_filtered = filter_jsons_by_attrs(all_jsons, attr_values)
    print(f'Detected with multiple filters {mul_filtered}')
    mul_filtered1 = filter_jsons_by_attrs(all_jsons, attr_values1)
    print(f'Detected with multiple filters 1 {mul_filtered1}')
    # attr_values2 = attr_values = {'name': 'Ranadeep Banik', 'detected_at': None, 'frame_number': None, 'user_id': 6, 'email': None, 'is_img_saved_in_local': None, 'unidentified_reason': None}
    #attr_values2 = get_active_attributes(name='Ranadeep Banik', detection_time=None, frame_number=None, user_id=6, email=None, has_saved_image=None, unidentified_reason=None)
    #mul_filtered2 = filter_jsons_by_attrs(all_jsons, attr_values2)
    #print(f'Detected with multiple filters 1 {mul_filtered2}')
    att_vals = {
        'timestamp': ('2024-07-14T15:31:44', '2024-07-14T15:36:44'),
        'frame_number': (800, 900),
        'name': ('Ranadeep Banik', None)
    }
    att_vals = {'timestamp': ('2024-07-05T12:07', '2024-07-05T12:08')}
    mul_filtered_values3 = filter_jsons_by_ranges(all_jsons, att_vals)
    print(f'Multiple ranges values {mul_filtered_values3}')

