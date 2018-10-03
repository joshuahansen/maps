##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Clerk API Routes file - define all clerk API routes for the flask app within this file.
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

from flask import request
from app import app
from app.api import clerk as api

@app.route('/api/clerk/add', methods=['POST'])
def add_appointment():
    print("Calling endpoint /api/clerk/add.")
    return api.add_appointment(request)

@app.route('/api/clerk/get_by_id', methods=['GET'])
def get_appointments():
    print("Calling endpoint /api/clerk/get_by_id.")
    return api.get_appointment_by_id(request)

@app.route('/api/clerk/get_by_patient', methods=['GET'])
def get_appointments():
    print("Calling endpoint /api/clerk/get_by_patient.")
    return api.get_appointment_by_patient(request)

@app.route('/api/clerk/get_by_doctor', methods=['GET'])
def get_appointments():
    print("Calling endpoint /api/clerk/get_by_doctor.")
    return api.get_appointment_by_doctor(request)

@app.route('/api/clerk/delete', methods=['DELETE'])
def delete_appointment():
    print("Calling endpoint /api/clerk/delete.")
    return api.delete_appointment(request)

@app.route('/api/clerk/test', methods=['GET'])
def test():
    print("Calling endpoint /api/clerk/test.")
    return api.test()
