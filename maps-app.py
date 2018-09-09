##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# This file is the base launcher of our application, by importing the Flask app
# created within app/__init__.py.
#
# Subsequent project files should include a similar header 
# 
# Authors: Adam Young, Joshua Hansen, Lohgan Nashm, Zach Wingrave
##

from app import app

# App specific config
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'rgsdGSRFS4t56uh)(*&^'

