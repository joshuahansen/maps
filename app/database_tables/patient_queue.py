##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Patient Queue database table
# Stores patients when they arrive.
# Doctors query to get next patient
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

import MySQLdb.cursors
from app import app, db, ma

class PatientQueue(db.Model):
    __tablename__ = 'patientqueue'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    arrival = db.Column(db.DateTime)

    def __init__(self, patient_id, arrival):
        '''Initialize Patient queue class'''
        self.patient_id = patient_id
        self.arrival = arrival

class PatientQueueSchema(ma.Schema):
    class Meta:
        '''Fields to expose'''
        fields = ('id', 'patient_id', 'arrival')
