def search_value_by_attr(filtered_data, attr_name):
    result = {}
    for data in filtered_data:
        if attr_name in filtered_data:
            result[attr_name] = data[attr_name]
    return result


def search_value_by_attributes(filtered_data, attr_names):
    results = []
    for data in filtered_data:
        result = {}
        for attr_name in attr_names:
            if attr_name in data:
                result[attr_name] = data[attr_name]
        if result:  # Add to results only if there's at least one matching attribute
            results.append(result)

    return results
