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


cred2 = credentials.Certificate("labautonomy-firebase-adminsdk-lsyts-4196d3e085.json")

autonomy_app = firebase_admin.initialize_app(cred2,name="lab_autonomy")

db2 = firestore.client(autonomy_app)

def lights(value):
    print(db2)
    db2.collection('cp_lab').document('cpl').update({'Lights1_W':value})
    db2.collection('cp_lab').document('cpl').update({'Lights2_W':value})

def fans(value):
    db2.collection('cp_lab').document('cpl').update({'Fan1_W':value})
    db2.collection('cp_lab').document('cpl').update({'Fan2_W':value})
    db2.collection('cp_lab').document('cpl').update({'Fan3_W':value})
    db2.collection('cp_lab').document('cpl').update({'Fan4_W':value})

def acs(value):
    db2.collection('cp_lab').document('cpl').update({'AC1_W':value})
    db2.collection('cp_lab').document('cpl').update({'AC2_W':value})