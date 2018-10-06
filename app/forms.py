##
# Medical Appointment System (MAPS) - IoT Sem2 2018
#
# Forms file, handles form service requests
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nashm, Zach Wingrave
##

from flask import redirect, request, render_template

from flask_wtf import FlaskForm
from wtforms import DateField,SelectField
from wtforms.validators import DataRequired

import requests

class AppointmentForm(FlaskForm):

    doctor = SelectField('Doctor',
        validators=[DataRequired()]
    )
    date = DateField('Desired Appointment Date', format='%d/%m/%Y')

class MapsRegister(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    dob = DateTimeField('Date of Birth', format='%d/%m/%Y')
    gender = SelectField('Gender',
        validators=[DataRequired()],
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ]
    )
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State',
        validators=[DataRequired()],
        choices=[
            ('vic', 'VIC'),
            ('nsw', 'NSW'),
            ('act', 'ACT'),
            ('qld', 'QLD'),
            ('nt', 'NT'),
            ('wa', 'WA'),
            ('sa', 'SA'),
            ('tas', 'TAS')
        ]
    )
    postcode = StringField('Post Code', validators=[DataRequired()])

def maps_register():
    form = MapsRegister()

    if form.validate_on_submit():
        return redirect("/patient")

    return render_template('maps_register.html', form=form)

def maps_appointment(config):
    form = AppointmentForm()

    form.doctor.choices = doctors_list(config['MAPS_API_BASE_URL'])

    if form.validate_on_submit():
        return "Valid"

    return render_template('patient.html', form=form)

# UTILS
def doctors_list(apiurl):
    r = requests.get(apiurl + "/patient/doctors/")

    doctor_list = []
    for doc in r.json():
        fullname = "{} {}".format(doc['firstname'], doc["lastname"])
        doctor_list.append((doc['id'], fullname))

    return doctor_list
