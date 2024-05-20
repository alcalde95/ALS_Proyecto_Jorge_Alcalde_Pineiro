import flask_login
import werkzeug.security as safe
import sirope

class User(flask_login.UserMixin):
    def __init__(self, email, password):
        self.__email = email
        self.__password = safe.generate_password_hash(password)

    @property
    def email(self):
        return self.__email

    def get_id(self):
        return self.__email

    def compara_password(self, password):
        return safe.check_password_hash(self.__password, password)

    @staticmethod
    def current_user():
        usr = flask_login.current_user

        if usr.is_anonymous:
            usr.logout_user()
            usr = None
        return usr

    @staticmethod
    def find(srp: sirope.Sirope, email: str) -> "User":
        return srp.find_first(User, lambda u: u.email == email)