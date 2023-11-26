from werkzeug.security import generate_password_hash
from app.models import User, File
from app import db, app

EMAIL = "XYZ@gmail.com"
PASSWORD = "12345"
NAME = "John Doe"

if __name__ == "__main__":
    # Use this to add new users if needed
    with app.app_context():
        u = User(email = EMAIL, password = generate_password_hash(PASSWORD), name = NAME)
        db.session.add(u)
        db.session.commit()