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

@app.route('/api/clerk/', methods=['POST'])
def add_appointment():
    return api.add_appointment(request)

@app.route('/api/clerk/', methods=['POST'])
def get_appointments():
    if request.args.get('id'):
        return api.get_appointment_by_doctor(request.args.get('id'))
    elif request.args.get('patientID'):
        return api.get_appointment_by_doctor(request.args.get('patientID'))
    elif request.args.get('doctorID'):
        return api.get_appointment_by_doctor(request.args.get('doctorID'))

@app.route('/api/clerk/', methods=['DELETE'])
def delete_appointment():
    return api.delete_appointment(request)

@app.route('/test', methods=['GET'])
def test():
    return api.test()
