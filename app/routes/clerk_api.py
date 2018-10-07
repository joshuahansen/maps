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

@app.route('/api/clerk/add/', methods=['POST'])
def add_appointment():
    print("Calling endpoint /api/clerk/add.")
    return api.add_appointment(request)

@app.route('/api/clerk/get_by_id/', methods=['GET'])
def get_appointments_by_id():
    print("Calling endpoint /api/clerk/get_by_id.")
    return api.get_appointments_by_id(request.args.get('id'))

@app.route('/api/clerk/get_by_patient/', methods=['GET'])
def get_appointments_by_patient():
    print("Calling endpoint /api/clerk/get_by_patient.")
    return api.get_appointments_by_patient(request.args.get('patientID'))

@app.route('/api/clerk/get_by_doctor/', methods=['GET'])
def get_appointments_by_doctor():
    print("Calling endpoint /api/clerk/get_by_doctor.")
    return api.get_appointments_by_doctor(request.args.get('doctorID'))

@app.route('/api/clerk/delete/', methods=['DELETE'])
def delete_appointment():
    print("Calling endpoint /api/clerk/delete.")
    return api.delete_appointment(request.args.get('id'))

@app.route('/api/clerk/test/', methods=['GET'])
def clerk_api_test():
    print("Calling endpoint /api/clerk/test.")
    return api.test()
