from extensions import db 
from datetime import date

# db.Model tells SQLAlchemy that this py class is a table in the database
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    role = db.Column(db.String(20),nullable=False)
    # this column is to check if new user is approved to be staff by admin 
    approved = db.Column(db.Boolean,nullable=False,default=False)
    blacklisted = db.Column(db.Boolean, nullable=False, default=False)

class Trek(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    trek_name = db.Column(db.String(100),nullable=False)
    location = db.Column(db.String(100),nullable=False)
    difficulty = db.Column(db.String(20),nullable=False)
    duration = db.Column(db.Integer,nullable=False)
    available_slots = db.Column(db.Integer,nullable=False,default=0)
    status = db.Column(db.String(20),nullable=False,default="Pending")
    start_date = db.Column(db.Date,nullable=False)
    end_date = db.Column(db.Date,nullable=False)
    assigned_staff_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=True)

class Booking(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    trek_id=db.Column(db.Integer,db.ForeignKey("trek.id"),nullable=False)
    booking_date=db.Column(db.Date,nullable=False,default=date.today)
    status = db.Column(db.String(20),nullable=False,default="Booked")