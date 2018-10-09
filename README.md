# maps

MAPS - Medical Appointment System

# API Documentation
Navigate to: /docs

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

# installing google cloud sdk (May not be needed)
 cd ~
 wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-215.0.0-linux-x86_64.tar.gz
 tar -xvf google-cloud-sdk-215.0.0-linux-x86_64.tar.gz google-cloud-sdk
 ./google-cloud-sdk/install.sh
Restart Console
 gcloud init --console-only

# install project dependancies (into your local virtual environment)
pip3 install -r requirements.txt

# Google Calendar
create Oauth2 credentials (type other) in google cloud console
download file and rename to calendar-config.json
mv calendat-config.json to project root directory
python3 create_token.py --noauth_local_webserver
login online

# Face Detection
For best installation follow the following tutorial
https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
As we already have a virtual environment there is no need to do step 4
Leave plenty of time for instalation as it takes multiple hours on the pi

# Run the Flask server
flask run
```
