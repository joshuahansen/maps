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

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Doctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))

    def __init__(self, id, firstname, lastname):
        '''Initialize Patient class'''
        self.id = id
        self.firstname = firstname
        self.lastname = lastname

class DoctorsSchema(ma.Schema):
    class Meta:
        '''Fields to expose'''
        fields = ('id', 'firstname', 'lastname')
