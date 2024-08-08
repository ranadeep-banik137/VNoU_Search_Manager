log_attributes = [
    "timestamp",
    "frame_number",
    "user_id",
    "name",
    "contact",
    "email",
    "detected_at",
    "total_visit_count",
    "model",
    "is_repeated_user",
    "is_img_saved_in_local",
    "unidentified_reason",
    "image_link"
]


def map_search_contents(search_json):
    result_json = {}
    for attr in log_attributes:
        value = search_json.get(attr)
        result_json[attr] = 'N/A' if value is None or value == '' else value
    return result_json


