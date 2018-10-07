##
# Medical Appointment System (MAPS) - IoT Sem2 2018
#
# Forms file, handles form service requests
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nashm, Zach Wingrave
##

from flask import redirect, request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField,DateField,DateTimeField,SelectField
from wtforms.validators import Email,DataRequired

import requests
from datetime import datetime, timedelta

class AppointmentForm(FlaskForm):
    doctor = SelectField('Doctor', validators=[DataRequired()])
    date = DateTimeField('Desired Appointment Date', format='%d/%m/%Y')

class ApptWithTime(AppointmentForm):
    time = SelectField('Time', validators=[DataRequired()])


class MapsRegister(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    dob = DateField('Date of Birth', format='%d/%m/%Y')
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
    timeArr = []

    doctor_list = doctors_list(config['MAPS_API_BASE_URL'])

    form.doctor.choices = doctor_list

    if form.validate_on_submit():
        print("Valid")
        formwithtime = ApptWithTime()
        formwithtime.doctor.choices = doctor_list

        doctor = form.doctor.data
        date = form.date.data

        formwithtime.time.choices = times_list(config['MAPS_API_BASE_URL'], doctor, date)

        # Use values given to us previously
        formwithtime.doctor.default = doctor
        formwithtime.date.default = date

        # Disabled the fields above time
        formwithtime.doctor.render_kw={'readonly':''}
        formwithtime.date.render_kw={'readonly':''}

        return render_template('patient.html', form=formwithtime, action="/patient/confirmation")

    else:
        return render_template('patient.html', form=form)

def maps_appointment_confirmation(config):
    form = ApptWithTime()

    doctor_list = doctors_list(config['MAPS_API_BASE_URL'])
    form.doctor.choices = doctor_list

    doctor = form.doctor.data
    date = form.date.data

    time_list = times_list(config['MAPS_API_BASE_URL'], doctor, date)
    form.time.choices = time_list

    if form.validate_on_submit():


        # make the appointment
        appt_time = make_appointment(config['MAPS_API_BASE_URL'], form, time_list)

        return render_template('appt_confirmation.html', date=datetime.strftime(date, '%d/%m/%Y'), time=appt_time)

    for field in form:
        for error in field.errors:
            print(error)
    return "An error has occured."



# UTILS
def doctors_list(apiurl):
    r = requests.get(apiurl + "/patient/doctors/")

    doctor_list = []
    for doc in r.json():
        fullname = "{} {}".format(doc['firstname'], doc["lastname"])
        doctor_list.append((str(doc['id']), fullname))

    return doctor_list

def times_list(apiurl, doctor, date):
    appt_length = 30*60 # seconds
    time_list = []

    datestr = datetime.strftime(date, "%Y-%m-%d")
    r = requests.post(apiurl + "/patient/availability/", json={'doctorID': doctor, 'date': datestr})
    summary = r.json()

    day_start = summary['availability']['startTime']
    day_end = summary['availability']['endTime']

    start_hr,start_min = map(int, day_start.split(':'))
    end_hr,end_min = map(int, day_end.split(':'))

    seconds_avail = (int(end_hr) - int(start_hr)) * 60 * 60 + (int(end_min) - int(start_min)) * 60
    possible_slots = int(seconds_avail / appt_length)

    startTime = date + timedelta(seconds=start_hr*60*60 + start_min*60)

    for i in range(0, possible_slots):
        appt_time = startTime + timedelta(seconds=i * appt_length)
        time_list.append((str(i), appt_time.strftime('%H:%M')))

    print(time_list)

    return time_list

def make_appointment(apiurl, form, time_list):
    doctor = form.doctor.data
    date = form.date.data.date() # no time please
    selected_slot = int(form.time.data)

    starttime = time_list[selected_slot][1]
    endtime = time_list[selected_slot+1][1]

    payload = {
        'patient': 1,
        'startDate': '{}T{}:00'.format(date, starttime),
        'endDate': '{}T{}:00'.format(date, endtime),
        'doctor': 1,
        'description': 'test',
        'summary': 'test',
        'location': 'loc'
    }
    r = requests.post("http://localhost:5000/api/patient/make-appointment/", json=payload)

    return starttime
