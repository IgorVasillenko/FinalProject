from db_queries.db_functions import *

'''
TO DO
1. handle db errors -> wrap basic sb functions with try/catch 

'''

def check_login(user_inputs: dict):
    """
    :param: this function receive username and password then check if it exists in the DB.
    :return: if the data is matched to the DB data, return true -> otherwise return false.
    """
    manager_from_db = find_one('managers', user_inputs)
    if manager_from_db:
        return True
    return False

def handle_register(user_input: dict):
    """
    the function send the user inputs to test to see if the inputs are valid.
    if the inputs are valid -> insert the new manager to the DB in managers collection.
    otherwise, handle the error and send the error msg back to the front.
    :param user_input: dictionary of user input from register page, should contain all prop in manager document.
    :return: bool, msg
                bool -> true if everything good with the user's input
                        false if the inputs didnt pass all the tests.
                msg -> if bool is true - none
                        if bool is false - the error msg
    """
    bool, msg = check_register(user_input)
    if bool:
        insert_one('managers', user_input)
        return bool, msg
    return bool, msg



def check_register(user_input: dict):
    """
    valid tests:
        1.check if all the fields are not empty
        2.check if password len > 6
        3.check if username which is _id is not taken
        4.check if the class name is not taken, we need it to be unique
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
    if find_one('managers', query):
        # if the query returned document and the username already exists in the DB
        msg = 'Username is already taken.'
        return False, msg
    if not check_unique_class(user_input):
        # if the class name already exists in the system
        msg = "Class name already exists, please select another name"
        return False , msg
    return True, 'none'


def check_unique_class(user_input:dict):
    """
    Class name should be unique so in this function we check if the user input for class name is valid
    and doesnt exists in the DB for other manager.
    :param user_input: the input dictionary we got from the user in the register page.
    :return: true if the class name doesnt exist ,otherwise -> False
    """
    query = create_query(user_input,'class')
    if find_one('managers',query):
        return False
    return True

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


def create_query(dictionary: dict, prop: str):
    """

    :param dictionary   : given dictionary with some properties.
    :param prop: the property we want to query.
    :return: object where the ket is the prop name and the value is the value from given dict.
            the return obj is ready to be used as a query to the DB.
    """
    return {prop: dictionary[prop]}


def fetch_class_kids(username):
    class_name = find_one('managers', {"_id": username})["class"]
    class_list = find_all("kids", {"class":class_name})
    clean_list_result = handle_cursor_obj(class_list)
    return clean_list_result


def handle_cursor_obj(cursor_obj):
    """
    in this function are going to iterate the given obj and make it a list of documents.
    :param cursor_obj:
    :return: list of documents.
    """
    result = []
    for doc in cursor_obj:
        result.append(doc)
    return result


def handle_addKid_page(username):
    """

    :param username: the teacher username we got from the mainPage
    :return: the class name of the teacher that will be injected to the class name input in addKid html page.
    """
    class_name = find_one('managers', {"_id": username})["class"]
    return class_name

def handle_addKid_post(user_inputs, class_name):
    print(user_inputs)


# def safe_run(func):
#
#     def func_wrapper(*args, **kwargs):
#
#         try:
#            return func(*args, **kwargs)
#
#         except Exception as e:
#
#             print(e)
#             return None
#
#     return func_wrapper

if __name__ == '__main__':
    print('yay')