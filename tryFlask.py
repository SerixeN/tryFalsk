from flask import Flask, render_template, request, redirect, url_for
from wtforms import DateField, validators, PasswordField, BooleanField, Form

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    try:
        form = RegistartionForm(request.form)

        if request.method == "POST" and form.validate():
            userFirstName = form.userFirstName.data
            userLastName = form.userLastName.data
            userLogin = form.userLogin.data
            userEmail = form.userEmail.data
            userPassword = form.userPassword.data
            return redirect(url_for('main'))

        return render_template('signup.html', form=form)
    except Exception as e:
        return (str(e))


@app.route('/login/')
def login():
    return render_template('login.html')

class RegistartionForm(Form):
    userFirstName = DateField("First name", [validators.Length(min=4, max=20)])
    userLastName = DateField("Last name", [validators.Length(min=4, max=20)])
    userLogin = DateField("Login", [validators.Length(min=6, max=20)])
    userEmail = DateField("Email", [validators.Length(min=6, max=50)])
    userPassword = PasswordField("New password", [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Password must match")
    ])
    confirm = PasswordField('Repeat password')
    accept_tos = BooleanField("I agree with rules.")

if __name__ == '__main__':
    app.run(port=app.config.get("PORT", 9000))
