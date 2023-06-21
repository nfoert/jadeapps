'''
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        This is work by nfoert. If this is in someone else's repo that means they submitted an app to add to the original repo here https://github.com/nfoert/jadeapps
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


--------------------------------------------- Welcome to Jade Apps! ---------------------------------------------
If you're here to make your own apps, take a look at the documentation here https://github.com/nfoert/jadeapps
You will need this whole file to make your own apps. This code is what's inside the executable for Jade Apps.
You should not edit any of the below code up until the Apps section. (Other then adding some imports)

=== PLEASE READ THE COMMENTS! ===
'''


# ----------
# Imports
# ----------
'''You can add your own imports here. Some apps may not be compatiable if they're using a large library that makes the final executable incredibly large.'''

from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import QTimer
from guizero import *
import sys
import assets
import traceback
import os
import webbrowser
from time import sleep
import threading
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import geocoder

# Detect if i'm an .exe or a .py
# Thanks to https://pyinstaller.org/en/stable/runtime-information.html
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    developmental = False
else:
    developmental = True


# Variables
'''VVV  Don't edit anything below!  VVV'''

actions = {}
version_MAJOR = 1
version_MINOR = 0
version_PATCH = 0

guiLoopList = []

# Thanks to ArmindoFlores's answer on Stack Overflow https://stackoverflow.com/questions/51264169/pyinstaller-add-folder-with-images-in-exe-file

def resource_path(relative_path):
    '''This is the function that gets the resources specified in the spec file for a pyinstaller .exe'''
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def writeVersionFile():
        '''This function writes to a version file for the Jade Launcher to read. You do not need to use this or modify it.'''
        global version_MAJOR
        global version_MINOR
        global version_PATCH
        print("Wrting version file...")
        try:
            versionFile = open("JadeAppsVersion.txt", "w")
            versionFile.write(f"{version_MAJOR}\n{version_MINOR}\n{version_PATCH}")
            versionFile.close()
        except:
            print("There was a problem writing the version file.")
        print("Done.")

# Keys
if developmental == True:
    keys = open("keys.txt", "r")
    lines = keys.readlines()
    spotifySecretKey = lines[0].strip()
    openweathermapSecretKey = lines[1].strip()

else:
    keys = open(resource_path("keys.txt"), "r")
    lines = keys.readlines()
    spotifySecretKey = lines[0].strip()
    openweathermapSecretKey = lines[1].strip()


# Classes
class Action:
    '''
    Actions specify the triggers recieved from Jade Assistant that will run your function. 
    For example, you can set a trigger of 'something test app' to run a specific function. eg. doSomeThing(). Then when you tell Jade Assistant to 'something test app' the function
    doSomeThing() will run.
    Check the documentation for how to add actions to your App.
    The final argument specifies if the Action shows a ui. If True it starts up Jade Apps when a trigger is called from Jade Assistant
    '''
    def __init__(self, name, func, triggers, ui):
        self.name = name
        self.func = func
        self.triggers = triggers
        self.ui = ui
        pass

    def getName(self):
        '''Returns the name of the Action'''
        return self.name

    def run(self, args):
        '''Runs the function associated with the action.'''
        self.func(args)

