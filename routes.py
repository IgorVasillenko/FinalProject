from flask import Flask, render_template, redirect, request,url_for
from main import *

app = Flask(__name__)

# @app.route("/", methods=["GET" ,"POST"])
# def home():
#     # print('I am here and i want to die, now a bit less')
#     return render_template('subfolder/home.html')


@app.route("/")
def home():
    # print('I am here and i want to die, now a bit less')
    return render_template('subfolder/home.html')


@app.route("/login", methods=["POST"])
def post_login_info():
    if check_login(request.form.to_dict()):
        return render_template('subfolder/mainPage.html')
    else:
        message = "Wrong username or password"
        return render_template('subfolder/home.html', message=message)

@app.route("/register", methods =["GET"])
# this route render the register form.
def register():
    return render_template(('/subfolder/register.html'))

@app.route("/registerCheck", methods =["POST"])
# this route get the user input in register page and handles it.
def registerCheck():
    return "hello world"


if __name__ == '__main__':
    app.run()
