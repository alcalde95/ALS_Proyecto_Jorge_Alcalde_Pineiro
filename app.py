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
    return flask.redirect("/login")

...

@app.route("/", methods=["GET", "POST"])
def land():
    print(flask_login.current_user)
    elem = {"user": flask_login.current_user, "isAunthenticated": flask_login.current_user.is_authenticated}
    return flask.render_template("index.html", **elem)


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
