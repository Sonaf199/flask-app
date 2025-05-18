from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import NameForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config.update(
    SECRET_KEY = '6b1f34c5d8a7e10c25f79ab02f39c37eb3c8d0a94d7b452b',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # Use True if HTTPS, False for local dev
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800,  # 30 minutes
    SQLALCHEMY_DATABASE_URI='sqlite:///firstapp.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

csrf = CSRFProtect(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    form = NameForm()
    if form.validate_on_submit():
        name = form.fname.data
        new_user = User(fname=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    data = User.query.all()
    return render_template("index.html", data=data, form=form)

@app.route("/delete/<int:id>")
def delete(id):
    user_to_delete = User.query.get(id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    user = User.query.get(id)
    form = NameForm(obj=user)
    if form.validate_on_submit():
        user.fname = form.fname.data
        db.session.commit()
        return redirect("/")
    return render_template("update.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
