#!/usr/bin/env python3

import socket
import json
import requests
import time
import pygame
from gtts import gTTS

#from walexa
from difflib import SequenceMatcher
import sys
import math
import struct
import time
import csv
import pyaudio
import wave
import speech_recognition as sr

audios = ["crucifixion1.mp3", "crucifixion2.mp3", "crucifixion3.mp3", "crucifixion4.mp3"]
last_qst = ""
class obj:
    def __init__(self, name):
        self.name = name
        self.who = None
        self.where = None 
        self.what = None 
        self.why = None 
        self.when = None 

    def get_ans(self, qst):
        qst = qst.lower()
        ans = ""
        if "who" in qst:
                ans = self.who
        elif "where" in qst:
                ans = self.where
        elif "what" in qst:
                ans = self.what
        elif "why" in qst:
                ans = self.why
        elif "when" in qst:
                ans= self.when
        else:
                ans = "I don't understand"
        return ans
    def get_second_ans(self, qst):
        qst = qst.lower()
        ans = ""
        if "who" in qst:
                ans = self.who2
        elif "where" in qst:
                ans = self.where2
        elif "what" in qst:
                ans = self.what2
        elif "why" in qst:
                ans = self.why2
        elif "when" in qst:
                ans= self.when2
        else:
                ans = "no further information"
        return ans        

objects = []
def initialize_everything():
    cruxobj = obj(name = 'the crucifixion')
    cruxobj.who= 'The crucifixion was created by Naddo Ceccarelli'
    cruxobj.who2 = 'Naddo Ceccarelli was a gifted pupil of the leading Sienese painter Simone Martini. Ceccarelli was particularly skilled in suggesting the shine of metalwork through his use of tempera'
    cruxobj.what = 'The crucifixion is a Tempera and gold on panel  gold leaf is gilded onto the wood panel before inscription and detailing'
    cruxobj.what2 = 'The crucifixion is a depiction of Jesus Christs death as spoken about in the Bible'
    cruxobj.where = 'The crucifixion was created in Siena Italy'
    cruxobj.where2 = 'It was created In siena after he returned from Avignon in 1330'
    cruxobj.why = 'The crucfixion is a depiction of Christs death  used in many Churches. These panel works were typically used in reliquaries'
    cruxobj.why2 = 'Ceccarelli was particularly skilled in suggesting the shine of metalwork through his use of tempera. He carefully layered his paint over the gold ground, which he enriched with a variety of tooled and incised designs. Ceccarelli was apt at capturing the gleam of chain mail and the arabesques of damask'
    cruxobj.when = 'The crucifixion was created in the 14th century  circa 1350-1359'
    cruxobj.when2 = 'experts are not sure exactly when but it is estimated that it was around 1352'
    objects.append(cruxobj)

initialize_everything()
# from server.py
language = 'en'

HOST = '129.105.10.218'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

         

def play_sound(fname):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(fname)
    print("playing", fname)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    print("done playing", fname)

def play_piece_audios(audios):
    for audio in audios:
        play_sound(audio)

def record_qst():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 8
    WAVE_OUTPUT_FILENAME ="question.wav"
    
    audio = pyaudio.PyAudio()
    
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")
    
    
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def get_qst(fname):
    audio_f = sr.AudioFile(fname)
    r = sr.Recognizer()
    with audio_f as source:
        audio = r.record(source)
    try:
        qst = r.recognize_google(audio)
    except sr.UnknownValueError:
        qst = None
    return qst

def create_answer(qst):
    answ = "I don't understand"
    for elem in objects:
        if elem.name in qst.lower():
            print(elem.name)
            answ = elem.get_ans(qst.lower())
    print(answ)
    save_answer(answ)

def create_second_response(qst):
    answ = "I have no further information"
    for elem in objects:
        if elem.name in qst.lower():
            print(elem.name)
            answ = elem.get_second_ans(qst.lower())
    print(answ)
    save_answer(answ)

def save_answer(answ):
    myobj = gTTS(text=answ, lang=language, slow=False) 
    myobj.save("answer.mp3") 
    play_sound("answer.mp3")

def get_distance():
    sound_played = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print("server started")
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', conn, ' ', addr)
            while True:
                conn, addr = s.accept()
                data = conn.recv(1024)
                if data:
                    j = json.loads(data.decode())['d']['distance']
                    if j<50 and not sound_played:
                        print("playing piece audios")
                        play_piece_audios(audios)
                        sound_played = True
                        while True:
                            record_qst()
                            qst = get_qst("question.wav")
                            print(qst)
                            if qst is None:
                                sound_played = False
                                break
                            if "more" in qst.lower():
                                if last_qst != "":
                                    create_second_response(last_qst)
                            elif "cat" in qst.lower():
                                create_answer(qst)
                            last_qst = qst
                            
       
get_distance()

