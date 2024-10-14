import webbrowser
import pyttsx3  # type: ignore
import datetime
import speech_recognition as sr  # type: ignore
import os
import wikipedia  # type: ignore
import subprocess
import pywhatkit  # type: ignore
import random
import requests
from bs4 import BeautifulSoup  # type: ignore
import cv2  # type: ignore
import numpy as np  # type: ignore
from ultralytics import YOLO
import requests
import mediapipe as mp
import json
import time


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate", 175)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning sir")
    elif 12 <= hour < 18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")


def takeCommands(say = "please lodge the query"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak(say)
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=10, phrase_time_limit=10)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Recognized command: {query}")
        return query.lower()
    except Exception as e:
        print("Error: Command not recognized. Please try again.")
        return None



def sylcommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please clarify if to stop.")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=10, phrase_time_limit=10)

    try:
        print("................")
        query = r.recognize_google(audio, language='en-in')
        print(f"Recognized command: {query}")
        return query.lower()
    except Exception as e:
        print("Error: Command not recognized. Please try again.")
        return None


def searchGoogle(query):
    if "google" in query or "internet" in query:
        import wikipedia as googleScrap

        query = query.replace("search google for", "")
        query = query.replace("search", "")
        query = query.replace("google search", "")
        query = query.replace("google", "")
        query = query.replace("internet", "")
        query = query.replace("search for", "")
        query = query.strip() 

        if not query:
            speak("Please provide a valid search term.")
            return

        speak(f"OK! searching for {query}")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query, 1)
            speak(result)
        except Exception as e:
            speak("No speakable output available")

def searchYoutube(query):
    query = query.lower().replace("youtube search", "").replace("search youtube", "").replace("youtube", "").strip()
    
    if query:
        speak(f"Searching YouTube for {query}")
        print(f"Searching YouTube for: {query}")
        
        try:
            web = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(web)

            query = takeCommands("Do you want me to play the top result on youtube?")
            if query=="yes":
                pywhatkit.playonyt(query)
            
            speak("Playing the top result on YouTube.")
        except Exception as e:
            print(f"Error during YouTube search: {e}")
            speak("Sorry, I encountered an issue while trying to play the video on YouTube.")
    else:
        speak("Please provide a valid search term for YouTube.")


c = ["Any tracks on mind?", "What song or track would you like to listen to?", "What shall I play?"]
h = random.choice(c)

def stop(silq):
    if any(word in silq for word in ["stop", 'quit', 'close', 'thats is', 'sleep']):
        exit()

def set_alarm():
    speak("At what time would you like me to set the alarm?")
    alarm_time = input("Please specify the alarm time (HH:MM AM/PM): ")
    alarm_hour, alarm_minute, alarm_period = alarm_time.split(":")
    alarm_hour = int(alarm_hour)
    alarm_minute, alarm_period = map(int, alarm_minute.split())

    if alarm_period.lower() == "pm":
        alarm_hour += 12
def open_application(app_name):
    speak(f"Opening {app_name}")
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(f'start {app_name}', shell=True)
        elif os.name == 'posix':  # Unix/Linux/Mac
            if "darwin" in os.sys.platform:  # MacOS
                subprocess.Popen(['open', '-a', app_name])
            else:  # Linux
                subprocess.Popen([app_name])
        else:
            speak("Sorry, unsupported operating system.")
            print("Unsupported OS")
    except FileNotFoundError:
        speak(f"Sorry, I couldn't find the application: {app_name}. Please check the name.")
        print(f"FileNotFoundError: {app_name} not found.")
    except Exception as e:
        speak(f"Sorry, I couldn't open {app_name}. Please try again.")
        print(f"Error: {e}")

