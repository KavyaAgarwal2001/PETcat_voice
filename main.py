import time 
import pyaudio
import wave
import numpy as np
import scipy as sp
from scipy.io.wavfile import read
from scipy.io.wavfile import write     # Imported libaries such as numpy, scipy(read, write), matplotlib.pyplot
from scipy import signal
import matplotlib.pyplot as plt
from vosk import Model, KaldiRecognizer
import os
import json
import pyttsx3

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

class speech_process:
    def soundrecord():
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "audio.wav"
        
        audio = pyaudio.PyAudio()
        
        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        print "recording..."
        frames = []
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print "finished recording"
        
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

    def noiseremove(string):
        (Frequency, array) = read(string)
        plt.plot(array) 
        plt.title('Original Signal Spectrum')
        plt.xlabel('Frequency(Hz)')
        plt.ylabel('Amplitude')
        plt.show()
        b,a = signal.butter(5, 1000/(Frequency/2), btype='highpass')
        filteredSignal = signal.lfilter(b,a,array)
        plt.plot(filteredSignal) # plotting the signal.
        plt.title('Highpass Filter')
        plt.xlabel('Frequency(Hz)')
        plt.ylabel('Amplitude')
        plt.show()
        c,d = signal.butter(5, 1000/(Frequency/2), btype='lowpass') # ButterWorth low-filter
        newfilteredSignal = signal.lfilter(c,d,filteredSignal) # Applying the filter to the signal
        plt.plot(newfilteredSignal) # plotting the signal.
        plt.title('Lowpass Filter')
        plt.xlabel('Frequency(Hz)')
        plt.ylabel('Amplitude')
        plt.show()
    
    def speechtotext(string):
        if not os.path.exists("model-en"):
            print ("Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model-en' in the current folder.")
            exit (1)

        wf = wave.open(string, "rb")

        # print(wf)
        if wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print ("Audio file must be WAV format mono PCM.")
            exit (1)

        model = Model("model-en")
        rec = KaldiRecognizer(model, wf.getframerate())
        text=""
        while True:
            data = wf.readframes(100000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                text = text + res[ 'text']
            # else:
                # res = json.loads(rec.PartialResult()
        res = json.loads(rec.FinalResult())
        text = text +res[ 'text' ]
        return text
    
    def texttospeech(string):
        engine = pyttsx3.init() 
        engine.setProperty('volume',1.0)
        engine.setProperty('rate', 125)
        # testing 
        str = sys.argv[1]
        engine.say(str)  
        engine.runAndWait()
    
f= speech_process()
f.sound record()
time.sleep(15)
f.noiseremove("audio.wav")
time.sleep(15)
f.speechtotext("output.wav")
string1 = time.sleep(25)
f.texttospeech(string1)



    