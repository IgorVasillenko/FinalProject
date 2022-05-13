# from FinalProject.db_queries.db_functions import *
from db_queries.db_functions import *

def is_pass_valid(password):
    """

    :param password: the user input password
    :return: true if the password.len >= 6. otherwise -> false.
    """
    return len(password) >= 5


def create_query(dictionary: dict, prop: str):
    """

    :param dictionary   : given dictionary with some properties.
    :param prop: the property we want to query.
    :return: object where the ket is the prop name and the value is the value from given dict.
            the return obj is ready to be used as a query to the DB.
    """
    return {prop: dictionary[prop]}


def check_unique_username(user_inputs):
    """

    :param user_inputs:
    :return: true if the new user name doesn't exists in db
            if the username is already taken -> return false
    """
    query = create_query(user_inputs, '_id')
    if find_one('managers', query):
        return False
    return True


# print(check_unique_username({"_id": 'sdada'}))
