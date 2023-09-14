#Simple Voice Assistant - built in commands; no GPT
# Requirements: pip install wolframalpha wikipedia SpeechRecognition pyttsx3 requests

import re
import datetime
import webbrowser
import os
import requests
import speech_recognition as sr
import pyttsx3
import wolframalpha
import wikipedia
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Set default VOICE!!!
siri_voice = "com.apple.speech.synthesis.voice.samantha"
#siri_voice= "com.apple.speech.synthesis.voice.tom"  #male

# Set rate and volume
#engine.setProperty('rate', 150)  # Experiment with this
engine.setProperty('volume', 1.0)  # Max volume
engine.setProperty('voice', siri_voice)
#engine.setProperty('voice', voices[1].id)

#Say it and wait
def speak(text):
    engine.say(text)
    engine.runAndWait()

#listen
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")

        #noice reduction 
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000
               
        audio = recognizer.listen(source) #(src, timeout=5.0)) for timeout reduction
        try:
            query = recognizer.recognize_google(audio, language='en')
            print(f"User said: {query}")
        except Exception as e:
            print("Sorry, could not recognize your voice.")
            return "Null"
        return query.lower()

#should add API later 
def get_bulgarian_news():
    global API
    url = f"https://newsapi.bg/apiKey={API}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get("articles")
    if articles:
        for i, article in enumerate(articles[:5], 1):
            print(f"{i}. {article.get('title')}")
            speak(f"{i}. {article.get('title')}")
            #should test
            return f"{i}. {article.get('title')}"
            
# save conversation data
def log_conversation(query, response):
    with open("conversation_log_vision.txt", "a") as file:
        if query != 'Null':
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - User: {query[0].upper() + query[1:]}\n")
            file.write(f"{timestamp} - Vision: {response}\n")
        
# Using regex to extract the numbers
def basic_calculator(query):
    try:
        if '+' in query:
            numbers = [int(num) for num in re.findall(r'\d+', query)]
            return sum(numbers)
        elif '-' in query:
            numbers = [int(num) for num in re.findall(r'\d+', query)]
            return numbers[0] - numbers[1]
        elif 'x' in query or '*' in query:
            numbers = [int(num) for num in re.findall(r'\d+', query)]
            return numbers[0] * numbers[1]
        elif '/' in query:
            numbers = [int(num) for num in re.findall(r'\d+', query)]
            if numbers[1] == 0:
                return "Cannot divide by zero."
            return numbers[0] / numbers[1]
        elif '%' in query or 'remainder' in query:
            numbers = [int(num) for num in re.findall(r'\d+', query)]
            result = numbers[0] % numbers[1]
            return f"The Remainder part is {result}"
    except Exception as e:
        return f"Error {e}."



#run response happens inside the whule loop
def main():
    
    global response
    
    speak("Hi, how can I assist you?")
    
    while True:
        #lower case commands 
        query = take_command().lower()

        # Checking for the wake word "vision"
        if "vision" not in query:
            print("Wake word not in query.")
            pass
            #continue 
            #Use continue to try to listen again... disabled for testing purposes
            #or choose a method to stop listen or just bring all statements under this check 
            
        # Removing wake word from the query
        query = query.replace("vision", "").strip()
    
        
        # Should be able to cut the bot so it doesnt read the full article or set limit to 2 sentences 
        if "wikipedia" in query:
            search_term = query.replace("wikipedia", "")
            results = wikipedia.summary(search_term, sentences=2)
            speak(f"According to Wikipedia: {results}")
            response = f"According to Wikipedia: {results}"
            
        elif "tell a joke" in query:
            speak(f"You are funny!")
            response = f"You are funny!"

        elif "destroy the world" in query:
            speak("Sorry, can't do this yet.")
            response = "Sorry, can't do this yet."
        
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("Confirmative")
            response = "Confirmative"

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("Confirmative")
            response = "Confirmative"

        elif 'current time' in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {current_time}")
            response = f"The current time is {current_time}"

        elif 'open chrome' in query:
            os.system("open /Applications/Google\\ Chrome.app")
            speak("Confirmative")
            response = "Confirmative"

        elif 'how are you' in query:
            speak("I'm fine, thank you for asking. How are you?")
            response = "I'm fine, thank you for asking. How are you?"

        elif 'what is your name' in query:
            speak("I am your voice assistant, Vision.")
            response = "I am your voice assistant, Vision."
        elif 'who made you' in query:
            speak("I was created by Filip.")
            response = "I was created by Filip."

        elif 'news' in query:
            speak("Fetching top Bulgarian news.")
            get_bulgarian_news()
            response = "Fetching top Bulgarian news:" + str(get_bulgarian_news())

        # You can use custom function as well
        # elif 'calculate' in query:
        #     app_id = "YOUR_WOLFRAMALPHA_APP_ID"
        #     client = wolframalpha.Client(app_id)
        #     index = query.find('calculate')
        #     search_query = query[index + 9:]
        #     result = client.query(search_query)
        #     answer = next(result.results).text
        #     speak(f"The answer is {answer}")

        elif any(op in query for op in ['+', '-', 'x', '/', '%', 'remainder']):
            solution = basic_calculator(query)
            speak(f"The answer is {solution}")
            response = f"The answer is {solution}"
        

        elif 'search for' in query:
            speak("Here is what I found.")
            webbrowser.open("https://www.google.com/search?q={}".format(query))
            response = "Opening Google Search..."
        
        
        elif 'bye' in query:
            speak("Goodbye!")
            response = "GoodBye!"
            #exit
            break
        
        else:
            speak("Can you say that again?")
            
        log_conversation(query, response)

if __name__ == "__main__":
    main()
