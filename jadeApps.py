# Imports
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import sys
import assets
import traceback
import os

#Variables
actions = {}
developmental = False

# Thanks to ArmindoFlores's answer on Stack Overflow https://stackoverflow.com/questions/51264169/pyinstaller-add-folder-with-images-in-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Classes
class Action:
    '''The Action that triggers functions to run in your App'''
    def __init__(self, name, func, triggers, ui):
        self.name = name
        self.func = func
        self.triggers = triggers
        self.ui = ui
        pass

    def getName(self):
        print(f"my name is {self.name}")

    def run(self):
        self.func()

class App:
    '''An App'''
    def __init__(self, name, simpleName, author, version):
        '''This makes me exist'''
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
        print(f"[{self.name}] > {text}")

    def action(self, name):
        print("Oh hi")

    def addAction(self, name, func, trigger, ui):
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

# Functions
def getAllActions():
    global actions
    print("- Get All Actions ---------")
    print(f"There are a total of {len(actions)} actions")
    for i in actions:
        print(f"    '{actions[i].name}' with triggers '{actions[i].triggers}'")

    print("---------------------------")

def analyseTrigger(trigger):
    print("- Analyse Trigger ---------")
    dataFile = open("../jadeAppsData.txt", "w")
    dataFile.write("loading")
    dataFile.close()
    global actions
    for action in actions:
        for i in actions[action].triggers:
            if i == trigger:
                if actions[action].ui == False:
                    print(f"Found a trigger that matches the action '{actions[action].name}' Now running it. It's not going to start the UI.")
                    actions[action].run()
                    break

                elif actions[action].ui == True:
                    print(f"Found a trigger that matches the action '{actions[action].name}' Now running it. It's going to start the UI.")
                    actions[action].run()                    
                    app.exec()
                    break

            else:
                dataFile = open("../jadeAppsData.txt", "w")
                dataFile.write("no data")
                dataFile.close()
                print("No data for this trigger")
                break

    print("----------------------------")

# -----
# Apps
# -----
class nfoert_test(App):
    '''nfoert's test app'''
    def __init__(self, name, simpleName, author, version):
        super().__init__(name, simpleName, author, version)

    def init(self):
        global developmental
        self.appPrint("Initiating nfoert's test app...")
        self.initUi("main")
        self.ui["main"].button.clicked.connect(self.buttonPress)
        self.addAction("openUi", self.showUi, ["test app show ui"], True)
        self.addAction("someMath", self.doSomeMath, ["do some math", "do some maths please"], False)
        pass

    def showUi(self):
        self.returnData("ui")
        self.ui["main"].show()

    def doSomeMath(self):
        dataOut = 2 * 8
        self.returnData(dataOut)

    def buttonPress(self):
        self.ui["main"].label.setText("Hello, world!")


# Define app
app = QtWidgets.QApplication(sys.argv)

# Define windows
if developmental == True:
    #.py
    window_main = uic.loadUi("ui/jadeapps/main.ui")

elif developmental == False:
    #.exe
    window_main = uic.loadUi(resource_path("jadeapps/main.ui"))

# Define apps
nfoert_test_app = nfoert_test("Nfoert's Test", "test", "nfoert", "0.0.1")
nfoert_test_app.init()

#Connections
window_main.nfoert_testapp.clicked.connect(nfoert_test_app.showUi)

# Start app

try:
    if len(sys.argv) == 1:
        print("ARG: Found start argument")
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
        window_main.show()
        app.exec()

except Exception as e:
    print(f"ARG: No args detected EXCEPT {e}")
    print(traceback.format_exc())
    window_main.show()
    app.exec()
