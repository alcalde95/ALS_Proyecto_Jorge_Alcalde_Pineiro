import flask
import json
import sirope
from datetime import datetime
import flask_login
from model.User import User
from model.Clase import Clase
from model.Session import Session
from blueprints.users import users_bp
from blueprints.classes import classes_bp
from blueprints.sessions import sessions_bp
def create_app():
    flapp = flask.Flask(__name__)
    lmanager = flask_login.login_manager.LoginManager()
    sirp = sirope.Sirope()

    flapp.config.from_file("cfg/config.json", load=json.load)
    lmanager.init_app(flapp)
    return flapp, lmanager, sirp


app, lm, srp = create_app()

app.register_blueprint(users_bp)
app.register_blueprint(classes_bp)
app.register_blueprint(sessions_bp)
# ver los blueprints en la documentación de Flask
# app/
# usuario : añadir,borrar,modificar -> 1 blueprint
# libros: añadir,borrar,modificar -> 1 blueprint
# El tema 16 es sobre bootstrap. Se puede usar algún framework
@lm.user_loader
def user_loader(id: str) -> User:
    return User.find(srp, id)


...


@lm.unauthorized_handler
def unauthorized():
    flask.flash("usuario no autorizado")
    flask.redirect("/")


...


@app.route("/", methods=["GET", "POST"])
def land():
    print(flask_login.current_user)
    elem = {"user": flask_login.current_user, "isAunthenticated": flask_login.current_user.is_authenticated}
    return flask.render_template("index.html", **elem)

'''
@app.route("/login", methods=["GET", "POST"])
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

'''
'''
@app.route("/register", methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        email = flask.request.form.get("email")
        pswd = flask.request.form.get("pswd")
        pswd2 = flask.request.form.get("pswd2")
        if not email or not pswd or not pswd2:
            flask.flash("Faltan campos por llenar")
            return flask.redirect("/register")
        if pswd != pswd2:
            flask.flash("contraseñas no coinciden")
            return flask.redirect("/register")
        exists = srp.find_first(User, lambda u: u.email == email)
        if exists is not None:
            flask.flash("usuario ya registrado")
            return flask.redirect("/register")


        usr = User(email, pswd)
        srp.save(usr)
        return flask.redirect("/login")
    return flask.render_template("register.html")

'''
@app.route("/admin", methods=["GET"])
@flask_login.login_required
def admin():
    if flask_login.current_user.email != 'admin':
        return flask.redirect("/")
    toRet = {
        "users": srp.filter(User, lambda c: c.email != 'admin'),
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("admin.html", **toRet)
'''@app.route("/users/delete/<email>", methods=["GET"])
@flask_login.login_required
def delete_user(email):
    if flask_login.current_user.email != 'admin':
        return flask.redirect("/")
    user = srp.find_first(User, lambda c: c.email == email)
    srp.delete(user.__oid__)

    classes = srp.filter(Clase, lambda c: c.creador == email)

    for clase in classes:
        srp.delete(clase.__oid__)
    return flask.redirect("/admin")'''

'''@app.route("/classes", methods=["GET", "POST"])
@flask_login.login_required
def classes():
    if flask.request.method == "POST":
        nombre = flask.request.form.get("nombre")
        descripcion = flask.request.form.get("descripcion")
        capacidadMaxima = flask.request.form.get("capacidadMaxima")
        duracion = flask.request.form.get("duracion")
        creador = flask_login.current_user.email

        if not nombre or not descripcion or not capacidadMaxima or not duracion:
            flask.flash("Faltan campos por llenar")
            return flask.redirect("/classes")

        clase = Clase(nombre, descripcion, capacidadMaxima, duracion, creador)

        srp.save(clase)

    clases = srp.load_all(Clase)

    toRet = {
        "clases": clases,
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("classes.html", **toRet)'''
##añadir y visualizar sessiones
'''@app.route("/classes/<id>", methods=["GET","POST"])
@flask_login.login_required
def class_sessions(id):
    if flask.request.method == "POST":
        print("entro")
        date = flask.request.form.get("date")
        instructor = flask.request.form.get("instructor")
        print(date)
        print(instructor)
        if not date or not instructor:
            flask.flash("Faltan campos por llenar")
            return flask.redirect("/classes/" + id)

        session = Session(id, date, instructor)
        print(session)
        srp.save(session)
    clase = srp.find_first(Clase, lambda c: c.id == id)
    sessions = srp.filter(Session, lambda s: s.class_id == id)
    print(sessions)
    toRet = {
        "clase": clase,
        "sessions":sessions,
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("classSessions.html", **toRet)
'''
'''@app.route("/classes/edit/<id>", methods=["GET", "POST"])
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
    return flask.render_template("editClass.html", **toRet)'''


'''@app.route("/classes/delete/<id>", methods=["GET"])
@flask_login.login_required
def delete_class(id):
    clase = srp.find_first(Clase, lambda c: c.id == id)
    srp.delete(clase.__oid__)
    return flask.redirect("/myClasses")
'''

'''@app.route("/myClasses", methods=["GET"])
@flask_login.login_required
def myClasses():
    clases = srp.filter(Clase, lambda c: c.creador == flask_login.current_user.email)
    toRet = {
        "clases": clases,
        "user": flask_login.current_user,
        "isAunthenticated": flask_login.current_user.is_authenticated
    }
    return flask.render_template("myClasses.html", **toRet)

'''
@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

# TODO: AÑADIR comprobación de datos en los formularios