class App:
    '''
    An App is the main basis for your Jade App. You will create a class that inherits from this one and you will have access to important functions to control your App.
    Read the documentation for how to create it https://github.com/nfoert/jadeapps
    '''
    def __init__(self, name, simpleName, author, version):
        self.name = name
        self.author = author
        self.version = version
        self.simpleName = simpleName
        self.appPrint("---------------")
        self.appPrint(f"{self.name}")
        self.appPrint(f"{self.version}")
        self.appPrint("---------------")
        self.ui = {}
        pass

    def appPrint(self, text):
        '''A pretty print for your App.'''
        print(f"[{self.name}] > {text}")

    def addAction(self, name, func, trigger, ui):
        '''Create an Action for your App.'''
        if type(trigger) == list:
            if type(ui) == bool:
                global actions
                actions[name] = Action(name, func, trigger, ui)
                self.appPrint(f"ACTION: Added action '{name}'")

            else:
                self.appPrint(f"ERROR: Please use a boolean instead of {type(ui)} for '{name}'")

        else:
            self.appPrint(f"ERROR: Please use a list instead of {type(trigger)} for '{name}'")

    def returnData(self, data):
        '''Returns some data for Jade Assistant to read.'''
        global developmental
        if developmental == True:
            path = "jadeAppsData.txt"

        elif developmental == False:
            path = "../jadeAppsData.txt"

        data = str(data)
        file = open(path, "w")
        file.write(data)
        file.close()
        self.appPrint(f"Returned some data '{data}' the data was written to '{file.name}'")

    def initUi(self, name):
        '''Creates a UI for your App. (For PyQt5)'''
        global developmental
        global resource_path
        if developmental == True:
            #Run as .py
            if ".ui" in name:
                path = f"./ui/{self.author}_{self.simpleName}/{name}"

            else:
                path = f"./ui/{self.author}_{self.simpleName}/{name}.ui"

        elif developmental == False:
            #Run as .exe
            if ".ui" in name:
                path = resource_path(f"{self.author}_{self.simpleName}/{name}")

            else:
                path = resource_path(f"{self.author}_{self.simpleName}/{name}.ui")

        self.ui[name] = uic.loadUi(path)
        self.appPrint(f"UI: Added ui with name '{name}' and path '{path}'")

# ----------
# Functions
# ----------
def getAllActions():
    '''List all created actions.'''
    global actions
    print("- Get All Actions ---------")
    print(f"There are a total of {len(actions)} actions")
    for i in actions:
        print(f"    '{actions[i].name}' with triggers '{actions[i].triggers}'")

    print("---------------------------")

def analyseTrigger(trigger):
    '''This function reads the input from Jade Assistant and runs the Action associated with it.'''
    ran = False
    print("- Analyse Trigger ---------")
    print(f">>> '{trigger}'")
    dataFile = open("../jadeAppsData.txt", "w")
    dataFile.write("loading")
    dataFile.close()
    global actions
    for item in actions:
        t = actions[item].triggers
        for something in range(len(t)):
            print(f"'{t[something]}' == '{trigger}'")
            if t[something] in trigger:
                

                trigger = trigger.replace(t[something], "")
                trigger = trigger.strip()
                args = trigger
                print("=====")
                print(args)
                print("=====")
                if actions[item].ui == False:
                    print(f"Found a trigger that matches the action '{actions[item].name}' Now running it. It's not going to start the UI.")
                    actions[item].run(args)
                    ran = True
                    break

                elif actions[item].ui == True:
                    print(f"Found a trigger that matches the action '{actions[item].name}' Now running it. It's going to start the UI.")
                    actions[item].run(args)                    
                    app.exec()
                    ran = True
                    break

            else:
                if ran == False:
                    dataFile = open("../jadeAppsData.txt", "w")
                    dataFile.write("no data")
                    dataFile.close()
                    print(f"No data for this trigger > {t[something]}")
                    

                else:
                    print("It ran!")

    print("----------------------------")

