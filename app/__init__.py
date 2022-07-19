from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import random, string
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy()
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import User

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

def generate_random_code(N = 10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))