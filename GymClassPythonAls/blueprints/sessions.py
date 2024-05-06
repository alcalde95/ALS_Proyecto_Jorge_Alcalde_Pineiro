import flask
from model.User import User
from model.Clase import Clase
from model.Session import Session
import sirope
from flask import Blueprint, render_template, redirect, request
import flask_login
srp = sirope.Sirope()

sessions_bp = Blueprint("sessions", __name__,template_folder="templates")

@sessions_bp.route("/classes/<id>", methods=["GET","POST"])
@flask_login.login_required
def class_sessions(id):
    if flask.request.method == "POST":
        date = flask.request.form.get("date")
        instructor = flask.request.form.get("instructor")
        insert = True
        if not date or not instructor:
            flask.flash("Faltan campos por llenar")
            insert=False

        insturctor = srp.find_first(User, lambda u: u.email == instructor)
        if not insturctor:
            flask.flash("El instructor no existe")
            insert = False

        if not insert:
            return flask.redirect("/classes/" + id)
        session = Session(id, date, instructor)
        srp.save(session)
    clase = srp.find_first(Clase, lambda c: c.id == id)
    sessions = srp.filter(Session, lambda s: s.class_id == id)
    toRet = {
        "clase": clase,
        "sessions":sessions,
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("classSessions.html", **toRet)

