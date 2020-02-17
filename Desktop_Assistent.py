import datetime
import requests
import random
import sys
import speech_recognition as sr
import os
import webbrowser
import smtplib
import urllib
from PyDictionary import PyDictionary
from pygame import mixer
import ety
from nltk.corpus import wordnet
import pyttsx3

# Starting the pyttsx3 engine
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 1].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', rate-62)


# Talk To Me Function
def TalkToMe(audio):
    print("Addy: " + audio)
    engine.say(audio)
    engine.runAndWait()

# Listen To Commend
def MyCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language = "en-in")
        print("User : " + command + '\n')
    #Loop back to continue to listen for command
    except sr.UnknownValueError:
        TalkToMe('Sorry ! I did not get that. Could you please type it out ?')
        command = str(input('Command: '))
    return command

""" ====================== Functions for executing the command ========================="""

# Greeting Function
def greeting():
    currentTime = int(datetime.datetime.now().hour)
    if(currentTime >= 0 and currentTime < 12):
        TalkToMe("Good Morning!")
    if(currentTime >= 12 and currentTime < 17):
        TalkToMe("Good Afternoon!")
    if(currentTime >= 17 and currentTime != 0):
        TalkToMe("Good Evening!")

# Play Music/Song Function
def playMusic():
    music_folder = r"D:\songs"
    music = os.listdir(music_folder)
    random_music = music_folder + random.choice(music)
    mixer.init()
    mixer.music.load(random_music)
    mixer.music.play()

# Function for Displaying complete info of a word
def getCompleteInfo(word):
    dictionary = PyDictionary()
    mean = {}
    mean = dictionary.meaning(word)
    synonyms = []
    antonyms = []

    TalkToMe("Alright. Here is the information you asked for.")

    for key in mean.keys():
        TalkToMe("When " + str(word) + " is used as a " + str(key) + " then it has the following meanings")
        for val in mean[key]:
            print(val)
        print()

    TalkToMe("The possible synonyms and antonyms of " + str(word) + " are given below.")
    for syn in wordnet.synsets(word):
        for i in syn.lemmas():
            if(i.name() not in synonyms):
                synonyms.append(i.name())
            if(i.antonyms() and i.antonyms()[0].name() not in antonyms):
                antonyms.append(i.antonyms()[0].name())
    print("Synonyms: ", end = " ")
    print(" ".join(synonyms), end = " ")
    print("\n")
    print("Antonyms: ", end = " ")
    print(" ".join(antonyms), end = " ")
    print("\n")

    ori = ety.origins(word)
    if(len(ori) > 0):
        TalkToMe("There are " + str(len(ori)) + " possible origins found.")
        for origin in ori:
            print(origin)
    else:
        TalkToMe("I'm sorry. No data regarding the origin of " + str(word) + " was found.")

# Function for finding file in System
def find(name, path):
    for root, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

# Function for googleSearch 
def searchOnGoogle(command, outputlist):
    try:
        from googlesearch import search
    except ImportError:
        TalkToMe("No module named 'google' found")
    TalkToMe("The top five search results from Google are Listed below.")
    for output in search(command, tld = "co.in", num = 10, stop = 5, pause = 2):
        print(output)
        outputlist.append(output)
    return outputlist


# Function for open a perticuler link in webbrowser
def openLink(outputlist):
    TalkToMe("Here's the first link for you.")
    webbrowser.open(outputlist[0])


# Function for open youtube
def playOnYoutube(command_string):
    command_string = urllib.parse.urlencode({"search_command" : command})
    search_string = str("http://www.youtube.com/results?" + command_string)
    TalkToMe("Here's what you asked for. Enjoy!")
    webbrowser.open_new_tab(search_string)

# Function for Joke
def tellAJoke():
    res = requests.get('https://icanhazdadjoke.com/',
        headers={"Accept":"application/json"})

    if(res.status_code == 200):
        TalkToMe("Okay. Here's one")
        TalkToMe(str(res.json()['joke']))
    else:
        TalkToMe("Oops! I run out of jokes")


greeting()
TalkToMe('Addy here.')
TalkToMe('What would you like me to do for you ?')


# Driver code for handling commands

if __name__ == '__main__':
    while True:

        command = MyCommand()
        command = command.lower()

        if('play music' in command or 'play a song' in command or 'song' in command):
            TalkToMe("Here's your music. Enjoy !")
            playMusic()
        
        if('stop the music' in command or 'stop the song' in command or 'stop song' in command or 'stop' in command):
            mixer.music.stop()
            TalkToMe("The music is stopped. Thank you")

        if('find file' in command):
            TalkToMe("What is the name of the file that I should find ?")
            command = MyCommand()
            filename = command
            print(filename)
            TalkToMe("What should br the extension of the file ?")
            command = MyCommand()
            command = command.lower()
            extension = command
            print(extension)
            fullname = str(filename) + '.' + str(extension)
            print(fullname)
            path = r'D:\\'
            location = find(fullname, path)
            TalkToMe("File is found at the below location")
            print(location)

        if('search' in command):
            outputlist = []
            TalkToMe("What should I search for ?")
            command = MyCommand()
            searchOnGoogle(command, outputlist)
            TalkToMe("Sholud I open up the first link for you ?")
            command = MyCommand()
            if('yes' in command or 'sure' in command):
                openLink(outputlist)
            if('no' in command):
                TalkToMe("Alright.")

        if('play on youtube' in command or 'youtube' in command):
            TalkToMe("What should I look up for ?")
            command = MyCommand()
            playOnYoutube(command)

        if('open dictionary' in command or 'dictionary' in command or 'meaning' in command):
            TalkToMe("What word should I look up for ? ")
            word = MyCommand()
            getCompleteInfo(word)

        if('joke' in command or 'tell me a joke' in command):
            tellAJoke()

        if('that would be all' in command or 'that is it' in command or 'bye Addy' in command):
            TalkToMe("Alright. Have a nice day")
            TalkToMe("Byeee")
            sys.exit() 
