from flask import Flask, render_template, redirect, request, url_for
from main import *

app = Flask(__name__)


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


@app.route('/mainPage/<username>', methods =["GET"])
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

    return render_template("subfolder/mainPage.html", username=username, data=data)


@app.route('/addKid/<username>', methods =["GET", "POST"])
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

        handle_addKid_post(user_inputs=request.form.to_dict(), class_name=username)
        print(request.form.to_dict())
        print(username)

        return'yaya'





if __name__ == '__main__':
    app.run()
