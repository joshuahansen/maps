##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Patient API file, handels all interactions with the cloud
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

from flask import request, jsonify
import configparser
import MySQLdb.cursors
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import app
from app.database_tables.patient import Patient, PatientSchema


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

patient_schema = PatientSchema()
patient_schema = PatientSchema(many=True)

def get_patient(patient_id):
    '''Return a patient's data in JSON format'''
    patient = Patient.query.filter_by(id=patient_id)

    result = patient_schema.dump(patient)

    response = jsonify(result.data)
    response.status_code = 200
    return response

def get_all_patients():
    '''Return all patient's data in JSON format'''
    all_patients = Patient.query.all()
    result = patient_schema.dump(all_patients)
    
    response = jsonify(result.data)
    response.status_code = 200
    return response

def add_patient(request):
    '''Add  a new patient to the database'''
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    phone = request.json['phone']
    email = request.json['email']
    gender = request.json['gender']
    dob = request.json['dob']
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    postcode = request.json['postcode']

    new_patient = Patient(firstname, lastname, phone, email,
                    gender, dob, address, city, state, postcode)

    db.session.add(new_patient)
    db.session.commit()

    response = jsonify({"status": "Successful", "action": "add"})
    response.status_code = 200

    return response
    
def update_patient(patient_id, data):
    '''Update a current patients data'''
    Patient.query.filter_by(id=patient_id).update(data)

    db.session.commit()


    response = jsonify({"status": "Successful", "action": "update", "id": patient_id})
    response.status_code = 200

    return response

def delete_patient(patient_id):
    '''Delete a patient from the database'''
    Patient.query.filter_by(id=patient_id).delete()
    
    db.session.commit()
    
    response = jsonify({"status": "Successful", "action": "delete", "id": patient_id})
    response.status_code = 200

    return response

def test():
    response = jsonify({"data": "Test API call without database"})
    response.status_code = 200
    return response
# Uncomment to delete all tables in database
#db.drop_all()

# Uncomment to add all tables to the database
#db.create_all()
