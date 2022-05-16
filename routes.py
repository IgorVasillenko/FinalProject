from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from main import *
from img_comparing import create_attendance_report
from clock import *


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/images/"

@app.route("/")
def home():
    return render_template('subfolder/home.html')


@app.route("/login", methods=["POST"])
def post_login_info():
    """
    This route take a request with username and password info.
    it sends the data to the check login.
    :return:
        if the function return true -> move the user to the main users page.
        otherwise -> render the login page again with alert to the user about the error.

    """
    if check_login(request.form.to_dict()):
        username = request.form['_id']
        return redirect(f'/mainPage/{username}')
    else:
        message = "Wrong username or password"
        return render_template('subfolder/home.html', message=message)


@app.route("/register", methods =["GET", "POST"])
# this route render the register form.
def register():
    if request.method == "GET":
        return render_template(('/subfolder/register.html'))
    else:
        # The request is POST so we need to validate the data.
        # if the handler function return true -> redirect to the main users page
        # otherwise -> alert the user what is the problem.
        valid, msg = handle_register(request.form.to_dict())
        # valid = False
        if valid:
            username = request.form['_id']
            return redirect(f'/mainPage/{username}')
        else:
            return render_template('/subfolder/register.html', msg=msg)


@app.route('/mainPage/<username>', methods=["GET"])
# this route get the user input in register page and handles it.
def mainPage(username):
    """
    This request should:
        1. get the username of the user
        2. query the kids collection and fetch the records.
    :param name:
    :return: render the html with injected username and data rows.
    """
    data = fetch_class_kids(username)
    if data:
        # there are students in the class .
        class_name = data[0]["class"]
    else:
        class_name = find_one('managers', {"_id": username})["class"]

    return render_template("subfolder/mainPage.html", username=username, data=data, class_name=class_name )


@app.route('/addKid/<username>', methods=["GET", "POST"])
# this route handle the get and post request for adding kids.
def addKid(username):
    if request.method == "GET":
        class_name = handle_addKid_page(username)
        return render_template("subfolder/addKid.html", class_name=class_name)
    else:
        '''
        the request method is post, which means we have to handle the request data.
        we send the user inputs and the class name we got from the main page to the handle function.
        then we render the mainPage again with an Error or success msg.

        '''
        user_inputs = request.form.to_dict()
        user_inputs['class'] = username
        bool, msg = handle_addKid_post(user_inputs, request.files.to_dict())
        if bool:
            # get from DB the teacher username of current class.
            class_teacher = fetch_username_using_classname(user_inputs['class'])
            return redirect(f'/mainPage/{class_teacher}')
        else:
            return render_template("subfolder/addKid.html", class_name=username, message=msg)


@app.route('/editKid/<kidId>', methods =["GET", "POST"])
# this route handle the get and post request for editing kids.
def editKid(kidId):
    kid_details = find_one('kids', {"_id": kidId})
    class_teacher = fetch_username_using_classname(kid_details['class'])

    if request.method == "GET":
        return render_template("subfolder/editKid.html", kidObj=kid_details, teacher_username=class_teacher)
    else:
        '''
        the request method is post, which means we have to handle the request data.
        we send the user both inputs and files to the handle function.
        '''
        bool, msg = handle_editKid_post(request.form.to_dict(), request.files.to_dict())
        if bool:
            '''the inputs were valid, db was update - return the main page.'''
            return redirect(f'/mainPage/{class_teacher}')
        else:
            '''inputs weren't good, re-render the page with the error msg.'''
            return render_template("subfolder/editKid.html", kidObj=kid_details, message=msg, teacher_username= class_teacher)


@app.route('/uploadPictures/<className>', methods=["GET", "POST"])
def uploadPictures(className):
    username = fetch_username_using_classname(className)
    if request.method == "GET":
        return render_template("subfolder/uploadPictures.html", className=className, username=username)
    else:
        # the method is post, handle the files , add to db
        uploaded_images = handle_uploaded_pictures(request.files.to_dict(), className)
        if uploaded_images > 0:
            # if any images uploaded, alert the user
            return render_template("subfolder/uploadPictures.html", className=className,
                                   uploaded_images=uploaded_images, username=username)
        return render_template("subfolder/uploadPictures.html", className=className, username=username)


