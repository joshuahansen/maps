##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Forms file, handles form service requests
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nashm, Zach Wingrave
##

from flask import request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField,DateTimeField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Email

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

class MapsBookings(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    date = DateTimeField('Appointment Date', format='%d/%m/%Y')
    doctor = SelectField('Doctor',
        validators=[DataRequired()],
        choices=[
            ('J Smith', 'Dr. J. Smith'),
            ('J Doe', 'Dr. J. Doe'),
            ('S Hawkings', 'Dr. S. Hawkings')
        ]
    )
    reason = TextAreaField('Reason for Visit')

def maps_register():
    form = MapsRegister()
    
    if form.validate_on_submit():
        return "<h2>Registered Successfully!</h2>"

    return render_template('maps_register.html', form=form)

def maps_bookings():
    form = MapsBookings()

    if form.validate_on_submit():
        return "<h2>Booking Successful!</h2>"

    return render_template('maps_bookings.html', form=form)
