##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# This file initialises the flask server and provides
# a global variable 'app' for use in our project
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nashm, Zach Wingrave
##

from flask import Flask

app = Flask(__name__)

from app import routes
