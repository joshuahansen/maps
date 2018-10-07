##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Doctors Availability database table
# Stores the Availability of each doctor
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

import MySQLdb.cursors
from app import app, db, ma

class DoctorAvailability(db.Model):
    __tablename__ = 'doctoravailability'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer)
    day = db.Column(db.Integer)
    startTime = db.Column(db.String(100))
    endTime = db.Column(db.String(100))

    def __init__(self, doctor_id, day, startTime, endTime):
        '''Initialize Doctor Availability class'''
        self.doctor_id = doctor_id
        self.day = day
        self.startTime = startTime
        self.endTime = endTime

class DoctorAvailabilitySchema(ma.Schema):
    class Meta:
        '''Fields to expose'''
        fields = ('id', 'doctor_id', 'day', 'startTime', 'endTime')
