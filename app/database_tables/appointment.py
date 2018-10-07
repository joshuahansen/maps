##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Appointments database table
# Holds a record of all appointments booked
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

import MySQLdb.cursors
from app import app, db, ma

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patientID = db.Column(db.Integer)
    doctorID = db.Column(db.Integer)
    startDateTime = db.Column(db.DateTime)
    endDateTime = db.Column(db.DateTime)

    def __init__(self, patientID, doctorID, startDate, endDate):
        '''Initialize Appointment class'''
        self.patientID = patientID
        self.doctorID = doctorID
        self.startDateTime = startDate
        self.endDateTime = endDate

class AppointmentSchema(ma.Schema):
    class Meta:
        '''Fields to expose'''
        fields = ('id', 'patientID', 'doctorID', 'startDateTime', 'endDateTime')
