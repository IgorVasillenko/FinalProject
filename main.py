from db_queries.db_functions import *


def check_login(user_inputs: dict):
    """
    :param: this function receive username and password then check if it exists in the DB.
    :return: if the data is matched to the DB data, return true -> otherwise return false.
    """
    print(user_inputs)
    manager_from_db = find_one('managers', user_inputs)
    print(manager_from_db)
    if manager_from_db:
        return True
    return False


def check_register(user_input: dict):
    """
    valid tests:
        1.check if all the fields are not empty
        2.check if password len > 6
        3.check if username which is _id is not taken
    :param user_input: dictionary of user input from register page, should contain all prop in manager document.
    :return: the function returns true if all text are good, if any test is wrong -> return false.
    """
    if not check_input_fields(user_input):
        # if even one input is empty , return false and error msg.
        msg = 'All fields are required.'
        return False, msg
    if not is_pass_valid(user_input['password']):
        # if the password user entered is less then 6 chars.
        msg = 'Password must be at least 6 chars.'
        return False, msg
    query = create_query(user_input, '_id')
    if find_one('manager', query):
        # if the query returned document and the username already exists in the DB
        msg = 'Username is already taken.'
        return False, msg
    return True, 'none'


def check_input_fields(user_input: dict):
    """

    :param user_input: dictionary of user input from register page, should contain all prop in manager document.
    :return: true if all input fields len > 0 , otherwise return false

    """
    for val in user_input.values():
        if is_empty(val):
            return False
    return True


def is_empty(property):
    '''

    :param property: the function get a property we got from the user
    :return: true if the property is empty string -> otherwise False
    '''
    return (len(property) == 0)


def is_pass_valid(password):
    """

    :param password: the user input password
    :return: true if the password.len >= 6. otherwise -> false.
    """
    return len(password) >= 5


def create_query(dict: dict, prop: str):
    """

    :param dict: given dictionary with some properties.
    :param prop: the property we want to query.
    :return: object where the ket is the prop name and the value is the value from given dict.
            the return obj is ready to be used as a query to the DB.
    """
    return {prop: dict[prop]}
