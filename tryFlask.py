from flask import Flask, render_template, request, redirect, url_for, flash, session
from wtforms import DateField, validators, PasswordField, BooleanField, Form, TextField, StringField
from pymongo import MongoClient
import gc
import pprint

app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    client = MongoClient()
    db = client.flaskProject
    try:
        form = RegistartionForm(request.form)
        if request.method == "POST" and form.validate():
            userFirstName = form.userFirstName.data
            userLastName = form.userLastName.data
            userLogin = form.userLogin.data
            userEmail = form.userEmail.data
            userPassword = form.userPassword.data

            if db.Users.find({"userLogin": userLogin}).count() == 1:
                flash("That login is already taken, please choose another")
                return render_template("signup.html", form=form)
            else:
                result = db.Users.insert_one({
                    "userFirstName": userFirstName,
                    "userLastName": userLastName,
                    "userLogin": userLogin,
                    "userEmail": userEmail,
                    "userPassword": userPassword
                })
                gc.collect()

                session['logged_in'] = True
                session['username'] = userLogin

            return redirect(url_for('main'))

        return render_template('signup.html', form=form)
    except Exception as e:
        return (str(e))


@app.route('/login/', methods=["GET", "POST"])
def login():
    error = ''
    client = MongoClient()
    db = client.flaskProject
    try:
        if request.method == "POST":
            if db.Users.find({"userLogin" : request.form["login"],
                              "userPassword" : request.form["password"]}).count() == 1:
                session['logged_in'] = True
                session['username'] = request.form["login"]
                return redirect(url_for('main'))
            else:
                error = "Invalid login or password. Please try again"

        gc.collect()

        return render_template("login.html", error=error)

    except Exception as e:
        error = "Invalid login or password. Please try again"
        return render_template("login.html", error=error)

@app.route('/logout/')
def logout():
    session.clear()
    gc.collect()
    return redirect(url_for('main'))


class RegistartionForm(Form):
    userFirstName = StringField("First name", [validators.Length(min=4, max=20)])
    userLastName = StringField("Last name", [validators.Length(min=4, max=20)])
    userLogin = StringField("Login", [validators.Length(min=6, max=20)])
    userEmail = StringField("Email", [validators.Length(min=6, max=50)])
    userPassword = PasswordField("New password", [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Password must match")
    ])
    confirm = PasswordField('Repeat password')
    accept_tos = BooleanField("I agree with rules.")


if __name__ == '__main__':
    app.run(port=app.config.get("PORT", 9000))

