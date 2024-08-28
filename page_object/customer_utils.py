from modules.data_cache import get_all_identifiers_data, remove_identifier_from_db


def get_all_customer_data():
    cust_data = get_all_identifiers_data()
    data = []
    for _id, details in cust_data.items():
        data.append(details)
    return data


def delete_customer_by_id(customer_id):
    return remove_identifier_from_db(customer_id)
