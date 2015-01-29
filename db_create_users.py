from project import db
from project.models import User

# insert data
db.session.add(User("erin", "shaw@isi.edu", "shaw"))
db.session.add(User("admin", "ad@min.com", "admin"))
db.session.add(User("zehui", "zehuizha@usc.edu", "zhang"))

# commit the changes
db.session.commit()
