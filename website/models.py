from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    Len = db.Column(db.String(4))  # Assuming this stores a student's length or ID
    password = db.Column(db.String(150))
    
    # Defining the relationship to Clothdetails model
    clothdetails = db.relationship("Clothdetails", backref="student", lazy=True)

class Clothdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kurta = db.Column(db.Integer, default=0)
    pajama = db.Column(db.Integer, default=0)
    shirt = db.Column(db.Integer, default=0)
    tshirt = db.Column(db.Integer, default=0)
    pant = db.Column(db.Integer, default=0)
    lower = db.Column(db.Integer, default=0)
    shorts = db.Column(db.Integer, default=0)
    bedsheet = db.Column(db.Integer, default=0)
    pillowcover = db.Column(db.Integer, default=0)
    towel = db.Column(db.Integer, default=0)
    duppata = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20))
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)




