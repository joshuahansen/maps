##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Forms file, handles form service requests
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nashm, Zach Wingrave
##

from flask import request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField,DateTimeField,SelectField
from wtforms.validators import DataRequired,Email

class MapsRegister(FlaskForm):
    fname = StringField('fname', validators=[DataRequired()])
    lname = StringField('lname', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(),Email()])
    dob = DateTimeField('dob', format='%d/%m/%Y')
    gender = SelectField('gender',
        validators=[DataRequired()],
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ]
    )
    address = StringField('address', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', 
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
    postcode = StringField('postcode', validators=[DataRequired()])

def maps_register():
    form = MapsRegister()
    states = {
        'vic': 'VIC',
        'nsw': 'NSW',
        'act': 'ACT',
        'qld': 'QLD',
        'nt': 'NT',
        'wa': 'WA',
        'sa': 'SA',
        'tas': 'TAS'
    }
    genders = {
        'male': 'Male',
        'female': 'Female',
        'other': 'Other'
    }
    if form.validate_on_submit():
        return "<h2>Registered Successfully!</h2>"

    return render_template('maps_register.html', form=form, states=states, genders=genders)

