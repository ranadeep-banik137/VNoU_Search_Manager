from modules.data_cache import get_all_identifiers_data, remove_identifier_from_db, update_identifiers_db


def get_all_customer_data(customer_id=None):
    cust_data = get_all_identifiers_data()
    data = []
    for _id, details in cust_data.items():
        if customer_id is None:
            data.append(details)
        else:
            if customer_id == _id:
                data.append(details)
    return data


def get_all_mapped_customers():
    return get_all_identifiers_data()

def delete_customer_by_id(customer_id, user_id):
    return remove_identifier_from_db(cust_id=customer_id, user_id=user_id)


def update_customer_details(user_id, customer_id, name, contact, email, dob, address, city, state, country, img):
    return update_identifiers_db(user_id=user_id, cust_id=customer_id, name=name, contact=contact, email=email, dob=dob, address=address, city=city, state=state, country=country, picture_binary=img)