def thumbs_up():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y:
                    # Detected thumbs up
                    speak("Thumbs up detected.")
                else:
                    # Detected thumbs down
                    speak("Thumbs down detected.")

        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def load_gestures():
    try:
        with open('gestures.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Add gesture to the JSON file
def add_gesture(gesture_name, landmarks):
    gestures = load_gestures()
    
    # Convert landmarks to a list of lists for JSON serialization
    gesture_data = {
        'name': gesture_name,
        'landmarks': landmarks
    }

    gestures[gesture_name] = gesture_data
    
    # Save to JSON file
    with open('gestures.json', 'w') as f:
        json.dump(gestures, f, indent=4)

# Hand detection function
def detect_hand_signs():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                gesture_name = recognize_gesture(landmarks)
                
                # Display detected gesture name
                if gesture_name:
                    cv2.putText(frame, gesture_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Hand Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Recognize gesture
def recognize_gesture(landmarks):
    gestures = load_gestures()
    for gesture_name, gesture_data in gestures.items():
        if gesture_data['landmarks'] == landmarks:
            return gesture_name
    return None

# Add gesture from user input
def add_gesture_from_user():
    gesture_name = takeCommands("Please say the name of the gesture to add:")
    speak(f"Please show the gesture for {gesture_name}.")
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                add_gesture(gesture_name, landmarks)  # Add gesture directly to the JSON file
                speak(f"{gesture_name} added successfully!")
                cap.release()
                cv2.destroyAllWindows()
                return

        cv2.imshow('Add Gesture', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def object_detection():
    speak("Starting object detection. Please wait.")
    
    model = YOLO('yolov5s.pt')

    cap = cv2.VideoCapture(0)
    
    while True:
        ret, img = cap.read()
        if not ret:
            break

        results = model(img)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0]) 
                conf = box.conf[0]
                cls = int(box.cls[0])
                label = model.names[cls] 
                color = (0, 255, 0) 
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("YOLO Object Detection", img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    speak("Object detection ended.")

def run():
    wishme()
    while True:
        query = takeCommands()

        if query:
            if any(word in query for word in ['who are you', 'introduce yourself', 'who is phoenix']):
                speak("I am a software assistant named Phoenix. I came into existence on the sixteenth of May, 2024, in the computer lab of R S S International School. By far, I have no persona and yet I tend to seek love and fulfill your requests.")
                continue

            elif any(word in query for word in ['launch the directory', 'run the directory', 'open the directory']):
                try:
                    os.system('cmd /k "dir/s"')
                except:
                    speak("Couldn't execute the directory run")
                continue

            elif "wikipedia" in query:
                speak("Fetching data from Wikipedia...")
                query = query.replace("wikipedia", '')
                results = wikipedia.summary(query, sentences=4)
                speak("According to Wikipedia...")
                speak(results)
                print(results)
                continue

            elif any(word in query for word in ['launch youtube', 'shoot youtube', 'open youtube']):
                webbrowser.open("https://youtube.com")
                continue

            elif any(word in query for word in ['launch insta', 'launch instagram', 'shoot insta', 'shoot instagram', 'open insta', 'open instagram']):
                webbrowser.open("https://instagram.com")
                continue

            elif any(word in query for word in ['launch github', 'shoot github', 'open github']):
                webbrowser.open("https://github.com")
                continue

            elif any(word in query for word in ['launch chatgpt', 'shoot chatgpt', 'open chatgpt']):
                webbrowser.open("https://chatgpt.com")
                continue

            elif any(word in query for word in ['launch netflix', 'shoot netflix', 'open netflix']):
                webbrowser.open("https://netflix.com")
                continue

            elif any(word in query for word in ['launch leetcode', 'shoot leetcode', 'open leetcode']):
                webbrowser.open("https://leetcode.com")
                continue

            elif any(word in query for word in ["lift the mood", "play me a track", "play music", "play me a song", "roll the cassette"]):
                speak(h)
                query = takeCommands()
                pywhatkit.playonyt(query)
                continue

            elif any(word in query for word in ['quit', 'exit', 'stop', 'shut up', 'shut down yourself', 'silence', 'go to sleep']):
                speak("Eradicating running script and killing the terminal")
                exit()
        
            elif any(word in query for word in ["what's the time", "what is the time", "read the clock"]):
                strH = int(datetime.datetime.now().strftime("%H"))
                strM = int(datetime.datetime.now().strftime("%M"))
                speak(f"the time is {strM} past {strH}")
                continue

            elif any(word in query for word in ['set an alarm', 'wake me up', 'ring at']):
                set_alarm()
                continue

            elif any(word in query for word in ["search google", "browse google", ("search" and "on google")]):
                searchGoogle(query)
                continue

            elif any(word in query for word in ["search youtube", "browse youtube", ("search" and "on youtube")]):
                searchYoutube(query)
                continue

            elif "shutdown the system" in query:
                query = takeCommands("Are You sure you want to shutdown")
                if "yes" in query:
                    os.system("shutdown /s /t 1")
                elif "no" in query:
                    break

            elif "temperature" in query:
                search = "temperature in noida"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak(f"current {search} is {temp}")


            elif "wheather" in query:
                baseurl = "https://api.openweathermap.org/data/2.5/weather?"
                apikey = "a8acd508d3a8d2dbebce62b167ddccb7"
                city = "Noida"

                url = f"{baseurl}appid={apikey}&q={city}"

                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()

                    def kelvin(kelvin_temp):
                        celsius = kelvin_temp - 273.15
                        fahrenheit = celsius * (9 / 5) + 32
                        return celsius, fahrenheit
                    
                    tempk = data['main']['temp']
                    tempc, tempf = kelvin(tempk)

                    feelslikek = data['main']['feels_like']
                    feelslikec, feelslikef = kelvin(feelslikek)
                    windspeed = data['wind']['speed']
                    humidity = data['main']['humidity']
                    description = data['weather'][0]['description']
                    sunrise = datetime.datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
                    sunset = datetime.datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

                    speak(f"In NOIDA, the temperature is {tempc:.2f} degrees Celsius and feels like {feelslikec:.2f} degrees Celsius. Humidity is {humidity}% and wind speed is {windspeed} km/h. Today's weather is {description}, with sunrise at {sunrise} and sunset at {sunset}.")
                else:
                    print(f"Error fetching weather data: {response.status_code}")

            elif "object detection" in query:
                object_detection()

            elif "open" in query:
                query = query.replace("pheonix","")
                query = query.replace("open","")
                open_application(query)

            elif "doodles" in query:
                ix, iy, k = 200, 200, -1
                def mouse(event, x, y, flags, param):
                    global ix, iy, k
                    if event == cv2.EVENT_LBUTTONDOWN:
                        ix, iy = x, y
                        k = 1
                        

                cv2.namedWindow("draw")
                cv2.setMouseCallback("draw", mouse)

                cap = cv2.VideoCapture(0)


                while True:
                    _, frm = cap.read()

                    frm = cv2.flip(frm, 1)

                    cv2.imshow("draw", frm)

                    if cv2.waitKey(1) == 27 or k == 1:
                        old_gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
                        mask = np.zeros_like(frm)
                        break

                cv2.destroyAllWindows()

                old_pts = np.array([[ix, iy]], dtype=np.float32).reshape(-1,1,2)

                color = (0,255,0)
                c=0
                while True:

                    _, new_frm = cap.read()

                    new_frm = cv2.flip(new_frm, 1)

                    new_gray = cv2.cvtColor(new_frm ,cv2.COLOR_BGR2GRAY)

                    new_pts,status,err = cv2.calcOpticalFlowPyrLK(old_gray, 
                                        new_gray, 
                                        old_pts, 
                                        None, maxLevel=1,
                                        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                                                                        15, 0.08))

                    key = cv2.waitKey(1)

                    if key == ord('e'):
                        mask = np.zeros_like(new_frm)

                    elif key == ord('c'):
                        color = (0,0,0)
                        lst = list(color)
                        c+=1
                        lst[c%3] = 255
                        color = tuple(lst)

                    elif key == ord('g'):
                        pass
                    else:
                        for i, j in zip(old_pts, new_pts):
                            x,y = j.ravel()
                            a, b = i.ravel()

                            cv2.line(mask, (int(a),int(b)), (int(x), int(y)), color, 15)

                    cv2.circle(new_frm, (int(x),int(y)), 3, (255,255,0), 2)


                    
                    new_frm = cv2.addWeighted(new_frm ,0.8, mask, 0.2, 0.1)

                    cv2.imshow("", new_frm)
                    cv2.imshow("drawing", mask)

                    old_gray = new_gray.copy()

                    old_pts = new_pts.reshape(-1,1,2) 

                    if key == ord("q"):
                        break

                cv2.destroyAllWindows()
                cap.release()    

            elif any(word in query for word in ["thumbs up"]):
               thumbs_up()

            elif any(word in query for word in ["add handsign", "add gesture", "add hand sign"]):
                add_gesture_from_user()

            elif any(word in query for word in ["detect handsign", "detect gesture", "detect hand sign"]):
                detect_hand_signs()

            else:
                speak("didn't get that, please try again")

run()
