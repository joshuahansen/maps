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
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)

    def __init__(self, doctor_id, startDate, endDate):
        '''Initialize Doctor Availability class'''
        self.doctor_id = doctor_id
        self.startDate = startDate
        self.endDate = endDate

class DoctorAvailabilitySchema(ma.Schema):
    class Meta:
        '''Fields to expose'''
        fields = ('id', 'doctor_id', 'startDate', 'endDate')
