##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Patient Notes database table
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

class PatientNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.Text)
    diagnostics = db.Column(db.Text)

    def __init__(self, id, notes, diagnostics):
        '''Initialize Patient class'''
        self.id = id
        self.notes = notes
        self.diagnostics = diagnostics

class PatientNotesSchema(ma.Schema):
    class Meta:
        '''Fields to expose'''
        fields = ('id', 'notes', 'diagnostics')
