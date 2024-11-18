from app.db import BaseModel
from app.extensions import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(BaseModel, UserMixin):
    first_name = db.Column(db.String(30), unique=False, nullable=False)
    last_name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    role = db.Column(db.String(30), unique=False, nullable=False)
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.id}, {self.username})'