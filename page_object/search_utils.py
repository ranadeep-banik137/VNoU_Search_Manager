from modules.json_filtering import filter_jsons_by_ranges
from modules.data_reader import get_json_objects_from_directory, get_active_attributes, process_log_files, fetch_all_log_files
from modules.config_reader import read_config
from constants.search_constants import map_search_contents

config = read_config()


# Dummy function to represent your search function
def search_data(name=None, start_detection_time=None, end_detection_time=None, start_frame_number=None, end_frame_number=None, user_id=None, email=None, has_saved_image=None, unidentified_reason=None):
    # This should be replaced with your actual search function logic
    attr_values = get_active_attributes(name, start_detection_time, end_detection_time, start_frame_number, end_frame_number, user_id, email, has_saved_image, unidentified_reason)
    print(f'Input attributes: {attr_values}')

    file_src = config['file_transfer']['dest']
    all_jsons = process_log_files(fetch_all_log_files(file_src))

    # all_jsons = get_json_objects_from_directory(file_dest)
    filtered = filter_jsons_by_ranges(all_jsons, attr_values) if len(attr_values) > 0 else []
    results = []
    for filtered_data in filtered:
        results.append(map_search_contents(filtered_data))
    return results
