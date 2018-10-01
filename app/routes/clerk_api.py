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
def create():
    return None

@app.route('/api/clerk/', methods=['GET'])
def read():
    return None

@app.route('/api/clerk/', methods=['PUT'])
def update():
    return None
    # Needed?

@app.route('/api/clerk/', methods=['DELETE'])
def delete():
    return None

@app.route('/test', methods=['GET'])
def test():
    return api.test()