# -----
# Apps
# -----
'''
You make your own apps below. Take a look at the example app to get a feel for how it works.
Check out the documentation for instructions. https://github.com/nfoert/jadeapps
'''
class nfoert_example(App):
    '''nfoert's test app'''
    def __init__(self, name, simpleName, author, version):
        super().__init__(name, simpleName, author, version)

    def init(self):
        '''This function is required for an App. It does all the startup stuff to make it work.'''
        global developmental
        self.appPrint("Initiating nfoert's test app...")
        self.initUi("main")
        self.ui["main"].button.clicked.connect(self.buttonPress) #Connect the button in the UI to a function in the App
        self.addAction("openUi", self.showUi, ["test app show ui"], True) #Add action with name 'openUi' function 'self.showUi()' and trigger 'test app show ui' it does open a UI so add a True
        self.addAction("someMath", self.doSomeMath, ["do some math", "do some maths please"], False)
        self.addAction("args", self.argument, ["peanut butter"], False)
        pass

    def showUi(self, args):
        '''This function is an example of one that opens a UI.'''
        print(args)
        self.returnData("ui")
        self.ui["main"].show()

    def doSomeMath(self, args):
        '''This function is an example of one that dosent need a UI, it just returns some data.'''
        try:
            args = args.replace("x", "*")
            args = args.replace("X", "*")
            dataOut = eval(args)
            self.returnData(dataOut)

        except:
            self.returnData(f"Invalid args. '{args}'")

    def argument(self, args):
        '''This function is called with the trigger 'args' and returns everything else in the string.'''
        self.returnData(args)


    def buttonPress(self):
        '''When the button is pressed in the ui, run this function.'''
        self.ui["main"].label.setText("Hello, world!")

class jadeapps_quickgoogle(App):
    '''Jade Apps' quick google app'''
    def __init__(self, name, simpleName, author, version):
        super().__init__(name, simpleName, author, version)

    def init(self):
        '''initialize the application'''
        self.returnData("loading")
        self.appPrint("Initilizing Jade Apps' Quick Google.")
        self.initUi("main")
        self.addAction("googleNoUi", self.googleNoUi, ["google "], False)
        self.addAction("googleUi", self.google, ["google"], True)

        self.ui["main"].google.clicked.connect(self.googleButton)
        self.ui["main"].google.setShortcut("Return")
        
        pass

    def google(self, args):
        self.ui["main"].move(20, 20)
        self.ui["main"].show()
        self.returnData("ui")

    def googleNoUi(self, args):
        webbrowser.open(f"https://www.google.com/search?q={args}&")
        self.returnData(f"I googled '{args}' for you.")

    def googleButton(self):
        if self.ui["main"].text.text() != "":
            if self.ui["main"].open.isChecked():
                text = self.ui["main"].text.text()
                webbrowser.open(f"https://www.google.com/search?q={text}&")
                self.ui["main"].text.setText("")

            else:
                text = self.ui["main"].text.text()
                webbrowser.open(f"https://www.google.com/search?q={text}&")
                self.ui["main"].hide()
                sys.exit()

