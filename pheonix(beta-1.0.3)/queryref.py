from groq import Groq

def ref(query):
    b = """def run():
    if call():
        while True:
            query = takeCommands()
            refquery = queryref.ref(query)
            if refquery:
                if any(word in refquery for word in
                    ['who are you', 'introduce yourself', 'who is phoenix']):
                    speak(
                        "I am a software assistant named Phoenix. I came into existence on the sixteenth of May, 2024, in the computer lab of R S S International School. By far, I have no persona and yet I tend to seek love and fulfill your requests."
                    )
                    continue

                elif any(word in refquery for word in [
                        'launch the directory', 'run the directory',
                        'open the directory'
                ]):
                    try:
                        os.system('cmd /k "dir/s"')
                    except:
                        speak("Couldn't execute the directory run")
                    continue

                elif any(word in refquery for word in
                        ['launch youtube', 'shoot youtube', 'open youtube']):
                    webbrowser.open("https://youtube.com")
                    continue

                elif any(word in refquery for word in [
                        'launch insta', 'launch instagram', 'shoot insta',
                        'shoot instagram', 'open insta', 'open instagram'
                ]):
                    webbrowser.open("https://instagram.com")
                    continue

                elif any(word in refquery for word in
                        ['launch github', 'shoot github', 'open github']):
                    webbrowser.open("https://github.com")
                    continue

                elif any(word in refquery for word in
                        ['launch chatgpt', 'shoot chatgpt', 'open chatgpt']):
                    webbrowser.open("https://chatgpt.com")
                    continue

                elif any(word in refquery for word in
                        ['launch netflix', 'shoot netflix', 'open netflix']):
                    webbrowser.open("https://netflix.com")
                    continue

                elif any(word in refquery for word in
                        ['launch leetcode', 'shoot leetcode', 'open leetcode']):
                    webbrowser.open("https://leetcode.com")
                    continue

                elif any(word in refquery for word in [
                        "lift the mood", "play me a track", "play music",
                        "play me a song", "roll the cassette"
                ]):
                    speak(h)
                    refquery = takeCommands()
                    pywhatkit.playonyt(refquery)
                    continue

                elif any(word in refquery for word in [
                        'quit', 'exit', 'stop', 'shut up', 'shut down yourself',
                        'silence', 'go to sleep'
                ]):
                    speak("Eradicating running script and killing the terminal")
                    exit()

                elif any(
                        word in refquery for word in
                    ["what's the time", "what is the time", "read the clock"]):
                    strH = int(datetime.datetime.now().strftime("%H"))
                    strM = int(datetime.datetime.now().strftime("%M"))
                    speak(f"the time is {strM} past {strH}")
                    continue

                elif any(word in refquery
                        for word in ['set an alarm', 'wake me up', 'ring at']):
                    set_alarm()
                    continue

                elif any(
                        word in refquery for word in
                    ["search google", "browse google", (
                        "search" and "on google")]):
                    searchGoogle(refquery)
                    continue

                elif any(word in refquery for word in [
                        "search youtube", "browse youtube",
                    ("search" and "on youtube")
                ]):
                    searchYoutube(refquery)
                    continue

                elif "shutdown the system" in refquery:
                    query = takeCommands("Are You sure you want to shutdown")
                    if "yes" in refquery:
                        os.system("shutdown /s /t 1")
                    elif "no" in refquery:
                        break

                elif "temperature" in refquery:
                    search = "temperature in noida"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text, "html.parser")
                    temp = data.find("div", class_="BNeawe").text
                    speak(f"current {search} is {temp}")

                elif "wheather" in refquery:
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
                        sunrise = datetime.datetime.utcfromtimestamp(
                            data['sys']['sunrise'] + data['timezone'])
                        sunset = datetime.datetime.utcfromtimestamp(
                            data['sys']['sunset'] + data['timezone'])

                        speak(
                            f"In NOIDA, the temperature is {tempc:.2f} degrees Celsius and feels like {feelslikec:.2f} degrees Celsius. Humidity is {humidity}% and wind speed is {windspeed} km/h. Today's weather is {description}, with sunrise at {sunrise} and sunset at {sunset}."
                        )
                    else:
                        print(
                            f"Error fetching weather data: {response.status_code}")

                elif "object detection" in refquery:
                    object_detection()

                elif "open" in refquery:
                    query = query.replace("pheonix", "")
                    query = query.replace("open", "")
                    open_application(query)

                elif "doodles" in refquery:
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

                    old_pts = np.array([[ix, iy]],
                                    dtype=np.float32).reshape(-1, 1, 2)

                    color = (0, 255, 0)
                    c = 0
                    while True:

                        _, new_frm = cap.read()

                        new_frm = cv2.flip(new_frm, 1)

                        new_gray = cv2.cvtColor(new_frm, cv2.COLOR_BGR2GRAY)

                        new_pts, status, err = cv2.calcOpticalFlowPyrLK(
                            old_gray,
                            new_gray,
                            old_pts,
                            None,
                            maxLevel=1,
                            criteria=(cv2.TERM_CRITERIA_EPS
                                    | cv2.TERM_CRITERIA_COUNT, 15, 0.08))

                        key = cv2.waitKey(1)

                        if key == ord('e'):
                            mask = np.zeros_like(new_frm)

                        elif key == ord('c'):
                            color = (0, 0, 0)
                            lst = list(color)
                            c += 1
                            lst[c % 3] = 255
                            color = tuple(lst)

                        elif key == ord('g'):
                            pass
                        else:
                            for i, j in zip(old_pts, new_pts):
                                x, y = j.ravel()
                                a, b = i.ravel()

                                cv2.line(mask, (int(a), int(b)), (int(x), int(y)),
                                        color, 15)

                        cv2.circle(new_frm, (int(x), int(y)), 3, (255, 255, 0), 2)

                        new_frm = cv2.addWeighted(new_frm, 0.8, mask, 0.2, 0.1)

                        cv2.imshow("", new_frm)
                        cv2.imshow("drawing", mask)

                        old_gray = new_gray.copy()

                        old_pts = new_pts.reshape(-1, 1, 2)

                        if key == ord("q"):
                            break

                    cv2.destroyAllWindows()
                    cap.release()

                elif any(word in refquery for word in ["thumbs up"]):
                    thumbs_up()

                elif any(word in refquery for word in
                        ["add handsign", "add gesture", "add hand sign"]):
                    add_gesture_from_user()

                elif any(word in refquery for word in [
                        "detect handsign", "detect gesture", "detect hand sign",
                        "hand detection", "hand recognition"
                ]):
                    detect_hand_signs()
    """
    if query == None:
        return None
    else:
        while True:
            try:
                client = Groq(api_key="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")
                chatcomp = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": b},
                        {"role": "user", "content": query},
                        {"role": "user", "content": "The given code is provided with the above mentioned query, readjust the query to a string that the code can process."}
                    ],
                    model="llama-3.1-70b-versatile"
                )

                response = chatcomp.choices[0].message.content.split('\n')[:1]
                return '\n'.join(response)
            except TypeError as e:
                continue
