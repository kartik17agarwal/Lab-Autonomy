from sqlite3 import Time
import speech_recognition as sr
import pyttsx3
import pvporcupine
import pyaudio
import struct
import time
import winsound
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 
from firebase_admin import auth

cred = credentials.Certificate("fsmdashboard-1f0d5-firebase-adminsdk-6718m-8b743ae8b2.json")

firebase_admin.initialize_app(cred)

db= firestore.client()

def station1(value):
    db.collection('Controls').document('WS1').update({'External_Start':value})

def reset_station1(value):
    db.collection('Controls').document('WS1').update({'External_Reset':value}) 

def station_clear_faults(value):
    db.collection('Controls').document('WS1').update({'Clear_Faults_External':value})

def station2(value):
    db.collection('Controls').document('WS2').update({'External_Start':value})

def emergency(value):
    db.collection('Controls').document('WS1').update({'External_Emergency':value})