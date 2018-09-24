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

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientID = db.Column(db.Integer)
    DoctorID = db.Column(db.Integer)
    dateTime = db.Column(db.DateTime)

    def __init__(self, patientID, doctorID, dateTime):
        '''Initialize Patient class'''
        self.patientID = patientID
        self.doctorID = doctorID
        self.dateTime = dateTime

class AppointmentSchema(ma.Schema):
    class Meta:
        '''Fields to expose'''
        fields = ('id', 'patientID', 'doctorID', 'dateTime')
