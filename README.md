# Jade Apps

Welcome to Jade Apps! Jade Apps allows you to get information and control tasks like getting weather data and starting timers. It's integrated into Jade Assistant.

Jade Apps will also be able to get user-added apps. The process is fairly straightforward and is explained in detail below.

<a href="https://nfoert.pythonanywhere.com/jadesite/jadelauncher"><img src="launcher.png" width="200"></a>

## Adding your own apps to Jade Apps
---
This assumes that you know how to program in Python, have an understanding of functions and classes and have had experience in GUI programming. Jade Apps supports both [PyQt5](https://pypi.org/project/PyQt5/) and [guizero](https://lawsie.github.io/guizero/about/) for your App's GUI.

I reccomend using `PyQt5` for more complicated GUIs, but it's quite complicated in itself so if you're new to GUI programming, you should use `guizero` as it's quick and easy to get started with.
If you use `PyQt5` you should create your UIs with [Qt Designer](https://build-system.fman.io/qt-designer-download). Having an interface to make your UIs makes it easier to visualize how it's going to look. Additionally this helps keep the code cleaner and Jade Apps is built with a system to quickly and easily set up a .ui file created in `Qt Designer`.

### Getting started
---
To start, make sure you have [Python](https://www.python.org/) installed.

Then, create a new directory somewhere and create a new virtual enviroment. (`python -m venv .venv`) if you're using [Visual Studio Code](https://code.visualstudio.com/) you can quickly activate your new virtual enviroment by using the Python Interpreter selector in the bottom right hand corner. Otherwise run these commands to activate your new virtual enviroment
-  `./.venv/Scripts/activate.ps1` on Windows with PowerShell
-  `.\.venv\Scripts\activate` on Windows with the command prompt
-  `source ./.venv/bin/activate` on Mac or Linux

If it activated you'll see `(.venv)` at the beginning of your command prompt.

If you've never used virtual enviroments before, they're basically a seperate area from your main Python installation that you can install packages to.
Jade Apps requires two packages that's not in the Python standard library. `PyQt5`, `guizero` and `pyinstaller`. Run these commands to install them.
- `pip install PyQt5`
- `pip install guizero`
- `pip install pyinstaller`

Provided there were no problems, you should be good to go with your virual enviroment. If you're planning on using PyQt5, you should install [Qt Designer](https://build-system.fman.io/qt-designer-download) now.<br>
Next, you should download the project files in this repo. Either click the green '`<> Code`' button and click `Download ZIP`, then unzip it to the project directory you made, or use the `git` command line tool and run `git clone https://github.com/nfoert/jadeapps` to get the files in your directory. (Installing git is a pain unless you're on Linux where it's included. For Windows use [Git for Windows](https://git-scm.com/) and for mac you'll need to use [Homebrew](https://brew.sh/))

Once you have the files in your directory, you're done with setup, **it's time to code.**

### Making your Jade App
---
Take a look at the files. You'll see a structure sort of like this:
```
|   assets.py                   # 'compiled' assets file. Used for images when using PyQt5 and Qt Designer
│   assets.qrc                  # The assets file for Qt Designer to read from
│   Jade Apps.exe               # The executable file that the Jade Launcher downloads (Please delete me!)
│   jadeApps.py                 # The main Python file
│   jadeApps.spec               # The spec file used when converting jadeApps.py to a executable
│   README.md                   # This README
│
├───assets                      # This folder is where assets like images, sounds and animations are stored
│   ├───jadeapps                # Assets for the main Jade Apps program are stored here
│   │       background.png      # Background image for the main screen
│   │       blankicon.png       # A template for creating your own app icons
│   │
│   └───nfoert_example          # Assets for the app 'nfoert's example'
│           icon.png            # The icon for 'nfoert's example'
│
└───ui                          # UIs for all apps are stored here (If you're using Qt Designer)
    ├───jadeapps                # UIs for the main Jade Apps part
    │       main.ui             # The main screen
    │
    └───nfoert_example          # UIs for the app 'nfoert's example'
            main.ui             # The main UI
```

You should delete 'Jade Apps.exe' as you'll be creating your own executable later with `pyinstaller` and `jadeApps.spec`. It's only for the Jade Launcher to be able to download Jade Apps.

You'll be adding code to jadeApps.py. You'll also be adding files to the 'assets' directory and the 'ui' directory.

You can take a look at the `nfoert_example` app in the jadeApps.py file to get a feel for what you're about to make.

[comment]: <> (Thanks to https://gist.github.com/jbsulli/03df3cdce94ee97937ebda0ffef28287 for the collapsable box)
[comment]: <> (And thanks to Magnus' anwser here https://stackoverflow.com/questions/4823468/comments-in-markdown for how to even make a comment)
<details>
    <summary>It looks a bit like this</summary>

    
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
    
</details>

The first thing you'll want to do is make an icon for your app. Browse to the `./assets/jadeapps` folder and copy the `blankicon.png` file. Place it in a new directory located at `./assets/<your username>_<your app name>` and edit it with your prefered image editing program. You shouldn't edit the background, instead just add something on top of the icon. Rename it to `icon.png` This is the icon i'll place on the main screen of Jade Apps once you're finished with your app. You don't need to do anything else with this file.

Next you should make some UIs. If you're using `guizero` don't do anything yet, but if you're using `PyQt5` create a new directory at `./ui/<your username>_<your app name>` and then open `Qt Designer` make your main ui and save it as `main.ui` in the directory you just created. Next its time to add some code.

Scroll down to the bottom of the apps that are already there.
```python
-- snip --

(Scroll to here)


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

-- snip --
```

You need to create your class. `class <your username>_<your app name>(App):` Add a docstring to explain what your app does
```python
class nfoert_example(App):
    '''This app is a demo for the jade apps github'''
```

Now you need to add your normal `__init__` function. This is the normal function you need in every class.
```python
def __init__(self, name, simpleName, author, version):
        super().__init__(name, simpleName, author, version)
```

Next you need to add your `init` function. This function is called whenever Jade Apps is started and should include your `Actions` which I'll explain later. It's different than the `__init__` function.
```python
def init(self):
        '''This function is required for an App. It does all the startup stuff to make it work.'''
        self.appPrint("Initiating nfoert's test app...")
        self.initUi("main")
```

There's a lot going on here. `appPrint()` is a function that is a pretty print. You should have one saying that your app is initilized. `initUi()` is if you're using PyQt. It automatically sets up your UIs so you can access them with `self.ui["main"]`. The name `main` here means that it's looking for a ui called `main.ui`. Make sure you have a UI with that name, or else it won't work.

Next lets make a function that opens your ui. Every function must accept `args` as a parameter. This is used to pass extra information when/if your function is called by an Action.

```python
def showUi(self, args):
        '''This function is an example of one that opens a UI.'''
        print(args)
        self.returnData("ui")
        self.ui["main"].show()
```

You can see that this function accepts the parameter `args`. You can see that we're refrencing UI `main` and telling it to show. This is normal syntax for PyQt5. It also runs `self.returnData()` which is what tells Jade Assistant what your app is doing, or if it's finished.

| Keyword | Tells Jade Assistant |
| ---------- | ---------- |
| ui | Your app opened a ui |
| loading | This Action will take a little bit of time to complete, please wait |
| Anything else | Jade Assistant will speak this once you set it |

I keep taking about Actions. This is how they work. Actions are the way for you to add functions that Jade Assistant can call. Let's add an action to our `init` function.
```python
def init(self):
        '''This function is required for an App. It does all the startup stuff to make it work.'''
        self.appPrint("Initiating nfoert's test app...")
        self.initUi("main")

        self.addAction("openUi", self.showUi, ["test app show ui", "show ui"], True)

-- snip --
```

You can see that we added a `addAction` call. The first argument is the name of the action. The second argument is the function to run when this action is called. In this case it's the function `self.showUi`. The third argument is a list of the triggers that you can say to Jade Assistant that will trigger this function. There can be multiple strings in this list. And finally, the last argument should be `True` if the function that is called opens a UI. If it dosen't open a UI, this should be `False`.

If you're using guizero to make your UIs, you should create it in the `init` function. If you'd like to refrence parts of your UI outside of the `init` function, you should declare it using `self.app = App()` At this time I have not tested guizero at all, as I prefer PyQt5. If you find a problem or want to add to these instructions, please make an Issue.

You're also going to have to define your app.
```python
nfoert_example_app = nfoert_example("Nfoert's Example", "example", "nfoert", "0.0.1")
nfoert_example_app.init()
```
The variable should be called `<your username>_<your app name>_app`. The first argument is the pretty name for your app. The second argument is a simple name for your app. The third argument is the username of the author of the app. The last argument is the version of your app.


### Building your executable
Your `.ui` files will need to be added to the spec file. Locate the `a.datas` section and go to the bottom. Add this line for each of your UIs.
```
('<your username>_<your app name>/main.ui','./ui/<your username>_<your app name>/main.ui', "DATA"),
```

Jade Apps will automatically import your UIs differently depending if you're running it as a `.py` or a `.exe`


### Adding modules
If your Jade App requires additional modules you can use them, but any large ones like `numpy` ect. may cause the final executable to be very large. You should try to build the executable with `pyinstaller jadeApps.spec` to see how much larger the executable will be.


### Publishing your Jade App
You should create a GitHub repo with your updated version of `jadeApps.py` and any `assets` or `uis`. You should indicate that your repo is to add to this one. Then you should let me know that you created a Jade App by emailing `jadesoftware1@gmail.com`. I'll add it to the next release of Jade Apps. If you update your app you should let me know so I can add it to the next release.


### Getting help
If you need help making your Jade App you could email me at `jadesoftware1@gmail.com` or create an Issue if you find a bug or problem. I hope you have fun and good luck! :)