@app.route('/middleware/<moveTo>/<variable>/', methods=["GET"])
def middleware_endpoint(moveTo, variable):
    """
    move to mainPage -> fetch the username and redirect
    move to settings -> fetch the username and redirect
    :param class_name:
    :return:
    """
    if moveTo in ['mainPage', 'settings']:
        username = fetch_username_using_classname(variable)
        print(username, variable)
        return redirect(f'/{moveTo}/{username}')
    # if moveTo in ['uploadPictures']:
        # print(variable):


@app.route('/settings/<username>/', methods=["GET", "POST"])
def settings(username):
    user_details = find_one(collection='managers', query={"_id": username})
    if request.method == "GET":
        return render_template("subfolder/settings.html",
                               username=username, user_details=user_details,
                               className=user_details['class'])
    else:
        # the request method is POST, handle the changes and re-render the page with a msg.
        response_obj = handle_post_settings(user_inputs=request.form.to_dict(), user_details=user_details)
        # fetch user data again since we updated
        user_details = find_one(collection='managers', query={"_id": username})
        return render_template("subfolder/settings.html", username=username, user_details=user_details,
                               className=user_details['class'], response_obj=response_obj)


@app.route('/deleteKid/<kidId>', methods = ["GET"])
# this route get kid_id and deletes from DB
def deleteKid(kidId):
    class_name = find_one(collection="kids", query={"_id": kidId})["class"]
    username = fetch_username_using_classname(classname=class_name)
    print(username)
    delete_one(collection="kids", query={"_id": kidId})
    return redirect(f'/mainPage/{username}')


@app.route('/report/<username>', methods=["GET", "POST"])
# this route handle the report-UI and the options to view older reports.
# the post option is for reports of other dates.
# and the default value of the date is today's date.
def report(username):
    now = datetime.now()
    print("report route start", now.strftime("%H:%M:%S"))

    teacher_details = find_one('managers', {"_id": username})
    curr_date = date.today().strftime("%d/%m/%Y")
    today_attendance = None
    max_date_for_html = transform_date_to_html_format(curr_date)
    kids_details = fetch_class_kids(username)

    if request.method == "GET":
        today_attendance = find_one('attendance', {"class_name": teacher_details["class"], "date": curr_date})
        # after using curr_date to fetch from db, change it to html format.
        curr_date = max_date_for_html

    else:
        # print(request.args.get("curr_date"))
        curr_date = request.form["curr_date"]
        db_date = transform_date_to_db_format(curr_date)
        today_attendance = find_one('attendance', {"class_name": teacher_details["class"], "date": db_date})

    now = datetime.now()
    print("END OF REPORT ROUTE: ", now.strftime("%H:%M:%S"))
    return render_template("subfolder/report.html", username=username, curr_date=curr_date,
                           class_name=teacher_details["class"], max_date=max_date_for_html,
                           attendence=today_attendance, schedule=teacher_details["schedule"],
                           kids=kids_details)


@app.route('/produceReport', methods=["POST"])
# this route activate the producing of the attendance report
def produce_report():
    '''
    NOTE TO ===AMIT====
    when creating the schedule chain the sms sending right after
    and remeber to add sms_sent property set to true.
    :return:
    '''
    now = datetime.now()
    print("start time:", now.strftime("%H:%M:%S"))

    username, curr_date, class_name = request.form["username"], request.form["curr_date"], request.form["class"]
    db_date_format = transform_date_to_db_format(curr_date)
    produce_by_click(class_name=class_name, curr_date=db_date_format)
    # return redirect(f"load/{username}")
    return redirect(f"mainPage/{username}")


@app.route('/load/<username>', methods=["GET"])
def load(username):
    return render_template('subfolder/load.html', username=username)


@app.route('/check_attendance', methods=["GET"])
def check_attendance():
    """gets a querystring containing the username"""

    now = datetime.now()
    curr_date = get_db_date_format(now)

    username = request.args.get('username')
    class_name = find_one('managers', {"_id": username})["class"]

    today_attendance = find_one('attendance', {"class_name": class_name, "date": curr_date}, projection={"images":0})
    if "last_update" in today_attendance:
        print("last_update exists")
        return {"bool": True, "curr_date": curr_date}
    print("last_update doesnt exists")
    return {"bool": False}


if __name__ == '__main__':
    app.run(debug=True)
