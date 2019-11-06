#!/usr/bin/env python3
import socket
import json
import requests
import time
import pygame
from gtts import gTTS
from difflib import SequenceMatcher
import sys
import math
import struct
import time
import csv
import pyaudio
import wave
import speech_recognition as sr

from audio_processing import *

audios = ["crucifixion1.wav"]

# from server.py
language = 'en'

HOST = '129.105.10.218'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

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
                            play_answer(qst)
                            
       
# get_distance()

