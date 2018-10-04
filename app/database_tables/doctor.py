##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Doctors database table
# Holds all information about current doctors
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

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80))
    calendarID = db.Column(db.String(255))

    def __init__(self, firstname, lastname, email, calendarID):
        '''Initialize Doctor class'''
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.calendarID = calendarID

class DoctorSchema(ma.Schema):
    class Meta:
        '''Fields to expose'''
        fields = ('id', 'firstname', 'lastname', 'email', 'calendarID')
