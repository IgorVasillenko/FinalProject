# from utilities_functions import *


def handle_post_settings(user_inputs, user_details):
    if user_inputs['form-name'] == 'password':
        # print(is_pass_valid(''))
        # check if current pass = pass in db
        # check if new pass is valid (len >6)
        # update the pass in db
        print('password')
    elif user_inputs['form-name'] == 'schedule':
        # update in db
        print('schedule')
    elif user_inputs['form-name'] == 'username':
        # check if new username doesnt exists in db
        # if so, update username in DB
        print('username')
    else:
        # else -> the form is to change class.
        # check if new class name doesnt exists in db
        # if so, update class name
        # update new class name to all class students.
        print('class')


def handle_change_password(user_inputs, user_curr_password):
    pass
