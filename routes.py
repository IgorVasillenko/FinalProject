from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from main import *
import FoldersManager
import os


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
            return render_template("subfolder/editKid.html", kidObj=kid_details, message=msg)


@app.route('/uploadPictures/<className>', methods=["GET", "POST"])
def uploadPictures(className):
    if request.method == "GET":
        return render_template("subfolder/uploadPictures.html", className=className)
    else:
        # the method is post, handle the files , add to db
        handle_uploaded_pictures(request.files.to_dict(), className)
        return 'post made'


if __name__ == '__main__':
    app.run(debug=True)
