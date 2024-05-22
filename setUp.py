from model.User import User
from model.Clase import Clase
from model.Session import Session
from model.Inscription import Inscription
import sirope
srp = sirope.Sirope()

usr = User("admin", "admin")
srp.save(usr)
usr = User("test@test.test", "test1234")
srp.save(usr)
usr = User("test2@test.test", "test1234")
srp.save(usr)

clase = Clase("Clase de prueba test", "Esta es una clase de muestra básica", 10, 60, "test@test.test")
srp.save(clase)
session = Session(clase.id, "2024-06-01T10:00", "test@test.test")
srp.save(session)
session2 = Session(clase.id, "2024-06-01T10:00", "test2@test.test")
srp.save(session)

insc = Inscription(clase.id,session.date,session.instructor,"test2@test.test")
srp.save(insc)