class jadeapps_spotifyremotecontrol(App):
    '''Jade Apps' Spotify Remote Control app. TODO: This has been disabled for now as I was having trouble adding it. '''
    def __init__(self, name, simpleName, author, version):
        super().__init__(name, simpleName, author, version)

    def initconnections(self):
        self.appPrint("Initilizing Jade Apps' Spotify Remote Control.")
        self.initUi("main")

        self.appPrint("Making UI Connections...")
        self.ui["main"].playpause.clicked.connect(self.playPauseButton)
        self.ui["main"].next.clicked.connect(self.next)
        self.ui["main"].prev.clicked.connect(self.previous)
        self.ui["main"].volume.sliderReleased.connect(self.volumeUpdate)

        # self.appPrint("Adding actions...") TODO: Disabled for now.
        # self.addAction("spotify play", self.playFromJadeAssistant, ["spotify play"], ui=False)
        # self.addAction("play", self.playFromJadeAssistant, ["play"], ui=False)
        # self.addAction("spotify pause", self.pauseFromJadeAssistant, ["spotify pause"], ui=False)
        # self.addAction("pause", self.pauseFromJadeAssistant, ["pause"], ui=False)
        # self.addAction("spotify next", self.nextFromJadeAssistant, ["spotify next"], ui=False)
        # self.addAction("next", self.nextFromJadeAssistant, ["next"], ui=False)
        # self.addAction("spotify skip", self.nextFromJadeAssistant, ["spotify skip"], ui=False)
        # self.addAction("skip", self.nextFromJadeAssistant, ["skip"], ui=False)
        # self.addAction("spotify previous", self.previousFromJadeAssistant, ["spotify previous"], ui=False)
        # self.addAction("previous", self.previousFromJadeAssistant, ["previous"], ui=False)
        # self.addAction("spotify back", self.previousFromJadeAssistant, ["spotify back"], ui=False)
        # self.addAction("back", self.previousFromJadeAssistant, ["back"], ui=False)
        # self.addAction("spotify", self.startFromJadeAssistant, ["spotify"], ui=True)
        # self.addAction("spotify remote control", self.startFromJadeAssistant, ["spotify remote control"], ui=True)
        # self.addAction("music", self.startFromJadeAssistant, ["music"], ui=True)

    def init(self, ui):
        '''Initilize the application'''
        self.appPrint("Initilizing Jade Apps' Spotify Remote Control.")
        self.initUi("main")

        self.appPrint("Making UI Connections...")
        self.ui["main"].playpause.clicked.connect(self.playPauseButton)
        self.ui["main"].next.clicked.connect(self.next)
        self.ui["main"].prev.clicked.connect(self.previous)
        self.ui["main"].volume.sliderReleased.connect(self.volumeUpdate)

        self.appPrint("Signing in...")
        # Get access token from server
        request = requests.get("http://127.0.0.1:8080/spotipy/spotipy")
        
        #If already signed in
        if "Login - Spotify" in request.text:
            req = requests.get("http://127.0.0.1:8080/spotipy/pause")
            print(req)
            reqJson = req.json()
            print(f"===================== {req.text}")
            reqJson = reqJson["access_token"]
            spotipy.CacheFileHandler.save_token_to_cache(reqJson)

            self.sp = spotipy.Spotify(reqJson)

        # Otherwise sign in
        else:
            requestJson = request.json()
            requestJson = requestJson["access_token"]

            self.sp = spotipy.Spotify(requestJson)

        device = self.sp.current_playback()
        try:
            playing = device['is_playing']

            if playing == True:
                self.ui["main"].playpause.setText("||")

            else:
                self.ui["main"].playpause.setText("|>")
        except:
            if ui == False:
                self.returnData("You're not listening to anything. Open Spotify on one of your devices to control it here.")
                pass

        

        if ui == True:
            self.ui["main"].show()
            self.appPrint("Starting thread...")
            updateThreadManager = threading.Thread(target=self.updateThread, daemon=True)
            updateThreadManager.start()

        else:
            self.ui["main"].hide()

        pass

    def updateThread(self):
        self.appPrint("Update thread started.")
        lastName = ""
        while True:
            
            device = self.sp.current_playback()

            # Get values
            try:
                playing = device['is_playing']
                image = device["item"]["album"]["images"][0]["url"]
                name  = device["item"]["name"]

                artist = device["item"]["album"]["artists"][0]['name']
                volume = device['device']['volume_percent']

                deviceName = device['device']['name']

                try:
                    artist2 = device["item"]["album"]["artists"][1]['name']
                    artist2 = ", " + artist2 
                except:
                    artist2 = ""

                try:
                    artist3 = device["item"]["album"]["artists"][2]['name']
                    artist3 = ", " + artist3
                except:
                    artist3 = ""
                
                # Playing
                if playing == True:
                    guiLoopList.append('jadeapps_spotifyremotecontrol_app.ui["main"].playpause.setText("||")')

                else:
                    guiLoopList.append('jadeapps_spotifyremotecontrol_app.ui["main"].playpause.setText("|>")')
                    


                

                #Song title and artists
         
                guiLoopList.append(f'jadeapps_spotifyremotecontrol_app.ui["main"].title.setText("{name}")')
                guiLoopList.append(f'jadeapps_spotifyremotecontrol_app.ui["main"].artist.setText("{artist}{artist2}{artist3}")')

                #Download image
                if name != lastName:
                    self.pixmap = QtGui.QPixmap()
                    guiLoopList.append(f'jadeapps_spotifyremotecontrol_app.ui["main"].image.setPixmap(jadeapps_spotifyremotecontrol_app.pixmap)')
                    self.appPrint("Downloading image...")
                    request = requests.get(image, stream=True)
                    if request.status_code == 200:
                        with open("jadeapps_spotifyremotecontrol_art.png", 'wb') as f:
                            for chunk in request:
                                f.write(chunk)
                            f.close()

                    self.pixmap = QtGui.QPixmap("./jadeapps_spotifyremotecontrol_art.png")
                    guiLoopList.append(f'jadeapps_spotifyremotecontrol_app.ui["main"].image.setPixmap(jadeapps_spotifyremotecontrol_app.pixmap)')
                    
                    self.appPrint("Done!")
                    
                    lastName = name

                #Volume
                self.volume = volume
                guiLoopList.append(f'jadeapps_spotifyremotecontrol_app.ui["main"].volume.setValue(jadeapps_spotifyremotecontrol_app.volume)')

                if deviceName == "iPad" or deviceName == "iPhone":
                    guiLoopList.append('jadeapps_spotifyremotecontrol_app.ui["main"].volume.hide()')

                else:
                    guiLoopList.append('jadeapps_spotifyremotecontrol_app.ui["main"].volume.show()')
                
                # Delay the next loop
                sleep(1)
            
            except:
                self.appPrint("No device active.")
                guiLoopList.append(f'jadeapps_spotifyremotecontrol_app.ui["main"].title.setText("Spotify is not running.")')
                guiLoopList.append(f'jadeapps_spotifyremotecontrol_app.ui["main"].artist.setText("You\'re not listening to anything.")')
                self.pixmap = QtGui.QPixmap()
                guiLoopList.append(f'jadeapps_spotifyremotecontrol_app.ui["main"].image.setPixmap(jadeapps_spotifyremotecontrol_app.pixmap)')
                lastName = ""
                sleep(1)
            
    def pause(self):
        self.appPrint("Paused.")
        self.sp.pause_playback()

    def play(self):
        self.appPrint("Resumed.")
        self.sp.start_playback()

    def next(self):
        self.appPrint("Next song.")
        self.sp.next_track()

    def previous(self):
        self.appPrint("Previous song.")
        self.sp.previous_track()

    def playPauseButton(self):
        device = self.sp.current_playback()
        playing = device['is_playing']
        print(playing)
        if playing == True:
            self.ui["main"].playpause.setText("|>")
            self.pause()

        else:
            self.ui["main"].playpause.setText("||")
            self.play()

    def volumeUpdate(self):
        try:
            self.sp.volume(self.ui["main"].volume.value())
            
        except:
            warningDialog = QtWidgets.QMessageBox()
            warningDialog.setWindowTitle("Spotify Remote Control")
            warningDialog.setText("That device can't be used with the volume slider. Is it IOS?")
            warningDialog.exec()
            self.ui["main"].volume.hide()

    def startFromJadeAssistant(self, args):
        self.returnData("loading")
        self.init(True)
        self.returnData("ui")
        pass
        
    def playFromJadeAssistant(self, args):
        self.returnData("loading")
        self.init(False)
        try:
            print("PLAY")
            self.sp.start_playback()
            self.returnData("Playback started.")

        except:
            self.returnData("I couldn't start playback. Spotify may not be running on any of your devices.")

    def pauseFromJadeAssistant(self, args):
        self.returnData("loading")
        self.init(False)
        try:
            print("PAUSE")
            self.sp.pause_playback()
            self.returnData("Playback paused.")

        except:
            self.returnData("I couldn't pause playback. Spotify may not be running on any of your devices.")

    def nextFromJadeAssistant(self, args):
        self.returnData("loading")
        self.init(False)
        try:
            print("SKIP")
            self.sp.next_track()
            self.returnData("Skipped song.")

        except:
            self.returnData("I couldn't skip that song. Spotify may not be running on any of your devices.")

    def previousFromJadeAssistant(self, args):
        self.returnData("loading")
        self.init(False)
        try:
            print("PREVIOUS")
            self.sp.next_track()
            self.returnData("Previous song.")

        except:
            self.returnData("I couldn't go back a song. Spotify may not be running on any of your devices.")

