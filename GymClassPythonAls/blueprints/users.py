import flask
from model.User import User
from model.Clase import Clase
from model.Session import Session
from model.Inscriptions import Inscription
import sirope
from flask import Blueprint, render_template, redirect, request
import flask_login
srp = sirope.Sirope()

users_bp = Blueprint("users", __name__,template_folder="templates")

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        if flask_login.current_user.is_authenticated:
            return flask.redirect("/classes")

    if flask.request.method == "POST":
        email = flask.request.form.get("email")
        pswd = flask.request.form.get("pswd")
        usr = User.find(srp, email)

        if usr is not None and usr.compara_password(pswd):
            flask_login.login_user(usr)

            if usr.email == 'admin':
                return flask.redirect("/admin")
            else:
                return flask.redirect("/classes")
        else:
            flask.flash("usuario o contraseña incorrectos")
    return flask.render_template("login.html")

@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        email = flask.request.form.get("email")
        pswd = flask.request.form.get("pswd")
        pswd2 = flask.request.form.get("pswd2")

        error = False
        if not email or not pswd or not pswd2:
            error = True
            flask.flash("Faltan campos por llenar")
        if pswd != pswd2:
            error = True
            flask.flash("contraseñas no coinciden")
        if len(pswd) < 8:
            error = True
            flask.flash("Contraseña muy corta.Mínimo 8 caracteres")

        if len(email) < 3:
            error = True
            flask.flash("Email muy corto")


        exists = srp.find_first(User, lambda u: u.email == email)
        if exists is not None:
            error = True
            flask.flash("usuario ya registrado")

        if error:
            return flask.render_template("register.html")

        usr = User(email, pswd)
        srp.save(usr)
        return flask.redirect("/login")
    return flask.render_template("register.html")

@users_bp.route("/users/delete/<email>", methods=["GET"])
@flask_login.login_required
def delete_user(email):
    if flask_login.current_user.email != 'admin':
        return flask.redirect("/")
    user = srp.find_first(User, lambda c: c.email == email)
    srp.delete(user.__oid__)

    classes = srp.filter(Clase, lambda c: c.creador == email)

    for clase in classes:
        sessions = srp.filter(Session, lambda s: s.class_id == clase.id)
        for session in sessions:
            srp.delete(session.__oid__)
        inscriptions = srp.filter(Inscription, lambda i: i.class_id == clase)
        for inscription in inscriptions:
            srp.delete(inscription.__oid__)
        srp.delete(clase.__oid__)

    inscribedClasses = srp.filter(Inscription, lambda i: i.user == email)
    for inscribedClass in inscribedClasses:
        srp.delete(inscribedClass.__oid__)
    return flask.redirect("/admin")

