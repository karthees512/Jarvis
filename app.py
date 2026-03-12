from flask import Flask, render_template, jsonify
import speech_recognition as sr
import pyttsx3
import os
import datetime

app = Flask(__name__)

# Jarvis Voice Setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # Professional Male Voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command')
def get_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.8) # For Realme Buds N1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in').lower()
        print(f"User said: {query}")
        
        # System Automation Logic
        if 'hello' in query:
            speak("Hello Sir, Jarvis is operational.")
            
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"Sir, the time is {strTime}")
            
        elif 'open brave' in query:
            speak("Opening Brave Browser .")
            # Note: Path may vary. Standard path below:
            brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
            os.startfile(brave_path)
            
        elif 'open notepad' in query:
            speak("Opening Notepad.")
            os.system("start notepad")
            
        elif 'open chrome' in query:
            speak("Opening Google Chrome.")
            os.system("start chrome")
            
        elif 'open code' in query or 'vs code' in query:
            speak("Opening Visual Studio Code.")
            os.system("code") # Works if VS Code is in your PATH
            
        return jsonify({"status": "success", "command": query})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": "Voice not captured"})

if __name__ == "__main__":
    print("Jarvis Engine Initialized.")
    app.run(debug=True, port=5000)