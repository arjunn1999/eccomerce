from flask_sqlalchemy import SQLAlchemy
from market import db
from market import bcrypt
from market import login_manager
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    x=User.query.filter_by(id=int(user_id))
    if x:
        return x.first()
    else:
        return None


class Item(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    barcode = db.Column(db.String(50),nullable=False,unique=True)
    price = db.Column(db.Float(),nullable=False)
    description = db.Column(db.String(2000))
    owner = db.Column(db.Integer(),db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"{self.name}-{self.price}"

class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(50),unique=True,nullable=False)
    password_hash=db.Column(db.String(100),nullable=False)
    name = db.Column(db.String(20),nullable=False)
    items = db.relationship('Item',backref='owned_user',lazy=True)
    budget = db.Column(db.Float(),nullable=False,default=1000.0)
    @property
    def password(self):
        return self.password
    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
            return bcrypt.check_password_hash(self.password_hash,attempted_password)
    
    @property
    def prettier_budget(self):
        return "{:,}".format(self.budget)+" $"
    

    def __repr__(self):
        return f"{self.name}"

