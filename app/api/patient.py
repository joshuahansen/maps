##
# Medical Appointment System (MAPS) - IoT Sem2 2018
# 
# Patient API file, handels all interactions with the cloud
#
# Authors: Adam Young, Joshua Hansen, Lohgan Nash, Zach Wingrave
##

from flask import request, jsonify
import MySQLdb.cursors
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from app import app, db, ma
from app.database_tables.patient import Patient, PatientSchema
from app.database_tables.patient_notes import PatientNotes, PatientNotesSchema
from app.database_tables.doctor import Doctor, DoctorSchema
from app.database_tables.doctor_availability import DoctorAvailability, DoctorAvailabilitySchema
from app.database_tables.appointment import Appointment, AppointmentSchema
from app.database_tables.patient_queue import PatientQueue, PatientQueueSchema

patient_schema = PatientSchema()
patient_schema = PatientSchema(many=True)
patient_queue_schema = PatientQueueSchema()
patient_queue_schema = PatientQueueSchema(many=True)
doctor_schema = DoctorSchema()
doctor_schema = DoctorSchema(many=True)
doctor_availability_schema = DoctorAvailabilitySchema()
doctor_availability_schema = DoctorAvailabilitySchema(many=True)

def get_patient(patient_id):
    '''
    Return a patient's data in JSON format

    @param patient_id is a integer patient id
    '''
    patient = Patient.query.filter_by(id=patient_id)

    result = patient_schema.dump(patient)

    response = jsonify(result.data)
    response.status_code = 200
    return response

def get_all_patients():
    '''
    Return all patient's data in JSON format
    '''
    all_patients = Patient.query.all()
    result = patient_schema.dump(all_patients)
    
    response = jsonify(result.data)
    response.status_code = 200
    return response

def add_patient(request):
    '''
    Add  a new patient to the database
    
    @param request is a json object with the following elements:
        firstname
        lastname
        phone
        email
        gender
        dob
        address
        city
        state
        postcode
    @return json object with elements:
        status
        action
    '''
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    phone = request.json['phone']
    email = request.json['email']
    gender = request.json['gender']
    dob = request.json['dob']
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    postcode = request.json['postcode']

    new_patient = Patient(firstname, lastname, phone, email,
                    gender, dob, address, city, state, postcode)

    db.session.add(new_patient)
    db.session.commit()

    response = jsonify({"status": "Successful", "action": "add"})
    response.status_code = 200

    return response
    
def update_patient(patient_id, data):
    '''
    Update a current patients data
    
    @param patient_id integer of the patient wishing to update
    @param data json object with patient details
    @returns json object with elements
        status
        action
    '''
    Patient.query.filter_by(id=patient_id).update(data)

    db.session.commit()


    response = jsonify({"status": "Successful", "action": "update", "id": patient_id})
    response.status_code = 200

    return response

def delete_patient(patient_id):
    '''
    Delete a patient from the database
    
    @param patient_id integer patient id to be deleted
    @return json object awith elements:
        status
        action
    '''
    Patient.query.filter_by(id=patient_id).delete()
    
    db.session.commit()
    
    response = jsonify({"status": "Successful", "action": "delete", "id": patient_id})
    response.status_code = 200

    return response

def make_appointment(request):
    '''
    Add  a new appointment to the database
    Also creates a new appointment in the doctors calendar

    @param request json object with the elements:
        patient
        startDate
        endDate
        doctor
        description
        summary
        location

    @return json object with elements:
        status
        action
        id
    '''
    
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('calendar-config.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
   
    try:
        patient_id = request.json['patient']
        startDate = request.json['startDate']
        endDate = request.json['endDate']
        doctor_id = request.json['doctor']
        description = request.json['description']
        summary = request.json['summary']
        location = request.json['location']
        
        doctor = Doctor.query.filter_by(id=doctor_id)
        doctor_result = doctor_schema.dump(doctor).data
        if len(doctor_result) < 1:
            raise ValueError
        doctor_result = doctor_result[0]
        
        patient = Patient.query.filter_by(id=patient_id)
        patient_result = patient_schema.dump(patient).data
        
        if len(patient_result) < 1:
            raise ValueError
        patient_result = patient_result[0]


        time_start = "{}".format(startDate)
        time_end   = "{}".format(endDate)

        new_appointment = Appointment(patient_id, doctor_id, time_start, time_end)
        db.session.add(new_appointment)
        db.session.commit()
        
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': time_start,
                'timeZone': 'Australia/Melbourne',
            },
            'end': {
                'dateTime': time_end,
                'timeZone': 'Australia/Melbourne',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 5},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
            'attendees': [
                {
                    'email': doctor_result['email'],
                    'email': patient_result['email']
                }
            ],
            'transparency': 'opaque'
        }
        calendarID = doctor_result['calendarID']
        print(calendarID)
        event = service.events().insert(calendarId=calendarID, body=event).execute()
        print('Event created: {}'.format(event.get('htmlLink')))

        response = jsonify({"status": "Successful", "action": "make-appointment", "id": patient_id})
        response.status_code = 200
    except ValueError:
        response = jsonify({"status": "failed", "action": "make-appointment", "id": patient_id})
        response.status_code = 200
    finally:
        return response

