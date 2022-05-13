from .utilities_functions import *
# from ..db_queries.db_functions import *
# from FinalProject.db_queries.db_functions import *
from db_queries.db_functions import *


def handle_post_settings(user_inputs: dict, user_details: dict):
    if user_inputs['form-name'] == 'password':
        return handle_change_password(user_inputs=user_inputs, user_curr_password=user_details["password"],
                                      user_details=user_details)
    elif user_inputs['form-name'] == 'schedule':
        return handle_change_schedule(user_inputs=user_inputs, user_details=user_details)
    elif user_inputs['form-name'] == 'username':
        handle_change_username(user_inputs=user_inputs, user_details=user_details)
        print(user_inputs)

    else:
        # else -> the form is to change class.
        # check if new class name doesnt exists in db
        # if so, update class name
        # update new class name to all class students.
        print('class')


def handle_change_password(user_inputs, user_curr_password, user_details):
    """
        1.check if current pass = pass in db
        2.check if new pass is valid (len >6)
        3. if both 1 and 2 ture => update the pass in db
    :return: dict => { bool: true/ false , msg:msg }
            bool ->true if updated successfully , otherwise false.
            msg -> if bool is true return success msg, otherwise failure msg.
    """
    if str(user_inputs["current_password"]) != user_curr_password:
        # User input for current password is wrong -> didn't pass the validation.
        return {"bool": False, "password_msg": "Password wasn't updated. Incorrect current password."}
    elif not is_pass_valid(user_inputs["new_password"]):
        # New password is not valid.
        return {"bool": False, "password_msg": "Password wasn't updated. New password must be at least 6 chars."}
    else:
        # new pass is ok -> add to db.
        update_one(collection='managers', query={"_id": user_details["_id"]},
                   newValues={"password": user_inputs["new_password"]})
        return {"bool": True, "password_msg": "Password updated successfully."}


def handle_change_schedule(user_inputs, user_details):
    if not user_inputs["new_schedule"]:
        # input is empty
        pass
    elif user_inputs["new_schedule"] == user_details["schedule"]:
        # prevent un-necessary DB updated.
        pass
    else:
        # update the new schedule
        update_one(collection="managers", query={"_id": user_details["_id"]},
                   newValues={"schedule": user_inputs["new_schedule"]})
    # for both elif and else, return true with success msg.
    return {"bool": True, "schedule_msg": "Schedule successfully updated."}


def handle_change_username(user_inputs: dict, user_details: dict):
    if not user_inputs["new_username"] or user_inputs["new_username"] == user_details["_id"]:
        # input is empty or the input equal current username
        pass
    elif check_unique_username({"_id": user_inputs["new_username"]}):
        # The username doesn't exists in the db, update and return.
        # update_one(collection="managers", query=)
        return {"bool": True, "username_msg": "Username successfully updated."}
    else:
        # Username already exists in the system, return false and msg.
        return {"bool": True, "username_msg": "Username is already taken.."}
