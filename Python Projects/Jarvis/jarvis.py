import speech_recognition as sr
import requests
import webbrowser
import datetime
import os
import random
import win32com.client
import ctypes

# =========================
# ADMIN CHECK (IMPORTANT)
# =========================
if not ctypes.windll.shell32.IsUserAnAdmin():
    print("Please run as Administrator")
    # exit()  # optional

# =========================
# CONFIG
# =========================
API_KEY = "API_KEY_HERE"  # get from https://groq.com/account/api-keys

API_URL = "https://api.groq.com/openai/v1/chat/completions"

# =========================
# VOICE ENGINE
# =========================
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def speak(text):
    print("\nJarvis:", text)
    speaker.Speak(text)

def stop_speaking():
    speaker.Speak("")  # instant stop
    print("Speech stopped")

# =========================
# LISTEN
# =========================
recognizer = sr.Recognizer()

def listen():
    try:
        with sr.Microphone() as source:
            print("\n🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=6)

        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text.lower()

    except:
        return ""

# =========================
# AI CHAT
# =========================
def ask_ai(text):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """
    You are Jarvis.

    - Reply in SAME language user speaks (English or Roman Urdu)
    - Keep replies short and natural
    - Be helpful like a personal assistant
    """

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    }

    try:
        r = requests.post(API_URL, headers=headers, json=data, timeout=15)

        if r.status_code != 200:
            return "AI error"

        return r.json()["choices"][0]["message"]["content"]

    except:
        return "Connection issue"

# =========================
# SYSTEM FUNCTIONS
# =========================
def open_google():
    webbrowser.open("https://google.com")
    speak("Google open")

def open_youtube():
    webbrowser.open("https://youtube.com")
    speak("YouTube open")

def search_google(q):
    webbrowser.open(f"https://www.google.com/search?q={q}")
    speak("Searching")

def open_notepad():
    os.startfile("notepad.exe")
    speak("Notepad open")

def close_notepad():
    os.system("taskkill /f /im notepad.exe")
    speak("Notepad closed")

def open_calculator():
    os.startfile("calc.exe")
    speak("Calculator open")

def close_calculator():
    os.system("taskkill /f /im CalculatorApp.exe")
    speak("Calculator closed")

def wifi_off():
    os.system('netsh interface set interface "Wi-Fi" disable')
    speak("WiFi off")

def wifi_on():
    os.system('netsh interface set interface "Wi-Fi" enable')
    speak("WiFi on")

def tell_time():
    t = datetime.datetime.now().strftime("%I:%M %p")
    speak("Time is " + t)

def tell_date():
    d = datetime.datetime.now().strftime("%d %B %Y")
    speak("Date is " + d)

# =========================
# STARTUP
# =========================
speak(random.choice([
    "Jarvis online",
    "System ready",
    "I am active"
]))

# =========================
# MAIN LOOP
# =========================
while True:

    command = listen()

    if not command:
        continue

    # STOP SPEAKING
    if "stop talking" in command or "stop" in command:
        stop_speaking()
        continue

    # EXIT
    if "exit" in command or "shutdown" in command:
        speak("Going offline")
        break

    # OPEN APPS
    elif "open google" in command:
        open_google()

    elif "open youtube" in command:
        open_youtube()

    elif "open notepad" in command:
        open_notepad()

    elif "open calculator" in command:
        open_calculator()

    # CLOSE APPS
    elif "close notepad" in command:
        close_notepad()

    elif "close calculator" in command:
        close_calculator()

    # WIFI
    elif "wifi off" in command or "turn off wifi" in command:
        wifi_off()

    elif "wifi on" in command or "turn on wifi" in command:
        wifi_on()

    # SEARCH
    elif "search" in command:
        q = command.replace("search", "")
        search_google(q)

    # TIME / DATE
    elif "time" in command:
        tell_time()

    elif "date" in command:
        tell_date()

    # AI CHAT
    else:
        reply = ask_ai(command)
        speak(reply)