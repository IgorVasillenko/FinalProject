from flask import Flask, render_template, redirect, request,url_for
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
        return render_template('subfolder/mainPage.html')
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
        if valid:
            return 'POST REGISTER WORKS'
        else:
            return render_template('/subfolder/register.html', msg=msg)


@app.route("/registerCheck", methods =["POST"])
# this route get the user input in register page and handles it.
def registerCheck():
    return "hello world"


if __name__ == '__main__':
    app.run()
