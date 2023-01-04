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
import workstations
import lab_autonomy
from firebase_admin import auth

#cred = credentials.Certificate("fsmdashboard-1f0d5-firebase-adminsdk-6718m-8b743ae8b2.json")
#cred = credentials.Certificate("labautonomy-firebase-adminsdk-lsyts-4196d3e085.json")
#firebase_admin.initialize_app(cred)

#db= firestore.client()

#db.collection('cp-lab').add({'name':'Samyak'})
#db.collection('cp-lab').document('Machines').set({'Station1_W':True})

def readychirp1():
    winsound.Beep(1000,300)

def readychirp2():
    winsound.Beep(600,300)

def speak(text):
    engine=pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)
    print("JARVIS "+text+"\n")
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        readychirp1()
        print("listening...",end="")
        audio=r.listen(source)
        query=''
        readychirp2()
        
        try:
            print("recognizing....",end="")
            query=r.recognize_google(audio,language='en-IN')
            print(f"user said {query}")

        except Exception as e:
            print("Exception"+str(e))

    return query.lower()


def conversationFlow():
    while True:
        usersaid=takeCommand()
        if 'hello' in usersaid:
            speak('hello i am Jarvis')

        if 'good morning' in usersaid:
            lab_autonomy.lights(True)
            speak('good morning')

        if 'good night' in usersaid:
            lab_autonomy.lights(False)
            speak('good night')

        if 'switch on' in usersaid:

            if 'workstation 1' in usersaid:  # or 'work station 1' or 'workstation one'
                speak('switching on workstation 1')
                workstations.station1(True)
                break

            if 'workstation 2' in usersaid: #or 'work station 2' or 'workstation two' 
                speak('switching on workstation 2')
                workstations.station2(True)
                break

            if 'workstation 3' in usersaid: #or 'work station 3' or 'workstation three' 
                speak('switching on workstation 3')
                workstations.station3(True)
                break

            if 'all lights' in usersaid:
                lab_autonomy.lights(True)
                speak('switching on all lights')
                break

            if 'all fans' in usersaid:
                lab_autonomy.fans(True)
                speak('switching on all fans')
                break

            if 'all ac' in usersaid:
                lab_autonomy.acs(True)
                speak('switching on all ac')
                break

        if 'switch off' in usersaid:
            
            if 'workstation 1' in usersaid: #or 'work station 1' or 'workstation one'
                speak('switching off workstation 1')
                workstations.station1(False)
                break

            if 'workstation 2' in usersaid: # or 'work station 2' or 'workstation two' 
                speak('switching off workstation 2')
                workstations.station2(False)
                break

            if 'workstation 3' in usersaid:#or 'work station 3' or 'workstation three' 
                speak('switching off workstation 3')
                workstations.station3(False)
                break

            if 'all lights' in usersaid:
                lab_autonomy.lights(False)
                speak('switching off all lights')
                break

            if 'all fans' in usersaid:
                lab_autonomy.fans(False)
                speak('switching off all fans')
                break

            if 'all ac' in usersaid:
                lab_autonomy.acs(False)
                speak('switching off all ac')
                break
        
        if 'reset' in usersaid:
            if 'workstation 1' in usersaid:  # or 'work station 1' or 'workstation one'
                speak('Reseting Station 1')
                workstations.reset_station1()
                break

        if 'clear faults' in usersaid:
            speak('Clearing Faults.....')
            workstations.station_clear_faults()
            break

        if 'place order' in usersaid:
            speak('Placing order..')
            workstations.placeorder()
            break

        if 'emergency' in usersaid:  # or 'stop ' 
            speak("Emergency stopping")
            workstations.emergency()
            break

        else:
            speak("Kindly speak again.....")
            break

        time.sleep(1)

                    

def main():
    porcupine=None
    pa=None
    audio_stream = None

    print("JARVIS IS READY")
    speak('hello i am jarvis')
    pa=pyaudio.PyAudio()
    #pa.get_default_input_device_info()
    #print(pa.get_device_count())
    #for i in range(pa.get_device_count()):#list all available audio devices
        #dev = pa.get_device_info_by_index(i)
        #print((i,dev['name'],dev['maxInputChannels']))

    try:
        porcupine=pvporcupine.create(access_key="99mF9DOHBRhiSe1DgAUT4S9SMIwa5WVPvM1+CvKWVcLuKal7u0rP1w==",keywords=["jarvis","computer"])
        pa=pyaudio.PyAudio()
        pa.get_default_input_device_info()
        audio_stream=pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        while True:
            pcm=audio_stream.read(porcupine.frame_length)
            pcm=struct.unpack_from("h"*porcupine.frame_length,pcm)

            keyword_index=porcupine.process(pcm)
            if keyword_index>=0:
                print("HOTWORD DETECTED..",end="")
                conversationFlow()
                time.sleep(0.5)
                print("JARVIS AWAITING FOR YOUR CALL")

    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
            pa.terminate()
    #await asyncio.gather(myproc(),commands())

if __name__=='__main__':
    main()
