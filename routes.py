from flask import Flask, render_template, redirect, request
app = Flask(__name__)

'''
    === HOME PAGE ===
'''
@app.route("/")
def home():
    return render_template('subfolder/home.html')


@app.route("/login", methods=["POST"])
def post_login_info():
    print(request.form)
    print(type(request))
    return render_template('subfolder/home.html')


if __name__ == '__main__':
    app.run(debug=True)