class jadeapps_weather(App):
    def __init__(self, name, simpleName, author, version):
        super().__init__(name, simpleName, author, version)

    def init(self):
        '''Initilize the application'''
        self.appPrint("Initlizing Jade Apps' Weather.")
        self.initUi("main")
        self.ui["main"].refresh.clicked.connect(self.getLocation)
        self.ui["main"].locationButton.clicked.connect(self.switchLocation)
        self.addAction("currenttemp", self.currentTemp, ["current temp", "temp", "temparature", "current temprature"], False)
        self.addAction("hightemp", self.highTemp, ["high temp", "high temprature", "high"], False)
        self.addAction("lowtemp", self.lowTemp, ["low temp", "low temprature", "low"], False)
        self.addAction("openweather", self.showUiTrigger, ["weather", "show me the weather", "what's the weather", "tell me the weather"], True)

    def showUi(self):
        window_main.hide()
        self.getLocation()
        self.ui["main"].show()

    def showUiTrigger(self, args):
        self.returnData("loading")
        self.getLocation()
        self.ui["main"].move(20, 20)
        self.ui["main"].show()
        
        self.returnData("ui")

    def getLocation(self):
        try:
            location = geocoder.ip("me")
            latitude = location.latlng[0]
            longitude = location.latlng[1]

            self.ui["main"].locationText.setText(f"{location.city}, {location.state}")

            self.getWeather(latitude, longitude, location)
        except:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Weather by Jade Apps")
            box.setText("There was a problem getting your current location! Are you connected to the internet?")
            box.setIcon(QtWidgets.QMessageBox.Critical)
            box.show()
            box.exec()
            
            
            sys.exit()

        
    def switchLocation(self):
        text = self.ui["main"].locationEnter.text()

        try:
            location = geocoder.arcgis(text)
            if "ERROR" in str(location):
                box = QtWidgets.QMessageBox()
                box.setWindowTitle("Weather by Jade Apps")
                box.setText("That location could not be found!")
                box.setIcon(QtWidgets.QMessageBox.Warning)
                box.show()
                box.exec()

                self.ui["main"].locationEnter.setText("")

            else:
                latitude = location.latlng[0]
                longitude = location.latlng[1]

                self.ui["main"].locationEnter.setText("")
                self.ui["main"].locationText.setText(text)

                self.getWeather(latitude, longitude, location)

        except:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Weather by Jade Apps")
            box.setText("There was a problem getting that location! Are you connected to the internet?")
            box.setIcon(QtWidgets.QMessageBox.Critical)
            box.show()
            box.exec()
            
            sys.exit()


    def getWeather(self, latitude, longitude, location):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={openweathermapSecretKey}&units=imperial"
        try:
            openWeatherMapRequest = requests.get(url)
            openWeatherMapRequest.raise_for_status()
            openWeatherMapRequestJson = openWeatherMapRequest.json()

        except:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Weather by Jade Apps")
            box.setText("There was a problem getting that location! Are you connected to the internet?")
            box.setIcon(QtWidgets.QMessageBox.Critical)
            box.show()
            box.exec()
            
            sys.exit()

        weather = openWeatherMapRequestJson["weather"]
        state = weather[0]["main"]
        icon = weather[0]["icon"]

        temp = openWeatherMapRequestJson["main"]
        current = temp["temp"]
        low = temp["temp_min"]
        high = temp["temp_max"]

        iconUrl = f"https://openweathermap.org/img/wn/{icon}@2x.png"
        iconRequest = requests.get(iconUrl)
        with open("jadeapps_weather_icon.png", "wb") as f:
            f.write(iconRequest.content)

        pixmap = QtGui.QPixmap("jadeapps_weather_icon.png")
        self.ui["main"].icon.setPixmap(pixmap)

        # Thanks to tzot's anwser here https://stackoverflow.com/questions/3215168/how-to-get-character-in-a-string-in-python
        degree_sign = u'\N{DEGREE SIGN}'
        self.ui["main"].state.setText(state)
        self.ui["main"].temp.setText(f"{current}{degree_sign}F.")
        self.ui["main"].highLow.setText(f"{high}{degree_sign}F. / {low}{degree_sign}F.")

    def connectionCheck(self):
        try:
            google = requests.get("https://google.com")
            google.raise_for_status()
            self.appPrint("You're connected!")

        except:
            self.appPrint("You're not connected!")
            self.returnData("You're not connected to the internet.")

    def currentTemp(self, args):
        global openweathermapSecretKey
        self.returnData("loading")
        self.connectionCheck()
        location = geocoder.ip("me")
        latitude = location.latlng[0]
        longitude = location.latlng[1]

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={openweathermapSecretKey}&units=imperial"
        try:
            openWeatherMapRequest = requests.get(url)
            openWeatherMapRequest.raise_for_status()
            openWeatherMapRequestJson = openWeatherMapRequest.json()

        except:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Weather by Jade Apps")
            box.setText("There was a problem getting that location! Are you connected to the internet?")
            box.setIcon(QtWidgets.QMessageBox.Critical)
            box.show()
            box.exec()
            
            sys.exit()
    
        temp = openWeatherMapRequestJson["main"]
        current = temp["temp"]

        # Thanks to tzot's anwser here https://stackoverflow.com/questions/3215168/how-to-get-character-in-a-string-in-python
        degree_sign = u'\N{DEGREE SIGN}'
        self.returnData(f"The current temparature in {location.city}, {location.state} is {current}{degree_sign}F.")


    def highTemp(self, args):
        global openweathermapSecretKey
        self.returnData("loading")
        self.connectionCheck()
        location = geocoder.ip("me")
        latitude = location.latlng[0]
        longitude = location.latlng[1]

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={openweathermapSecretKey}&units=imperial"
        openWeatherMapRequest = requests.get(url)
        openWeatherMapRequestJson = openWeatherMapRequest.json()
    
        temp = openWeatherMapRequestJson["main"]
        high = temp["temp_max"]

        # Thanks to tzot's anwser here https://stackoverflow.com/questions/3215168/how-to-get-character-in-a-string-in-python
        degree_sign = u'\N{DEGREE SIGN}'
        self.returnData(f"The high temparature today in {location.city}, {location.state} is {high}{degree_sign}F.")

    def lowTemp(self, args):
        global openweathermapSecretKey
        self.returnData("loading")
        self.connectionCheck()
        location = geocoder.ip("me")
        latitude = location.latlng[0]
        longitude = location.latlng[1]

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={openweathermapSecretKey}&units=imperial"
        openWeatherMapRequest = requests.get(url)
        openWeatherMapRequestJson = openWeatherMapRequest.json()
    
        temp = openWeatherMapRequestJson["main"]
        low = temp["temp_min"]

        # Thanks to tzot's anwser here https://stackoverflow.com/questions/3215168/how-to-get-character-in-a-string-in-python
        degree_sign = u'\N{DEGREE SIGN}'
        self.returnData(f"The low temparature today in {location.city}, {location.state} is {low}{degree_sign}F.")



