##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Clerk API file, handles all interactions with the cloud.
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

import MySQLdb.cursors
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from httplib2 import Http

from app import app, db, ma
from app.database_tables.appointment import Appointment, AppointmentSchema
from app.database_tables.patient import Patient, PatientSchema
from app.database_tables.doctor import Doctor, DoctorSchema

appointment_schema = AppointmentSchema()
appointment_schema = AppointmentSchema(many=True)
patient_schema = PatientSchema()
patient_schema = PatientSchema(many=True)
doctor_schema = DoctorSchema()
doctor_schema = DoctorSchema(many=True)

def add_appointment(request):
    """Adds a new appointment to the calendar.
    
    @param request is a json data structure with the following elements:
        patientID
        doctorID
        startDateTime
        endDateTime
        summary
        location
        description
    @return a json object containing success code and patient ID.
        
    """

    print("Calling API function clerk.add_appointment(request).")

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('calendar-config.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    
    print("Building event details.")

    # Build event details.
    patientID = request.json['patientID']
    doctorID = request.json['doctorID']
    startDateTime = request.json['startDateTime']
    endDateTime = request.json['endDateTime']
    summary = request.json['summary']
    location = request.json['location']
    description = request.json['description']
    
    print("Getting doctor information from the database.")

    # Get doctor information from db.
    doctor = Doctor.query.filter_by(id=doctorID)
    doctor_result = doctor_schema.dump(doctor).data[0]
    
    print("Getting patient information from the database.")

    # Get patient information from db.
    patient = Patient.query.filter_by(id=patientID)
    patient_result = patient_schema.dump(patient).data[0]

    print("Building the event.")

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
                'email': doctor_result['email'],
                'email': patient_result['email']
            }
        ],
        'transparency': 'opaque'
    }

    print("Adding the appointment to the calendar.")

    # Add appointment to calendar.
    event = service.events().insert(calendarId=doctor_result['calendarID'], body=event).execute()
    print('Event created: {}'.format(event.get('htmlLink')))

    # Add appointment to table in database.
    new_appointment = Appointment(patientID, doctorID, time_start, time_end)
    db.session.add(new_appointment)
    db.session.commit()

    print("Done.")

    # Provide feedback to user.
    response = jsonify({"status": "Successful", "action": "make-appointment", "id": patientID})
    response.status_code = 200
    return response

def get_appointments_by_id(request):
    """Reads all appointments for a particular ID.

    @param request is a single variable representing the appointment ID.
    @return a json object containing all corresponding database records.

    """

    print("Calling API function clerk.get_appointments_by_id(request).")

    appointments = Appointment.query.filter_by(id=request)
    result = appointment_schema.dump(appointments)
    response = jsonify(result.data)
    response.status_code = 200
    return response

def get_appointments_by_patient(request):
    """Reads all appointments for a particular patient.

    @param request is a single variable representing the patient ID.
    @return a json object containing all corresponding database records.

    """

    print("Calling API function clerk.get_appointments_by_patient(request).")
    
    appointments = Appointment.query.filter_by(patientID=request)
    result = appointment_schema.dump(appointments)
    response = jsonify(result.data)
    response.status_code = 200
    return response

def get_appointments_by_doctor(request):
    """Reads all appointments for a particular doctor.

    @param request is a single variable representing the doctor ID.
    @return a json object containing all corresponding database records.

    """

    print("Calling API function clerk.get_appointments_by_doctor(request).")
    
    appointments = Appointment.query.filter_by(doctorID=request)
    result = appointment_schema.dump(appointments)
    response = jsonify(result.data)
    response.status_code = 200
    return response

def delete_appointment_by_id(request):
    """Deletes an appointment in the calendar.

    @param request is a single variable representing the appointment ID.
    @return a json object containing success code and appointment ID.

    """

    print("Calling API function clerk.delete_appointment_by_id(request).")
    
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
    """Tests the connection to this API.

    @param request is a single variable representing the appointment ID.
    @return a json object containing success code and message.

    """

    print("Calling API function clerk.test().")
    
    response = jsonify({"data": "Test API call without database"})
    response.status_code = 200
    return response

# Uncomment to delete all tables in database
#db.drop_all()

# Uncomment to add all tables to the database
#db.create_all()
