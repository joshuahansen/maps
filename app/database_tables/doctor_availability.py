##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Doctors Availability database table
# Stores the Availability of each doctor
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

class DoctorAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer)
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)

    def __init__(self, doctor_id, startDate, endDate):
        '''Initialize Doctor Availability class'''
        self.doctor_id = doctor_id
        self.startDate = startDate
        self.endDate = endDate

class DoctorAvailibalitySchema(ma.Schema):
    class Meta:
        '''Fields to expose'''
        fields = ('id', 'doctor_id', 'startDate', 'endDate')
