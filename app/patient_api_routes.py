##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Routes file - define all routes for the flask app within this file
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nashm, Zach Wingrave
##

from flask import request

from app import app
from app import patient_api

@app.route('/api/patient', methods=['GET'])
def get_all_patient():
    return patient_api.get_all_patients()

@app.route('/api/patient', methods=['POST'])
def add_patient():
    return patient_api.add_patient(request)