def get_availability(request):
    '''
    Return availability of doctors on certain day

    @param request json object with elements:
        date
        doctorID
    
    @return json object:
        availability
        busy []
    '''
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('calendar-config.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    
    try:
        doctor_id = request.json['doctorID']
        date = datetime.strptime(request.json['date'], "%Y-%m-%d")
        day = date.weekday()

        doctor_availability = DoctorAvailability.query.filter_by(doctor_id = doctor_id, day = day)
        doctor_availability_result = doctor_availability_schema.dump(doctor_availability).data
        
        if len(doctor_availability_result) < 1:
            raise ValueError
        doctor_availability_result = doctor_availability_result[0]
        
        startTime = doctor_availability_result['startTime']
        endTime = doctor_availability_result['endTime']

        doctor = Doctor.query.filter_by(id=doctor_id)
        doctor_result = doctor_schema.dump(doctor).data
        
        if len(doctor_result) < 1:
            raise ValueError
        doctor_result = doctor_result[0]
        
        dateString = date.strftime("%Y-%m-%d")
        start_time = "{0}T{1}:00+10:00".format(dateString, startTime)
        end_time = "{0}T{1}:00+10:00".format(dateString, endTime)
        
        freebusy = {
                "timeMin": start_time,
                "timeMax": end_time,
                "items": [
                    {
                        "id": doctor_result['calendarID']
                    }
                ],
                "timeZone": "Australia/Melbourne"
            }
        
        freebusyResponse = service.freebusy().query(body=freebusy).execute()

        response = jsonify({"availability": doctor_availability_result, "busy": freebusyResponse['calendars'][doctor_result['calendarID']]['busy']})
        response.status_code = 200
    except ValueError:
        response = jsonify({"status": "failed", "action": "get doctor's availability", "id": doctor_id})
        response.status_code = 404
    finally:    
        return response

def get_doctors():
    '''
    Get all doctors for patients page selection

    @return json object with doctor details
    '''
    all_doctors = Doctor.query.all()
    result = doctor_schema.dump(all_doctors)
    
    response = jsonify(result.data)
    response.status_code = 200
    return response


def face_detected(request):
    '''
    Add new patient to the queue when detected with camera

    @param request json object
        patient with form firstname_lastname

    @return json object:
        data
    '''
    print(request.json)
    patient_name = request.json['patient']
    fname, lname = patient_name.split("_")

    patient = Patient.query.filter(Patient.firstname.like(fname), Patient.lastname.like(lname))
    result = patient_schema.dump(patient).data

    if(len(result) > 0):
        patient_id = result[0]['id']
        arrival = datetime.now()
        
        queue = PatientQueue.query.filter(PatientQueue.patient_id == patient_id)
        queue_results = patient_queue_schema.dump(queue).data

        if len(queue_results) == 0:
            new_arrival = PatientQueue(patient_id, arrival)

            db.session.add(new_arrival)
            db.session.commit()
            response = jsonify({"data": "Patient added to the queue"})
            response.status_code = 200
        else:
            response = jsonify({"data": "Patient already in the queue"})
            response.status_code = 200
            
    else:
        response = jsonify({"data": "Patient was not added to the queue"})
        response.status_code = 404
        
    return response
    
def reset():
    '''
    Used to reset the database if needed
    
    @return json object
        data
    '''
    try:
        # Uncomment to delete all tables in database
        #db.drop_all()
        # Uncomment to add all tables to the database
        db.create_all()
        db.session.commit()

        response = jsonify({"data": "Database was reset"})

        response.status_code = 200
    except:
        response = jsonify({"data": "Database was not reset"})

        response.status_code = 404
    finally:
        return response
