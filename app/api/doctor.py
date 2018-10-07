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
from app.database_tables.doctor import Doctor, DoctorSchema

patient_schema = PatientSchema()
patient_schema = PatientSchema(many=True)
doctor_schema = DoctorSchema()
doctor_schema = DoctorSchema(many=True)

def get_patient(request):
    """Reads all patients for a particular ID.

    @param request is a single variable representing the patient ID.
    @return a json object containing all corresponding database records.

    """

    print("Calling API function doctor.get_patient(request).")

    response = None
    return response

def add_patient_note(request):
    """Adds a patient note for the particular patient ID.

    @param request is a json data structure with the following elements:
        test
    @return a json object containing success code and patient ID.
        
    """

    print("Calling API function doctor.add_patient_note(request).")

    response = None
    return response

def set_availability(request):
    """Updates the availability for a particular doctor ID.

    @param request is a json data structure with the following elements:
        test
    @return a json object containing success code and doctor ID.
        
    """

    print("Calling API function doctor.set_availability(request).")

    response = None
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
