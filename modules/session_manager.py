session = {}


def clear_session():
    global session
    session.clear()


def get_session():
    global session
    return session


def add_session(key, data):
    global session
    session[key] = data


def get_session_value(key):
    return session.get(key)
