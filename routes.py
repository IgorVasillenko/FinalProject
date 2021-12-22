from flask import Flask, render_template, redirect, request
from main import *

app = Flask(__name__)
@app.route("/")
def home():
    return render_template('subfolder/home.html')


# @app.route("/login", methods=["POST"])
# def post_login_info():
#     if check_login(request.form.to_dict()):
#         return render_template('subfolder/mainPage.html')
#     else:
#         message = "Wrong username or password"
#         return render_template('subfolder/home.html', message=message)

# @app.route("/register", methods =["GET"])
# def register():
#     return "hello world"


if __name__ == '__main__':
    app.run()
