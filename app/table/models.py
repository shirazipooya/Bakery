from app.db import BaseModel
from app.extensions import db
from flask_login import UserMixin


class Bakery(BaseModel, UserMixin):
    
    first_name = db.Column(db.String(30), unique=False, nullable=True)
    last_name = db.Column(db.String(30), unique=False, nullable=True)
    nid = db.Column(db.String(10), unique=False, nullable=True)
    phone = db.Column(db.String(11), unique=False, nullable=True)
    bakery_id = db.Column(db.String(30), unique=False, nullable=True)
    ownership_status = db.Column(db.String(30), unique=False, nullable=True)
    number_violations = db.Column(db.Integer, unique=False, nullable=True)
    second_fuel = db.Column(db.String(30), unique=False, nullable=True)
    ostan = db.Column(db.String(30), unique=False, nullable=True)
    shahrestan = db.Column(db.String(30), unique=False, nullable=True)
    bakhsh = db.Column(db.String(30), unique=False, nullable=True)
    shahr = db.Column(db.String(30), unique=False, nullable=True)
    city = db.Column(db.String(30), unique=False, nullable=True)
    region = db.Column(db.Integer, unique=False, nullable=True)
    district = db.Column(db.Integer, unique=False, nullable=True)
    lat = db.Column(db.Float, unique=False, nullable=False)
    lon = db.Column(db.Float, unique=False, nullable=False)
    household_risk = db.Column(db.String(30), unique=False, nullable=True)
    bakers_risk = db.Column(db.String(30), unique=False, nullable=True)
    flour_types = db.Column(db.String(30), unique=False, nullable=True)
    bread_types = db.Column(db.String(30), unique=False, nullable=True)
    bread_rations = db.Column(db.Integer, unique=False, nullable=True)    
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.first_name}, {self.last_name}, {self.nid}, {self.bread_types}, {self.bread_rations})'



class OwnershipStatus(BaseModel):
    name = db.Column(db.String(60), unique=True, nullable=False)
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name})'

class SecondFuel(BaseModel):
    name = db.Column(db.String(60), unique=True, nullable=False)
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name})'

class HouseholdRisk(BaseModel):
    name = db.Column(db.String(60), unique=True, nullable=False)
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name})'

class BakersRisk(BaseModel):
    name = db.Column(db.String(60), unique=True, nullable=False)
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name})'

class TypeFlour(BaseModel):
    name = db.Column(db.String(60), unique=True, nullable=False)
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name})'

class TypeBread(BaseModel):
    name = db.Column(db.String(60), unique=True, nullable=False)
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name})'