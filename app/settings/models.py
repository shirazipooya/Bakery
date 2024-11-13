from app.db import BaseModel
from app.extensions import db
from flask_login import UserMixin

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