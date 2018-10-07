##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Patient database table
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

import MySQLdb.cursors
from app import app, db, ma

class Patient(db.Model):
    '''
    Patient Class stores all relevant details for the patient
    in the database
    '''
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(80))
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(20))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(80))
    postcode = db.Column(db.String(10))

    def __init__(self, firstname, lastname, phone, email,
                    gender, dob, address, city, state, postcode):
        '''
        Constructor to initialize Patient class
        '''
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email
        self.gender = gender
        self.dob = dob
        self.address = address
        self.city = city
        self.state = state
        self.postcode = postcode

class PatientSchema(ma.Schema):
    class Meta:
        '''
        Fields to expose
        '''
        fields = ('id', 'firstname', 'lastname', 'phone', 'email',
            'gender', 'dob', 'address', 'city', 'state', 'postcode')
