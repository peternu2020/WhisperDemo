
from os import path
#must pip install pydub and also install ffmpeg
from pydub import AudioSegment
import sys
import os

def main ():
    #src must be directory with files to properly work
    for filename in os.listdir('.'):
        if filename.endswith(".mp3"):
            split = filename.split(".")
            dst = split[0] + ".wav"
            sound = AudioSegment.from_mp3(filename)
            sound.export(dst, format="wav")
            os.remove(filename)
main()