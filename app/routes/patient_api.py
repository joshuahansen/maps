##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Pateint API Routes file - define all patient api routes for the flask app within this file
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

from flask import request

from app import app
from app.api import patient as api

@app.route('/api/patient/', methods=['GET'])
def get_all_patient():
    print(request.args)
    if request.args.get('id'):
        print("GET PATIENT")
        return api.get_patient(request.args.get('id'))
    else:
        print("GET ALL PATIENTS")
        return api.get_all_patients()

@app.route('/api/patient/', methods=['POST'])
def add_patient():
    print("ADD PATIENT")
    return api.add_patient(request)

@app.route('/api/patient/', methods=['DELETE'])
def delete_patient():
    print("DELETE PATIENT")
    return api.delete_patient(request.args.get('id'))

@app.route('/api/patient/', methods=['PUT'])
def update_patient():
    print("UPDATE PATIENT")
    return api.update_patient(request.args.get('id'), request.json)

@app.route('/test', methods=['GET'])
def test():
    return api.test()
