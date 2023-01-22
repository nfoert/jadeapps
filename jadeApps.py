'''
--------------------------------------------- Welcome to Jade Apps! ---------------------------------------------
If you're here to make your own apps, take a look at the documentation here https://github.com/nfoert/jadeapps
You will need this whole file to make your own apps. This code is what's inside the executable for Jade Apps.
You should not edit any of the below code up until the Apps section. (Other then adding some imports)
'''

# ----------
# Imports
# ----------
'''You can add your own imports here. Some apps may not be compatiable if they're using a large library that makes the final executable incredibly large.'''

from PyQt5 import QtCore, QtGui, uic, QtWidgets
import sys
import assets
import traceback
import os

# Variables

developmental = False # This value should be True if you're running a .py file, or False if you're using pyinstaller to create an .exe

'''VVV  Don't edit anything below!  VVV'''

actions = {}
version_MAJOR = 1
version_MINOR = 0
version_PATCH = 0

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
    print("- Analyse Trigger ---------")
    dataFile = open("../jadeAppsData.txt", "w")
    dataFile.write("loading")
    dataFile.close()
    global actions
    for action in actions:
        for i in actions[action].triggers:
            if i in trigger:
                trigger = trigger.replace(i, "")
                trigger = trigger.strip()
                args = trigger
                print("=====")
                print(args)
                print("=====")
                if actions[action].ui == False:
                    print(f"Found a trigger that matches the action '{actions[action].name}' Now running it. It's not going to start the UI.")
                    actions[action].run(args)
                    break

                elif actions[action].ui == True:
                    print(f"Found a trigger that matches the action '{actions[action].name}' Now running it. It's going to start the UI.")
                    actions[action].run(args)                    
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

# Define apps
'''Define your apps here.'''
nfoert_test_app = nfoert_example("Nfoert's Test", "test", "nfoert", "0.0.1")
nfoert_test_app.init()


'''VVV  Don't edit anything below  VVV'''
# Connections
window_main.nfoert_testapp.clicked.connect(nfoert_test_app.showUi)

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