'''VVV  Don't edit anything in this section  VVV'''

# Define app
app = QtWidgets.QApplication(sys.argv)

# Define windows for the app
if developmental == True:
    #.py
    window_main = uic.loadUi("ui/jadeapps/main.ui")

elif developmental == False:
    #.exe
    window_main = uic.loadUi(resource_path("jadeapps/main.ui"))

'''^^^  Don't edit anything in this section  ^^^'''

# Start print
print("--------------------")
print("Jade Apps")
print(f"Version {version_MAJOR}.{version_MINOR}.{version_PATCH}")
print("--------------------")

# Define apps
'''Define your apps here.'''
nfoert_example_app = nfoert_example("Nfoert's Example", "example", "nfoert", "0.0.1")
nfoert_example_app.init()

jadeapps_quickgoogle_app = jadeapps_quickgoogle("Jade Apps' Quick Google", "quickgoogle", "jadeapps", "0.0.1")
jadeapps_quickgoogle_app.init()

jadeapps_spotifyremotecontrol_app = jadeapps_spotifyremotecontrol("Jade Apps' Spotify Remote Control", "spotifyremotecontrol", "jadeapps", "0.0.1")
jadeapps_spotifyremotecontrol_app.initconnections()

jadeapps_weather_app = jadeapps_weather("Jade Apps' Weather", "weather", "jadeapps", "0.0.1")
jadeapps_weather_app.init()


