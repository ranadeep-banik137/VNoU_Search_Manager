from modules.data_cache import search_merged_data


def get_user_details(user_id):
    return search_merged_data(userid=user_id)[1]
