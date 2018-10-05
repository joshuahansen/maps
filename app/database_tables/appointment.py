##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Appointments database table
# Holds a record of all appointments booked
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

import configparser
import MySQLdb.cursors
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import app

config = configparser.ConfigParser()
config.read('config.ini')

if 'gcpMySQL' in config:
    HOST = config['gcpMySQL']['host']
    USER = config['gcpMySQL']['user']
    PASS = config['gcpMySQL']['pass']
    DBNAME = config['gcpMySQL']['db']

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Appointment(db.Model):
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
        seld.endDateTime = endDate

class AppointmentSchema(ma.Schema):
    class Meta:
        '''Fields to expose'''
        fields = ('id', 'patientID', 'doctorID', 'startDateTime', 'endDateTime')
