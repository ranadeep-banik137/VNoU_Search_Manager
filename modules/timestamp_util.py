from datetime import datetime
import time


def is_epoch_time(timestamp):
    # Check if the timestamp is a digit (integer in string form) or an actual integer
    if isinstance(timestamp, int):
        return True
    elif isinstance(timestamp, str) and timestamp.isdigit():
        return True
    return False


def is_iso8601(timestamp):
    # Try to parse the timestamp as an ISO 8601 datetime string
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False


def convert_to_epoch_time(time):
    if isinstance(time, datetime):
        return int(time.timestamp())
    elif is_epoch_time(time):
        return time
    elif is_iso8601(time):
        return int(datetime.fromisoformat(time).timestamp())
    else:
        raise TypeError("Expected a datetime object")


def convert_human_readable_date_from_epoch(epoch_time):
    time_struct = time.localtime(epoch_time)
    # Format the time in DD Mon YYYY format
    formatted_time = time.strftime("%d %b %Y", time_struct)
    return formatted_time
