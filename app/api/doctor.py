##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Doctor API file, handles all interactions with the cloud.
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

import MySQLdb.cursors
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from app import app, db, ma
from app.database_tables.patient import Patient, PatientSchema
from app.database_tables.doctor_availability import DoctorAvailability, DoctorAvailabilitySchema

patient_schema = PatientSchema()
patient_schema = PatientSchema(many=True)
doctor_availability_schema = DoctorAvailabilitySchema()
doctor_availability_schema = DoctorAvailabilitySchema(many=True)

def get_patient(request):
    """Reads all patients for a particular ID.

    @param request is a single variable representing the patient ID.
    @return a json object containing all corresponding database records.

    """

    print("Calling API function doctor.get_patient(request).")

    patient = Patient.query.filter_by(id=request)
    result = patient_schema.dump(patient)
    response = jsonify(result.data)
    response.status_code = 200
    return response

def add_patient_note(request):
    """Adds a patient note for the particular patient ID.

    @param request is a json data structure with the following elements:
        patientID
        notes
        diagnoses
    @return a json object containing success code and patient ID.
        
    """

    print("Calling API function doctor.add_patient_note(request).")

    # Build note details.
    patientID = request.json['patientID']
    notes = request.json['notes']
    diagnoses = request.json['diagnoses']

    # Add note to table in database.
    new_note = PatientNotes(patientID, notes, diagnoses)
    db.session.add(new_note)
    db.session.commit()

    # Provide feedback to user.
    response = jsonify({"status": "Successful", "action": "add-note", "id": patientID})
    response.status_code = 200
    return response

def set_availability(request):
    """Sets the availability for a particular doctor ID for a particular day.

    @param request is a json data structure with the following elements:
        doctorID
        day
        startTime
        endTime
    @return a json object containing success code and doctor ID.
        
    """

    print("Calling API function doctor.set_availability(request).")

    # Build availability details.
    doctorID = request.json['doctorID']
    day = request.json['day']
    startTime = request.json['startTime']
    endTime = request.json['endTime']

    # Add availability to table in database.
    new_note = DoctorAvailability(doctorID, day, startTime, endTime)
    db.session.update(new_note).where(day=day)
    db.session.commit()

    # Provide feedback to user.
    response = jsonify({"status": "Successful", "action": "set-availability", "id": doctorID})
    response.status_code = 200
    return response

def test():
    """Tests the connection to this API.

    @param request is a single variable representing the appointment ID.
    @return a json object containing success code and message.

    """

    print("Calling API function doctor.test().")

    response = jsonify({"data": "Test API call without database"})
    response.status_code = 200
    return response

# Uncomment to delete all tables in database
#db.drop_all()

# Uncomment to add all tables to the database
#db.create_all()
