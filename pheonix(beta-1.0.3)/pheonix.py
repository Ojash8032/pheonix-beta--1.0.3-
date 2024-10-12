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
import threading

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

def takeCommands(retry=False, fallback=False):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if retry:
            speak("I didn't catch that, please repeat.")
        else:
            speak("Please state your query.")
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"Recognized command: {query}")
            return query.lower()
        except sr.UnknownValueError:
            if fallback:
                speak("Voice recognition failed. Please type your request.")
                query = input("Please type your query: ")
                return query.lower()
            else:
                speak("Sorry, I didn't understand that.")
                return takeCommands(retry=True, fallback=True)
        except sr.RequestError:
            speak("There is an issue with the recognition service. Please try again later.")
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
    if "google" in query:
        import wikipedia as googleScrap  # type: ignore
        query = query.replace("pheonix", "")
        query = query.replace("google search", "")
        query = query.replace("google", "")
        speak("This is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query, 1)
            speak(result)
        except:
            speak("No speakable output available")

def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!")
        query = query.replace("youtube search", "")
        query = query.replace("youtube", "")
        query = query.replace("pheonix", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")

def latestnews():
    # Define the news categories and corresponding API URLs
    api_dict = {
        "business": "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=your_api_key",
        "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=your_api_key",
        "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=your_api_key",
        "science": "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=your_api_key",
        "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=your_api_key",
        "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=your_api_key"
    }

    # Ask the user which category of news they want
    speak("Which field of news do you want? You can choose from business, entertainment, health, science, sports, or technology.")
    field = takeCommands()

    while field not in api_dict:
        speak("Please choose a valid category.")
        field = takeCommands()

    url = api_dict.get(field)
    if url:
        news = requests.get(url).json()
        articles = news.get("articles")

        if articles:
            index = 0
            while index < len(articles):
                article = articles[index]
                title = article.get("title")
                speak(f"News {index + 1}: {title}")
                news_url = article.get("url")
                speak(f"More info at: {news_url}")

                speak("Would you like to hear the next news, stop, or repeat this one?")
                silq = sylcommand()

                if "stop" in silq:
                    speak("That's all for the news.")
                    break
                elif "next" in silq:
                    index += 1
                elif "repeat" in silq:
                    continue
                else:
                    speak("I didn't understand that.")
        else:
            speak("No news articles found.")
    else:
        speak("Invalid category. Please try again.")

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
        if os.name == 'nt': 
            subprocess.Popen(f'start {app_name}', shell=True)
        elif os.name == 'posix':
            if "darwin" in os.sys.platform: 
                subprocess.Popen(['open', '-a', app_name])
            else:  
                subprocess.Popen([app_name])
    except Exception as e:
        speak(f"Sorry, I couldn't open {app_name}. Please try again.")
        print(e)


def object_detection():
    speak("Starting object detection. Please wait.")
    
    model = YOLO('yolov8n.pt')

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

        cv2.imshow("YOLOv8 Object Detection", img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    speak("Object detection ended.")


class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy, lm.z))
        return lmList

def save_sign(name, landmarks):
    saved_signs[name] = landmarks
    with open('hand_signs.json', 'w') as file:
        json.dump(saved_signs, file, indent=4)
    print(f"Sign '{name}' saved with landmarks.")

def recognize_sign(landmarks):
    for sign_name, sign_landmarks in saved_signs.items():
        if np.allclose(np.array(sign_landmarks), np.array(landmarks), atol=0.1):
            return sign_name
    return None

try:
    with open('hand_signs.json', 'r') as file:
        saved_signs = json.load(file)
except FileNotFoundError:
    saved_signs = {}

def main(sign_name=None):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        exit()

    detector = handDetector()
    ptime = 0

    while True:
        success, img = cam.read()
        if not success:
            print("Failed to capture image")
            continue

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if lmList:
            landmarks = [(lm[0] / img.shape[1], lm[1] / img.shape[0], lm[2]) for lm in lmList]
            
            recognized_sign = recognize_sign(landmarks)
            if recognized_sign:
                cv2.putText(img, recognized_sign, (10, 150), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (0, 255, 0), 3)
            else:
                cv2.putText(img, "Unknown", (10, 150), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (0, 0, 255), 3)
                if sign_name and cv2.waitKey(1) & 0xFF == ord('s'):
                    save_sign(sign_name, landmarks)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (225, 0, 225), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

while True:
    query = takeCommands()

    if query:
        if any(word in query for word in ['who are you', 'introduce yourself', 'who is phoenix']):
            speak("I am a software assistant named Phoenix. I came into existence on the sixteenth of May, 2024, in the computer lab of R S S International School. By far, I have no persona and yet I tend to seek love and fulfill your requests.")
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ['launch the directory', 'run the directory', 'open the directory']):
            query = takeCommands()
            try:
                os.system('cmd /k "dir/s"')
            except:
                speak("Couldn't execute the directory run")
            silq = sylcommand()
            stop(silq)

        elif "wikipedia" in query:
            speak("Fetching data from Wikipedia...")
            query = query.replace("wikipedia", '')
            results = wikipedia.summary(query, sentences=4)
            speak("According to Wikipedia...")
            speak(results)
            print(results)
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ['launch youtube', 'shoot youtube', 'open youtube']):
            webbrowser.open("https://youtube.com")
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ['launch insta', 'launch instagram', 'shoot insta', 'shoot instagram', 'open insta', 'open instagram']):
            webbrowser.open("https://instagram.com")
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ['launch github', 'shoot github', 'open github']):
            webbrowser.open("https://github.com")
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ['launch chatgpt', 'shoot chatgpt', 'open chatgpt']):
            webbrowser.open("https://chatgpt.com")
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ['launch netflix', 'shoot netflix', 'open netflix']):
            webbrowser.open("https://netflix.com")
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ['launch leetcode', 'shoot leetcode', 'open leetcode']):
            webbrowser.open("https://leetcode.com")
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ["lift the mood", "play me a track", "play music", "play me a song", "roll the cassette"]):
            speak(h)
            query = takeCommands()
            pywhatkit.playonyt(query)
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ['quit', 'exit', 'stop', 'shut up', 'shut down yourself', 'silence', 'go to sleep']):
            speak("Eradicating running script and killing the terminal")
            exit()
    
        elif any(word in query for word in ["what's the time", "what is the time", "read the clock"]):
            strH = int(datetime.datetime.now().strftime("%H"))
            strM = int(datetime.datetime.now().strftime("%M"))
            speak(f"the time is {strM} past {strH}")
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ['set an alarm', 'wake me up', 'ring at']):
            set_alarm()
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ["search google", "browse google", ("search" and "on google")]):
            searchGoogle(query)
            silq = sylcommand()
            stop(silq)

        elif any(word in query for word in ["search youtube", "browse youtube", ("search" and "on youtube")]):
            searchYoutube(query)
            silq = sylcommand()
            stop(silq)

        elif "news" in query:
            latestnews()
            silq = sylcommand()
            stop(silq)

        elif "shutdown the system" in query:
            speak("Are You sure you want to shutdown")
            silq = sylcommand()
            if "yes" in silq:
                os.system("shutdown /s /t 1")
            elif "no" in silq:
                break

        elif "temperature" in query:
            search = "temperature in noida"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            speak(f"current {search} is {temp}")
            silq = sylcommand()
            stop(silq)

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
            stop(sylcommand())

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

        elif any(word in query for word in ['hand detection', 'hand sign', 'sign recognition']):
            speak("Please provide the name for the new hand sign or say 'none' if not saving.")
            sign_name = takeCommands()
            if "none" or "no" or "nope" or "" or " "in sign_name.lower() :
                sign_name = None
            main(sign_name)
        
