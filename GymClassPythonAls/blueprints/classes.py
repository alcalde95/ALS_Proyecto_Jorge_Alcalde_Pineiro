import flask
from model.User import User
from model.Clase import Clase
from model.Session import Session
import sirope
from flask import Blueprint, render_template, redirect, request
import flask_login
srp = sirope.Sirope()

classes_bp = Blueprint("classes", __name__,template_folder="templates")

@classes_bp.route("/classes", methods=["GET", "POST"])
@flask_login.login_required
def classes():
    if flask.request.method == "POST":
        nombre = flask.request.form.get("nombre")
        descripcion = flask.request.form.get("descripcion")
        capacidadMaxima = flask.request.form.get("capacidadMaxima")
        duracion = flask.request.form.get("duracion")
        creador = flask_login.current_user.email
        insert = True
        if not nombre or not descripcion or not capacidadMaxima or not duracion:
            flask.flash("Faltan campos por llenar")
            insert = False

        if not capacidadMaxima.isdigit():
            flask.flash("La capacidad máxima debe ser un número")
            insert = False
        if not duracion.isdigit():
            flask.flash("La duración debe ser un número")
            insert = False
        if len(descripcion) < 20:
            flask.flash("La duración debe ser mayor a 20 caracteres")
            insert = False
        if len(nombre) < 3:
            flask.flash("El nombre debe ser mayor a 3 caracteres")
            insert = False

        if not insert:
            return flask.redirect("/classes")


        clase = Clase(nombre, descripcion, capacidadMaxima, duracion, creador)

        srp.save(clase)

    clases = srp.load_all(Clase)

    toRet = {
        "clases": clases,
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("classes.html", **toRet)

@classes_bp.route("/classes/edit/<id>", methods=["GET", "POST"])
@flask_login.login_required
def edit_class(id):
    clase = srp.find_first(Clase, lambda c: c.id == id)

    if flask.request.method == "POST":
        nombre = flask.request.form.get("nombre")
        descripcion = flask.request.form.get("descripcion")
        capacidadMaxima = flask.request.form.get("capacidadMaxima")
        duracion = flask.request.form.get("duracion")

        if nombre:
            clase.nombre = nombre

        if descripcion:
            clase.descripcion = descripcion

        if capacidadMaxima:
            clase.capacidadMaxima = capacidadMaxima

        if duracion:
            clase.duracion = duracion

        srp.save(clase)
        return flask.redirect("/myClasses")
    toRet = {
        "clase": clase,
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("editClass.html", **toRet)

@classes_bp.route("/classes/delete/<id>", methods=["GET"])
@flask_login.login_required
def delete_class(id):
    clase = srp.find_first(Clase, lambda c: c.id == id)

    if clase.creador != flask_login.current_user.email:
        return flask.redirect("/")

    sessions = srp.filter(Session, lambda s: s.class_id == clase.id)
    for session in sessions:
        srp.delete(session.__oid__)

    srp.delete(clase.__oid__)
    return flask.redirect("/myClasses")

@classes_bp.route("/myClasses", methods=["GET"])
@flask_login.login_required
def myClasses():
    clases = srp.filter(Clase, lambda c: c.creador == flask_login.current_user.email)
    toRet = {
        "clases": clases,
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("myClasses.html", **toRet)

