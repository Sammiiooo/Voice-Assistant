import os
import datetime
import pyttsx3 
import speech_recognition as sr
import wikipedia 
import webbrowser
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hello sir, I am your assistant. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    mic_list = sr.Microphone.list_microphone_names()
    print("Available microphones:")
    for index, name in enumerate(mic_list):
        print(f"Microphone with index {index}: {name}")
        
    with sr.Microphone(device_index=0) as source:  # Change the index to the appropriate value
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Could not understand the audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "None"
    return query

def processQuery():
    query = takeCommand().lower()
    if query == "None":
        return
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif 'open youtube' in query:
        webbrowser.open("youtube.com")
    elif 'open google' in query:
        webbrowser.open("google.com")
    elif 'open stack overflow' in query:
        webbrowser.open("stackoverflow.com")
    elif 'open game' in query:
        gamePath = "C:\\Riot Games\\Riot Client\\RiotClientServices.exe" 
        os.startfile(gamePath)
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

def startAssistant():
    wishme()
    processQuery()

# UI setup
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("400x400")
root.configure(bg="#2E2E2E")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Adding a photo
photo_path = "D:\\Jarvis\\assistant.jpeg"
img = Image.open(photo_path)
img = img.resize((150, 150), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(img)

label = tk.Label(root, image=photo, bg="#2E2E2E")
label.pack(pady=10)

title_label = tk.Label(root, text="Voice Assistant", font=("Helvetica", 18, 'bold'), fg="#FFFFFF", bg="#2E2E2E")
title_label.pack(pady=10)

start_button = tk.Button(root, text="Start", command=startAssistant, font=("Helvetica", 14), bg="#4CAF50", fg="#FFFFFF", activebackground="#45A049", padx=20, pady=10, bd=0)
start_button.pack(pady=20)

quit_button = tk.Button(root, text="Quit", command=on_closing, font=("Helvetica", 14), bg="#F44336", fg="#FFFFFF", activebackground="#E53935", padx=20, pady=10, bd=0)
quit_button.pack(pady=10)

root.mainloop()
