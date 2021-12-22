from FinalProject.db_queries.db_functions import *


def check_login(user_inputs:dict):
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

