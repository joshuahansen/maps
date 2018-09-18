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

@app.route('/api/patient/', methods=['GET'])
def get_all_patient():
    print(request.args)
    if request.args.get('id'):
        print("GET PATIENT")
        return patient_api.get_patient(request.args.get('id'))
    else:
        print("GET ALL PATIENTS")
        return patient_api.get_all_patients()

@app.route('/api/patient/', methods=['POST'])
def add_patient():
    print("ADD PATIENT")
    return patient_api.add_patient(request)

@app.route('/api/patient/', methods=['DELETE'])
def delete_patient():
    print("DELETE PATIENT")
    return patient_api.delete_patient(request.args.get('id'))

@app.route('/api/patient/', methods=['PUT'])
def update_patient():
    print("UPDATE PATIENT")
    return patient_api.update_patient(request.args.get('id'), request.json)
