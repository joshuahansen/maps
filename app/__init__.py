##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# This file initialises the flask server and provides
# a global variable 'app' for use in our project
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nashm, Zach Wingrave
##

from flask import Flask
import configparser
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

if 'gcpMySQL' in config:
    HOST = config['gcpMySQL']['host']
    USER = config['gcpMySQL']['user']
    PASS = config['gcpMySQL']['pass']
    DBNAME = config['gcpMySQL']['db']

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.routes import routes, patient_api, doctor_api
