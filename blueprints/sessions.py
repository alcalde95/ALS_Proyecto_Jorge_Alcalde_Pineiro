import datetime
from datetime import datetime

import flask
from model.User import User
from model.Clase import Clase
from model.Session import Session
from model.Inscription import Inscription
import sirope
from flask import Blueprint, render_template, redirect, request
import flask_login

srp = sirope.Sirope()

sessions_bp = Blueprint("sessions", __name__, template_folder="templates")
#TODO: AÑADIR VERIFICACIÓN DE QUE NO EXISTEN MÁS PERSONAS INSCRITAS QUE EL NÚMERO MÁXIMO PUESTO EN LA CLASE DE LA QUE CAEN
date_format = '%Y-%m-%dT%H:%M'
@sessions_bp.route("/classes/<id>", methods=["GET", "POST"])
@flask_login.login_required
def class_sessions(id):
    if flask.request.method == "POST":
        date = flask.request.form.get("date")
        print(flask.request.form)
        instructor = flask.request.form.get("instructor")
        print(date, instructor,"pepe")
        insert = True
        if not date or not instructor:
            flask.flash("Faltan campos por llenar")
            insert = False

        insturctor = srp.find_first(User, lambda u: u.email == instructor)
        if not insturctor:
            flask.flash("El instructor no existe")
            insert = False
        if date:
            if datetime.strptime(date, date_format) < datetime.now():
                flask.flash("La fecha no puede ser menor a la actual")
                insert = False

        if not insert:
            return flask.redirect("/classes/" + id)

        existsSession = srp.find_first(Session, lambda s: s.class_id == id and s.date == date and s.instructor == instructor)
        if existsSession:
            flask.flash("Ya existe una sesión con esa fecha e instructor")
        else:
            session = Session(id, date, instructor)
            srp.save(session)
    clase = srp.find_first(Clase, lambda c: c.id == id)
    sessions = srp.filter(Session, lambda s: s.class_id == id)
    instructors = srp.filter(User, lambda u: u.email != "admin")
    toRet = {
        "clase": clase,
        "sessions": list(sessions),
        "instructors": list(instructors),
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("classSessions.html", **toRet)

@sessions_bp.route("/classes/<id>/managed", methods=["GET"])
@flask_login.login_required
def class_sessions_managed(id):

    clase = srp.find_first(Clase, lambda c: c.id == id)
    sessions = srp.filter(Session, lambda s: s.class_id == id and s.instructor == flask_login.current_user.email)
    toRet = {
        "clase": clase,
        "sessions": list(sessions),
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("managedSessions.html", **toRet)


@sessions_bp.route("/classes/<id>/delete", methods=["POST"])
@flask_login.login_required
def class_sessions_delete(id):
    date = flask.request.form.get("dateD")
    instructor = flask.request.form.get("instructorD")
    session = srp.find_first(Session, lambda s: s.class_id == id and s.date == date and s.instructor == instructor)
    if session is not None:
        srp.delete(session.__oid__)
        inscriptions = srp.filter(Inscription, lambda i: i.class_id == id and i.date == date and i.instructor == instructor)
        for ins in inscriptions:
            srp.delete(ins.__oid__)
    return redirect("/classes/" + id)

@sessions_bp.route("/classes/<id>/clients", methods=["GET", "POST"])
@flask_login.login_required
def class_sessions_clients(id):
    if flask.request.method == "POST":
        date = flask.request.form.get("date")
        instructor = flask.request.form.get("instructor")
        class_id = id
        user = flask_login.current_user.email
        exist = srp.find_first(Inscription, lambda i: i.class_id == class_id and i.date == date and i.user == user and i.instructor == instructor)
        if exist:
            flask.flash("Ya te has inscrito a esta clase")
            print("Nop")
        else:
            ins = Inscription(class_id, date, instructor, user)
            srp.save(ins)

    clase = srp.find_first(Clase, lambda c: c.id == id)
    sessions = list(srp.filter(Session, lambda s: s.class_id == id))
    inscriptions = list(srp.filter(Inscription, lambda i: i.class_id == id and i.user == flask_login.current_user.email))
    print(len(list(inscriptions)))

    inscribedSessions = []
    nonInscribedSessions = list(sessions)

    for session in sessions:
        for ins in inscriptions:
            if session.date == ins.date:
                inscribedSessions.append(session)
                nonInscribedSessions.remove(session)


    toRet = {
        "clase": clase,
        "inscribedSessions": inscribedSessions,
        "nonInscribedSessions": nonInscribedSessions,
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("classSessionsUsers.html", **toRet)

@sessions_bp.route("/classes/<id>/clients/unsubscribe", methods=["POST"])
@flask_login.login_required
def class_sessions_clients_unsubscribe(id):

    date = flask.request.form.get("dateSession")
    instructor = flask.request.form.get("instructorSession")


    clase = srp.find_first(Clase, lambda c: c.id == id)
    session = list(srp.filter(Session, lambda s: s.class_id == id and s.date == date))
    if clase is not None and session is not None:
        print(id, date, instructor, flask_login.current_user.email)
        inscription = srp.find_first(Inscription, lambda i: i.class_id == id and i.date == date and i.instructor == instructor and i.user == flask_login.current_user.email)
        if inscription is not None:

            srp.delete(inscription.__oid__)

    return redirect("/classes/" + id + "/clients")
