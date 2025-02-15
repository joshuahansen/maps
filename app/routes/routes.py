##
# Medical Appointment System (MAPS) - IoT Sem2 2018
#
# Routes file - define all routes for the flask app within this file
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nashm, Zach Wingrave
##

from flask import redirect, render_template

from app import app
from app import forms

@app.route('/')
@app.route('/index')
def index():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return forms.maps_register()

@app.route('/patient', methods=['GET', 'POST'])
def patient():
    return forms.maps_appointment(app.config)

@app.route('/patient/confirmation', methods=['GET', 'POST'])
def patient_confirmation():
    return forms.maps_appointment_confirmation(app.config)

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/clerk')
def clerk():
    return render_template('clerk.html')
