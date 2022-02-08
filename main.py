from db_queries.db_functions import *
from flask import Flask


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

    :param user_input: dictionary of user input from register page, should contain all prop in a document.
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


def handle_addKid_post(user_inputs: dict,  files: dict):
    """
    in this function we need to:
        1. check the text inputs and see if the data is valid
        2. check the image files and see if it's valid.
        3. process the images, transform it to binary context
    if both inputs and files are valid ->  concat them to one dict and insert to the db
    else -> send back the error msg.
    :param user_inputs: text inputs we got from the add_kid post request.
    :param files: the 10 image files we got from our user.
    :return: the function return bool, msg
            bool - true if both text & files are valid -> else false.
            msg - None if bool is true -> else error msg.

    """
    files_bool, files_msg = handle_files(files)
    inputs_bool,inputs_msg = check_add_kid_inputs(user_inputs)


def check_add_kid_inputs(user_inputs:dict):
    """
    the function check the text inputs only. not the image files.
    valid tests:
        1.check if all the fields are not empty
        2.check if id is in the correct len and doesnt contain non-int chars.
        3.check that id doesnt exists in the system
        4.check that phone number has exact 10 chars.
    :param user_inputs: dictionary of user input from addKid page, should contain all prop in kids document.
    :return: the function returns true if all tests are good,
             if any test is wrong -> return false and a msg containing what is wrong with the input.
    """
    if not check_input_fields(user_inputs):
        # some fields left empty
        msg = 'All fields are required'
        return False, msg
    if (not check_len(user_inputs['_id'], 9)) or (not convert_to_int(user_inputs['_id'])):
        # id len < 9 or it contains chars that are not numbers.
        msg = 'ID must be exactly 9 chars and contain only numbers.'
        return False, msg
    if not match_len(user_inputs['parent_phone'], 10) or (not convert_to_int(user_inputs['parent_phone'])):
        # parent phone number is not 10 chars or contains non-int chars.
        msg = 'Parent phone number must be exactly 10 chars. only numbers allowed.'
        return False, msg
    query = create_query(user_inputs, '_id')
    kid = find_one('kids',query)
    if kid:
        # if the kid _id already exists in the system
        msg = f"Kid already exists in the system in {kid['class']} class"
        return False, msg
    return True, None


def convert_to_int(prop):
    """
    :param prop: prop we want to check if it's an int although it comes from the input fields as strings.
    :return: return true if the prop is int , else return false.
    """
    try:
        int_prop = int(prop)
        return True
    except:
        # we had an error converting to string, meaning we have other chars in it.
        return False


def check_len(text, num):
    """

    :param text: a string we want to test his length.
    :param num: the minimum length we want the string to be
    :return: true if the string len is >= given num. otherwise -> return false.
    """
    return len(text) >= num


def match_len(param, num):
    """

    :param param: a parameter we want to test his length.
    :param num: the exact length we want the parameter to be
    :return: true if the parameter len = = given num. otherwise -> return false.
    """
    print(len(param))
    return len(param) == num


def check_suffix(filename):
    """

    :param filename:  the file name we want to check.
    :return: true if the file suffix is in the allowed list.
    """
    ALLOWED_EXTENSIONS = [
        'png',
        'jpg',
        'jpeg',
    ]
    split_str = filename.split(".")
    return split_str[-1].lower() in ALLOWED_EXTENSIONS


def handle_files(files):
    """
    the function check that the user uploaded 10 images and create clean dictionary that
    holds for each file it's name and the binary context of the file.
    in addition, for each file we will check if the suffix is good.
    :param files: dictionary containing file name and fileStorage object.
    :return: bool, msg ->
        bool = if the user uploaded 10 valid pictures return true -> else false.
        msg = if bool is true -> msg will be the clean result dictionary. else-> error msg.
    """
    result_dict = {}
    for k, v in files.items():
        if not v:
            # user didn't upload 10 images.
            msg = "10 images are required."
            return False, msg
        if not check_suffix(v.filename):
            # if the suffix is not in the allowed suffixes.
            msg = "Only images are allowed, other files won't be supported."
            return False, msg
        result_dict[k] = v.read()
    return True, result_dict



if __name__ == '__main__':
    print('yay')