##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Doctors database table
# Holds all information about current doctors
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

import MySQLdb.cursors
from app import app, db, ma

class Doctor(db.Model):
    '''
    Doctor class to store doctor information in the database
    '''
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80))
    calendarID = db.Column(db.String(255))

    def __init__(self, firstname, lastname, email, calendarID):
        '''
        Constructor to initialize Doctor class
        '''
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.calendarID = calendarID

class DoctorSchema(ma.Schema):
    class Meta:
        '''
        Fields to expose
        '''
        fields = ('id', 'firstname', 'lastname', 'email', 'calendarID')
