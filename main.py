import os
import eel

from Engine.features import *
from Engine.command import *
from Engine.auth import recoganize
def start():
    
    eel.init("WWW")
    
    playAssistantSound()
    @eel.expose
    def init():
        # subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello! I'm Savi, your smart assistant. How can I help you today?")
            eel.hideStart()
        else:
            speak("Face Authentication Fail")
    os.system('start msedge.exe --app="http://localhost:8000/Index.html"')

    eel.start('Index.html' , mode=None, host='localhost', block=True)