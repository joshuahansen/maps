# maps

MAPS - Medical Appointment System

# Installation
Development is done within a virtual environment to properly organise project
dependancies.

```
# clone the source
git clone git@bitbucket.org:joshuahansen188/maps.git
cd maps

# create a virtual environment for this projects dependancies
virtualenv venv

# activate the virtual environment.
source venv/bin/activate

# install mysql client on raspberry pi
sudo apt update
sudo apt install default-libmysqlclient-dev

# install project dependancies (into your local virtual environment)
pip3 install -r requirements.txt

# Run the Flask server
flask run
```
