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
from app.database_tables.doctor import Doctor, DoctorSchema
from app.database_tables.patient import Patient, PatientSchema
from app.database_tables.patient_notes import PatientNotes, PatientNotesSchema
from app.database_tables.doctor_availability import DoctorAvailability, DoctorAvailabilitySchema

doctor_schema = DoctorSchema()
doctor_schema = DoctorSchema(many=True)
patient_schema = PatientSchema()
patient_schema = PatientSchema(many=True)
patient_notes_schema = PatientNotesSchema()
patient_notes_schema = PatientNotesSchema(many=True)
doctor_availability_schema = DoctorAvailabilitySchema()
doctor_availability_schema = DoctorAvailabilitySchema(many=True)

def get_doctor(request):
    """Reads a particular doctor for a particular ID.

    @param request is a single variable representing the doctor ID.
    @return a json object containing all corresponding database records.

    """

    print("Calling API function doctor.get_doctor(request).")

    doctor = Doctor.query.filter_by(id=request)
    result = doctor_schema.dump(doctor)
    response = jsonify(result.data)
    response.status_code = 200
    return response

def get_all_doctors():
    """Reads all doctors from the database.

    @return a json object containing all corresponding database records.

    """

    print("Calling API function doctor.get_all_doctors().")

    doctor = Doctor.query.all()
    result = doctor_schema.dump(doctor)
    response = jsonify(result.data)
    response.status_code = 200
    return response

def get_patient(request):
    """Reads a particular patient for a particular ID.

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
        doctor_id
        day
        startTime
        endTime
    @return a json object containing success code and doctor ID.
        
    """

    print("Calling API function doctor.set_availability(request).")

    # Build availability details.
    doctor_id = request.json['doctor_id']
    day = request.json['day']
    startTime = request.json['startTime']
    endTime = request.json['endTime']

    # Add availability to table in database.
    results = DoctorAvailability.query.filter_by(doctor_id=doctor_id, day=day)
    if results.count() <= 0:
        new_availability = DoctorAvailability(doctor_id, day, startTime, endTime)
        db.session.add(new_availability)
    else:
        results.update(request.json)
    db.session.commit()

    # Provide feedback to user.
    response = jsonify({"status": "Successful", "action": "set-availability", "id": doctor_id})
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
