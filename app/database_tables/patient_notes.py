##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Patient Notes database table
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

import MySQLdb.cursors
from app import app, db, ma

class PatientNotes(db.Model):
    '''
    Patient Notes stores notes and diagnoses for a patient
    '''
    __tablename__ = 'patientnotes'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    notes = db.Column(db.Text)
    diagnostics = db.Column(db.Text)

    def __init__(self, patient_id, notes, diagnostics):
        '''
        Constructor to initialize Patient notes class
        '''
        self.patient_id = patient_id
        self.notes = notes
        self.diagnostics = diagnostics

class PatientNotesSchema(ma.Schema):
    class Meta:
        '''
        Fields to expose
        '''
        fields = ('id', 'patient_id', 'notes', 'diagnostics')
