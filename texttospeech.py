import pyttsx3 
import sys
# initialisation 
engine = pyttsx3.init() 
engine.setProperty('volume',1.0)
engine.setProperty('rate', 125)
# testing 
str = sys.argv[1]
engine.say(str)  
engine.runAndWait()