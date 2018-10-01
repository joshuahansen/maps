##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Clerk API file, handles all interactions with the cloud.
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

import configparser
import MySQLdb.cursors
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import app
from app.database_tables.patient import Patient, PatientSchema

config = configparser.ConfigParser()
config.read('config.ini')

patient_schema = PatientSchema()

if 'gcpMySQL' in config:
    HOST = config['gcpMySQL']['host']
    USER = config['gcpMySQL']['user']
    PASS = config['gcpMySQL']['pass']
    DBNAME = config['gcpMySQL']['db']

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME)

db = SQLAlchemy(app)
ma = Marshmallow(app)

def read_patient(patient):
    """Reads all future appointments in the calendar."""
    response = None
    return response

def update_patient(patient, update):
    """Updates an appointment in the calendar."""
    response = None
    return response

def test():
    response = jsonify({"data": "Test API call without database"})
    response.status_code = 200
    return response

# Uncomment to delete all tables in database
#db.drop_all()

# Uncomment to add all tables to the database
#db.create_all()
