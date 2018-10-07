##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Doctor API Routes file - define all doctor API routes for the flask app within this file.
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

from flask import request
from app import app
from app.api import doctor as api

@app.route('/api/doctor/get_doctor/', methods=['GET'])
def get_doctor():
    print("Calling endpoint /api/doctor/get_doctor.")
    return api.get_doctor(request.args.get('id'))

@app.route('/api/doctor/get_all_doctors/', methods=['GET'])
def get_all_doctors():
    print("Calling endpoint /api/doctor/get_all_doctors.")
    return api.get_all_doctors()

@app.route('/api/doctor/get_patient/', methods=['GET'])
def get_patient():
    print("Calling endpoint /api/doctor/get_patient.")
    return api.get_patient(request.args.get('id'))

@app.route('/api/doctor/add_note/', methods=['POST'])
def add_note():
    print("Calling endpoint /api/doctor/add_note.")
    return api.add_patient_note(request)

@app.route('/api/doctor/set_availability/', methods=['POST'])
def set_availability():
    print("Calling endpoint /api/doctor/set_availability.")
    return api.set_availability(request)

@app.route('/api/doctor/test/', methods=['GET'])
def doctor_api_test():
    print("Calling endpoint /api/doctor/test.")
    return api.test()
