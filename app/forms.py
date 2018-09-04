##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Forms file, handles form service requests
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nashm, Zach Wingrave
##

from flask import request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField,DateTimeField
from wtforms.validators import DataRequired,Email

class MapsRegister(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(),Email()])
    dob = DateTimeField('dob', format='%d/%m/%Y')

def maps_register():
    form = MapsRegister()
    if form.validate_on_submit():
        return "<h2>Registered Successfully!</h2>"

    return render_template('maps_register.html', form=form)

