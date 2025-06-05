import pyttsx3
import speech_recognition as sr 
import eel
import time
def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():  

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening........")
        eel.DisplayMessage("Listening........")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)

        try:
            print("Recognizing........")
            eel.DisplayMessage("Recognizing........")
            query = r.recognize_google(audio, language='en-in')
            print(f"User Said: {query}")
            eel.DisplayMessage(query)
            time.sleep(2)

        except Exception as e:
            return ""

        return query.lower()
    
@eel.expose
def allCommands(message=1):
    
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:
        
        if "open" in query:
            from Engine.features import openCommand
            openCommand(query)
        elif "youtube" in query and "play" in query:
            from Engine.features import PlayYouTube
            PlayYouTube(query) 
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from Engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use? WhatsApp or Mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("What message to send?")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("What message to send?")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)

        else:
            from Engine.features import chatBot
            chatBot(query)
            # print("I am not running")
    except Exception as e:
        print("Error:", e)

    eel.ShowHood()



    
# text = takeCommand()


# speak(text)