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
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
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

if 'googleCalendar' in config:
    mapsCalendarID = config['googleCalendar']['calendarID']

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

def make_appointment(request):
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('calendar-config.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    
    '''Add  a new patient to the database'''
    patientID = request.json['patientid']
    startDate = request.json['startDate']
    endDate = request.json['endDate']
    doctor = request.json['doctor']
    description = request.json['description']
    summary = request.json['summary']
    location = request.json['location']

    time_start = "{}".format(startDate)
    time_end   = "{}".format(endDate)
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': time_start,
            'timeZone': 'Australia/Melbourne',
        },
        'end': {
            'dateTime': time_end,
            'timeZone': 'Australia/Melbourne',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 5},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'attendees': [
            {'email': doctor}
        ]
    }
    event = service.events().insert(calendarId=mapsCalendarID, body=event).execute()
    print('Event created: {}'.format(event.get('htmlLink')))

    response = jsonify({"status": "Successful", "action": "make-appointment", "id": patientID})
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
