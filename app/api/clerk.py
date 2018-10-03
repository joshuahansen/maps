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
from app.database_tables.appointment import Appointment, AppointmentSchema
from app.database_tables.patient import Patient, PatientSchema
from app.database_tables.doctor import Doctor, DoctorSchema

config = configparser.ConfigParser()
config.read('config.ini')

appointment_schema = AppointmentSchema()
appointment_schema = AppointmentSchema(many=True)
patient_schema = PatientSchema()
patient_schema = PatientSchema(many=True)
doctor_schema = DoctorSchema()
doctor_schema = DoctorSchema(many=True)

if 'gcpMySQL' in config:
    HOST = config['gcpMySQL']['host']
    USER = config['gcpMySQL']['user']
    PASS = config['gcpMySQL']['pass']
    DBNAME = config['gcpMySQL']['db']

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME)

db = SQLAlchemy(app)
ma = Marshmallow(app)

def add_appointment(request):
    """Adds a new appointment to the calendar."""

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('calendar-config.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    
    # Build event details.
    patientID = request.json['patientID']
    doctorID = request.json['doctorID']
    startDateTime = request.json['startDateTime']
    endDateTime = request.json['endDateTime']
    summary = request.json['summary']
    location = request.json['location']
    description = request.json['description']
    
    # Get doctor information from db.
    doctor = Doctor.query.filter_by(id=doctorID)
    doctor_result = doctor_schema.dump(doctor)
    
    # Get patient information from db.
    patient = Patient.query.filter_by(id=patientID)
    patient_result = patient_schema.dump(patient)

    time_start = "{}".format(startDateTime)
    time_end   = "{}".format(endDateTime)
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
            {
                'email': doctor_result.email,
                'email': patient_result.email
            }
        ],
        'transparency': 'opaque'
    }

    # Add appointment to calendar.
    event = service.events().insert(calendarId=doctor_result.calendarID, body=event).execute()
    print('Event created: {}'.format(event.get('htmlLink')))

    # Add appointment to table in database.
    new_appointment = Appointment(patientID, doctorID, startDate, endDate)
    db.session.add(new_appointment)
    db.session.commit()

    # Provide feedback to user.
    response = jsonify({"status": "Successful", "action": "make-appointment", "id": patientID})
    response.status_code = 200
    return response

# def get_appointments_master(request):
#     """Gets appointments specified by request parameters."""
#     response.status_code = 200
#     return response

def get_appointments_by_id(request):
    """Reads all future appointments in the calendar."""

    appointments = Appointment.query.filter_by(id=request)
    result = appointment_schema.dump(appointments)
    response = jsonify(result.data)
    response.status_code = 200
    return response

def get_appointments_by_patient(request):
    """Reads all appointments for a particular patient."""
    
    appointments = Appointment.query.filter_by(patientID=request)
    result = appointment_schema.dump(appointments)
    response = jsonify(result.data)
    response.status_code = 200
    return response

def get_appointments_by_doctor(request):
    """Reads all future appointments in the calendar."""
    
    appointments = Appointment.query.filter_by(doctorID=request)
    result = appointment_schema.dump(appointments)
    response = jsonify(result.data)
    response.status_code = 200
    return response

def delete_appointment_by_id(request):
    """Deletes an appointment in the calendar."""
    
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('calendar-config.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Delete event from calendar.
    service.events().delete(calendarId='primary', eventId=request).execute()

    # Delete appointment from table in database.
    Appointment.query.filter_by(id=request).delete()
    db.session.commit()
    
    # Provide feedback to user.
    response = jsonify({"status": "Successful", "action": "delete", "id": request})
    response.status_code = 200
    return response

def test():
    """Tests the connection to this API."""
    
    response = jsonify({"data": "Test API call without database"})
    response.status_code = 200
    return response

# Uncomment to delete all tables in database
#db.drop_all()

# Uncomment to add all tables to the database
#db.create_all()
