from ast import keyword
import os
import re
import subprocess
import time
from playsound import playsound
import eel
import pyautogui
from Engine.config import ASSISTANT_NAME
from Engine.command import speak
import pywhatkit as kit
import webbrowser
import sqlite3
import pvporcupine
import pyaudio
import struct
from urllib.parse import quote

from Engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("savi.db")
cursor = con.cursor()

#---------------- Playing Assistant Sound Function ----------------#
@eel.expose
def playAssistantSound():
    # music_dir = "C:\Users\Admin\Desktop\Coding Project\11)Voice Assistant\Savi\WWW\Assets\Audio\Start_Sound.mp3"
    # playsound(music_dir)
    playsound("WWW\\Assets\\Audio\\Start_Sound.mp3")




def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()

    if app_name != "":
        
        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN(?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                    'SELECT url FROM web_command WHERE name IN(?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening " + query)
                    try:
                        os.system('start ' + query)
                    except:
                        speak("Not Found")
        except:
            speak("Something went wrong")


def PlayYouTube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)
    
    
    
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        
        #---------------- Pre Trained Keywords ----------------#
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"])
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        #---------------- Loop for Streaming ----------------#
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)
            
            #---------------- Processing keyword comes from mic ----------------#
            keyword_index=porcupine.process(keyword)
        
            #---------------- Checking first keyword detected for not ----------------#
            if keyword_index>=0:
                print("Hotword detected")

                #---------------- Pressing shortcut key win+j ----------------#
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



#---------------- Whatsapp Message Sending ----------------#
def findContact(query):    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+94 ' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('Not exist in contacts')
        return 0, 0

def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        jarvis_message = "Message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "Calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "Staring video call with "+name
        

    #---------------- Encode the message for URL ----------------#
    encoded_message = quote(message)

    #---------------- Construct the URL ----------------#
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    #---------------- Construct the full command ----------------#
    full_command = f'start "" "{whatsapp_url}"'

    #---------------- Open WhatsApp with the constructed URL using cmd.exe ----------------#
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)          


#---------------- Chat Bot ----------------#
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path=r"Savi\Engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

#---------------- Android Automation ----------------#

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


#---------------- To Send Message----------------#
def sendMessage(message, mobileNo, name):
    from Engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("Sending Message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    #---------------- Open SMS App ----------------#
    tapEvents(413, 1936)
    #---------------- Start Chat ----------------#
    tapEvents(413, 1942)
    #---------------- Search Mobile No ----------------#
    adbInput(mobileNo)
    #---------------- Tap on Name ----------------#
    tapEvents(414, 984)
    #---------------- Tap on Input ----------------#
    tapEvents(668, 1025)
    #---------------- Message ----------------#
    adbInput(message)
    #---------------- Send ----------------#
    tapEvents(922, 1066)
    speak("Message Send Successfully " + name)