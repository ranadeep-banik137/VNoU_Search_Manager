from modules.data_reader import is_timestamp_within_range, is_input_within_range


def filter_jsons_by_range(json_objs, attribute_name, start, end):
    matching_jsons = []
    is_range_match = False
    for json_obj in json_objs:
        if attribute_name in json_obj:
            if attribute_name == 'timestamp' or attribute_name == 'detected_at' or attribute_name == 'email_sent_at':
                is_range_match = is_timestamp_within_range(json_obj[attribute_name], start, end)
            elif attribute_name == 'total_visit_count' or attribute_name == 'user_id' or attribute_name == 'frame_number':
                is_range_match = is_input_within_range(json_obj[attribute_name], start, end)
            if is_range_match:
                matching_jsons.append(json_obj)
    return matching_jsons


# Example
# attr_ranges = {
#    'timestamp': ('2024-07-12T13:00:00', '2024-07-12T14:00:00'),
#    'total_visit_count': (3, 5)
#}
def filter_jsons_by_ranges(json_objs, attr_ranges):
    matching_jsons = []

    for json_obj in json_objs:
        match = True
        for attribute_name, (start, end) in attr_ranges.items():
            if attribute_name in json_obj:
                if attribute_name in ['timestamp', 'detected_at', 'email_sent_at']:
                    if not is_timestamp_within_range(json_obj[attribute_name], start, end):
                        match = False
                        break
                elif attribute_name in ['total_visit_count', 'user_id', 'frame_number']:
                    if not is_input_within_range(json_obj[attribute_name], start, end):
                        match = False
                        break
            else:
                match = False
                break
        if match:
            matching_jsons.append(json_obj)

    return matching_jsons


def filter_jsons_by_attr(json_objs, attr_name, attr_val):
    matching_jsons = []
    for json_obj in json_objs:
        if attr_name in json_obj:
            if json_obj[attr_name] == attr_val:
                matching_jsons.append(json_obj)
    return matching_jsons


# Example
# attr_values = {'user_id': 6, 'email': 'ranadeep.banik137@yahoo.com'}
def filter_jsons_by_attrs(json_objs, attr_values):
    matching_jsons = []
    for json_obj in json_objs:
        match = True
        for attr_name, attr_val in attr_values.items():
            attr_val = '' if attr_val is None else attr_val
            if attr_name in json_obj and attr_val != '':
                if json_obj[attr_name] != attr_val:
                    match = False
                    break
            else:
                match = False
                break
        if match:
            matching_jsons.append(json_obj)
    return matching_jsons
