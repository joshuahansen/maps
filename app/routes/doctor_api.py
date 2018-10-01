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

@app.route('/api/doctor/', methods=['GET'])
def read():
    return None

@app.route('/api/doctor/', methods=['PUT'])
def update():
    return None

@app.route('/test', methods=['GET'])
def test():
    return api.test()
