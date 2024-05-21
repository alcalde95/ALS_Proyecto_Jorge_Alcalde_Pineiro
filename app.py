import flask
import json
import sirope
import flask_login
from model.User import User
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
    return flask.redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