'''VVV  Don't edit anything below. I'll add your app icon to the main UI for you. VVV'''
# Connections
def jadeapps_spotifyremotecontrol_app_init_true():
    jadeapps_spotifyremotecontrol_app.init(True)

window_main.nfoert_testapp.clicked.connect(nfoert_example_app.showUi)
window_main.nfoert_testapp.hide() # Hidden so non-devs can't see it
window_main.jadeapps_quickgoogle.clicked.connect(jadeapps_quickgoogle_app.google)
window_main.jadeapps_spotifyremotecontrol.clicked.connect(jadeapps_spotifyremotecontrol_app_init_true)
window_main.jadeapps_spotifyremotecontrol.hide() #TODO: REIMPLEMENT
window_main.jadeapps_weather.clicked.connect(jadeapps_weather_app.showUi)

# Gui Loop
def guiLoop():
    '''Sometimes you need to change your UI in another thread. You can use the Gui Loop to do so. Appending instructions to the guiLoopList will then execute them inside the PyQt main thread.'''
    global guiLoopList
    if len(guiLoopList) >= 1:
        try:
            print(f"guiLoop: Running code '{guiLoopList[0]}'")
            exec(guiLoopList[0])
            guiLoopList.remove(guiLoopList[0])

        except Exception as e:
            print(f"guiLoop: There was a problem running some code! {e}")
            guiLoopList.remove(guiLoopList[0])
            print(f"The gui loop had a problem running some code! code >>'{guiLoopList[0]}'<< '{e}'")

guiLoopTimer = QTimer()
guiLoopTimer.timeout.connect(guiLoop)
guiLoopTimer.start(1)

''' >>> guiLoopList.append("nfoert_example_app.ui['main'].show()") <<< How to call your UI with the gui loop '''

# Start app
# This bit of code checks the arguments recived and puts Jade Apps in the correct mode.

try:
    if len(sys.argv) == 1:
        print("ARG: Found start argument")
        writeVersionFile()
        window_main.show()
        app.exec()

    elif sys.argv[1] == "analyse":
        print("ARG: Found analyse argument")
        analyseTrigger(sys.argv[2])
        print("Done Analysing")
        

    elif sys.argv[1] == "help":
        print("-----")
        print("Jade Apps Arguments")
        print("    - 'jadeApps.exe help' to show this message")
        print("    - 'jadeApps.exe start' to start the app")
        print("    - 'jadeApps.exe analyse <trigger>' to check all actions for the trigger and run the function if it has a match")
        print("-----")

    else:
        print("ARG: No args detected")
        writeVersionFile()
        window_main.show()
        app.exec()

except Exception as e:
    print(f"ARG: No args detected EXCEPT {e}")
    print(traceback.format_exc())
    writeVersionFile()
    window_main.show()
    app.exec()
