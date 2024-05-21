from model.User import User
import sirope
srp = sirope.Sirope()

usr = User("admin", "admin")
srp.save(usr)