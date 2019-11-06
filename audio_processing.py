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

from text_similarity import get_best_answer_audio_id

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
    WAVE_OUTPUT_FILENAME ="audios/question.wav"
    
    audio = pyaudio.PyAudio()
    
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
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


def play_answer(qst):
    audio_id = get_best_answer_audio_id(qst)
    # audio_file = retrieveAudioById(audio_id)
    audio_file = "audios/crucifixion3.wav"
    play_sound(audio_file)